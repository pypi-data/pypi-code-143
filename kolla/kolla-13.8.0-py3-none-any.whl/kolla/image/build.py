#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib
import datetime
import errno
import json
import logging
import os
import queue
import re
import requests
import shutil
import sys
import tarfile
import tempfile
import threading
import time

from distutils.version import StrictVersion
import docker
from enum import Enum
import git
import jinja2
from oslo_config import cfg
from requests import exceptions as requests_exc


# NOTE(SamYaple): Update the search path to prefer PROJECT_ROOT as the source
#                 of packages to import if we are using local tools instead of
#                 pip installed kolla tools
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from kolla.common import config as common_config  # noqa
from kolla.common import task  # noqa
from kolla.common import utils  # noqa
from kolla import exception  # noqa
from kolla.template import filters as jinja_filters  # noqa
from kolla.template import methods as jinja_methods  # noqa
from kolla import version  # noqa


class Status(Enum):
    CONNECTION_ERROR = 'connection_error'
    PUSH_ERROR = 'push_error'
    ERROR = 'error'
    PARENT_ERROR = 'parent_error'
    BUILT = 'built'
    BUILDING = 'building'
    UNMATCHED = 'unmatched'
    MATCHED = 'matched'
    UNPROCESSED = 'unprocessed'
    SKIPPED = 'skipped'
    UNBUILDABLE = 'unbuildable'


# All error status constants.
STATUS_ERRORS = (Status.CONNECTION_ERROR, Status.PUSH_ERROR,
                 Status.ERROR, Status.PARENT_ERROR)

LOG = utils.make_a_logger()

# The dictionary of unbuildable images supports keys in the format:
# '<distro>+<installation_type>+<arch>' where each component is optional
# and can be omitted along with the + separator which means that component
# is irrelevant. Otherwise all must match for skip to happen.
UNBUILDABLE_IMAGES = {
    'aarch64': {
        "bifrost-base",      # someone need to get upstream working first
        "prometheus-mtail",  # no aarch64 binary
        "skydive-base",      # no aarch64 binary
    },

    'binary': {
        "bifrost-base",
        "blazar-base",
        "cyborg-base",
        "freezer-base",
        "kuryr-base",
        "monasca-base",
        "monasca-thresh",
        "solum-base",
        "vmtp",
        "zun-base",
    },

    'centos': {
        "hacluster-pcs",         # Missing crmsh package
        "nova-spicehtml5proxy",  # Missing spicehtml5 package
        "ovsdpdk",               # Not supported on CentOS
        "tgtd",                  # Not supported on CentOS 8
    },

    'debian': {
        "bifrost-base",  # tries to install 'mysql-server' which is not in
                         # Debian 'buster' (fixed in Yoga)
        "qdrouterd",     # no qdrouterd package in Debian bullseye
    },

    'ubuntu': {
        "qdrouterd",  # There is no qdrouterd package for Ubuntu
    },

    'debian+aarch64': {
        "ovn-base",      # no binary package
    },

    'ubuntu+aarch64': {
        "kibana",        # no binary package
        "monasca-base",  # 'confluent-kafka' requires newer libfdkafka-dev
                         # than distribution has
    },

    'centos+aarch64': {
        "hacluster-pcs",  # no binary package
        "influxdb",       # no binary package
        "kibana",         # no binary package
        "monasca-base",   # 'confluent-kafka' requires newer libfdkafka-dev
                          # than distribution has
        "telegraf",       # no binary package
    },

    "centos+binary": {
        "masakari-base",
    },

    'debian+binary': {
        "nova-serialproxy",      # no binary package
        "tacker-base",           # no binary package
    },

    'ubuntu+binary': {
        "cloudkitty-base",  # no binary packages in UCA
        "senlin-conductor",  # no binary package
        "senlin-health-manager",  # no binary package
        "tacker-base",
        "vitrage-base",
        "neutron-mlnx-agent",
    },
}

# NOTE(hrw): all non-infra images and their children
BINARY_SOURCE_IMAGES = [
    'kolla-toolbox',
    'openstack-base',
    'monasca-thresh',
]


class ArchivingError(Exception):
    pass


@contextlib.contextmanager
def join_many(threads):
    try:
        yield
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        try:
            LOG.info('Waiting for daemon threads exit. Push Ctrl + c again to'
                     ' force exit')
            for t in threads:
                if t.is_alive():
                    LOG.debug('Waiting thread %s to exit', t.name)
                    # NOTE(Jeffrey4l): Python Bug: When join without timeout,
                    # KeyboardInterrupt is never sent.
                    t.join(0xffff)
                LOG.debug('Thread %s exits', t.name)
        except KeyboardInterrupt:
            LOG.warning('Force exits')


class DockerTask(task.Task):

    docker_kwargs = docker.utils.kwargs_from_env()

    def __init__(self):
        super(DockerTask, self).__init__()
        self._dc = None

    @property
    def dc(self):
        if self._dc is not None:
            return self._dc
        docker_kwargs = self.docker_kwargs.copy()
        self._dc = docker.APIClient(version='auto', **docker_kwargs)
        return self._dc


class Image(object):
    def __init__(self, name, canonical_name, path, parent_name='',
                 status=Status.UNPROCESSED, parent=None,
                 source=None, logger=None, docker_client=None):
        self.name = name
        self.canonical_name = canonical_name
        self.path = path
        self.status = status
        self.parent = parent
        self.source = source
        self.parent_name = parent_name
        if logger is None:
            logger = utils.make_a_logger(image_name=name)
        self.logger = logger
        self.children = []
        self.plugins = []
        self.additions = []
        self.dc = docker_client

    def copy(self):
        c = Image(self.name, self.canonical_name, self.path,
                  logger=self.logger, parent_name=self.parent_name,
                  status=self.status, parent=self.parent)
        if self.source:
            c.source = self.source.copy()
        if self.children:
            c.children = list(self.children)
        if self.plugins:
            c.plugins = list(self.plugins)
        if self.additions:
            c.additions = list(self.additions)
        return c

    def in_docker_cache(self):
        return len(self.dc.images(name=self.canonical_name, quiet=True)) == 1

    def __repr__(self):
        return ("Image(%s, %s, %s, parent_name=%s,"
                " status=%s, parent=%s, source=%s)") % (
            self.name, self.canonical_name, self.path,
            self.parent_name, self.status, self.parent, self.source)


class PushIntoQueueTask(task.Task):
    """Task that pushes some other task into a queue."""

    def __init__(self, push_task, push_queue):
        super(PushIntoQueueTask, self).__init__()
        self.push_task = push_task
        self.push_queue = push_queue

    @property
    def name(self):
        return 'PushIntoQueueTask(%s)' % (self.push_task.name)

    def run(self):
        self.push_queue.put(self.push_task)
        self.success = True


class PushError(Exception):
    """Raised when there is a problem with pushing image to repository."""
    pass


class PushTask(DockerTask):
    """Task that pushes an image to a docker repository."""

    def __init__(self, conf, image):
        super(PushTask, self).__init__()
        self.conf = conf
        self.image = image
        self.logger = image.logger

    @property
    def name(self):
        return 'PushTask(%s)' % self.image.name

    def run(self):
        image = self.image
        self.logger.info('Trying to push the image')
        try:
            self.push_image(image)
        except requests_exc.ConnectionError:
            self.logger.exception('Make sure Docker is running and that you'
                                  ' have the correct privileges to run Docker'
                                  ' (root)')
            image.status = Status.CONNECTION_ERROR
        except PushError as exception:
            self.logger.error(exception)
            image.status = Status.PUSH_ERROR
        except Exception:
            self.logger.exception('Unknown error when pushing')
            image.status = Status.PUSH_ERROR
        finally:
            if (image.status not in STATUS_ERRORS and
                    image.status != Status.UNPROCESSED):
                self.logger.info('Pushed successfully')
                self.success = True
            else:
                self.success = False

    def push_image(self, image):
        kwargs = dict(stream=True, decode=True)

        # Since docker 3.0.0, the argument of 'insecure_registry' is removed.
        # To be compatible, set 'insecure_registry=True' for old releases.
        # NOTE(frickler): The version check will fail for docker >= 6.0, but
        # in that case we know that the workaround isn't needed.
        try:
            dc_running_ver = StrictVersion(docker.version)
            if dc_running_ver < StrictVersion('3.0.0'):
                kwargs['insecure_registry'] = True
        except TypeError:
            pass

        for response in self.dc.push(image.canonical_name, **kwargs):
            if 'stream' in response:
                self.logger.info(response['stream'])
            elif 'errorDetail' in response:
                raise PushError(response['errorDetail']['message'])

        # Reset any previous errors.
        image.status = Status.BUILT


class BuildTask(DockerTask):
    """Task that builds out an image."""

    def __init__(self, conf, image, push_queue):
        super(BuildTask, self).__init__()
        self.conf = conf
        self.image = image
        self.push_queue = push_queue
        self.forcerm = not conf.keep
        self.logger = image.logger

    @property
    def name(self):
        return 'BuildTask(%s)' % self.image.name

    def run(self):
        self.builder(self.image)
        if self.image.status in (Status.BUILT, Status.SKIPPED):
            self.success = True

    @property
    def followups(self):
        followups = []
        if self.conf.push and self.success:
            followups.extend([
                # If we are supposed to push the image into a docker
                # repository, then make sure we do that...
                PushIntoQueueTask(
                    PushTask(self.conf, self.image),
                    self.push_queue),
            ])
        if self.image.children and self.success:
            for image in self.image.children:
                if image.status in (Status.UNMATCHED, Status.SKIPPED,
                                    Status.UNBUILDABLE):
                    continue
                followups.append(BuildTask(self.conf, image, self.push_queue))
        return followups

    def process_source(self, image, source):
        dest_archive = os.path.join(image.path, source['name'] + '-archive')

        # NOTE(mgoddard): Change ownership of files to root:root. This
        # avoids an issue introduced by the fix for git CVE-2022-24765,
        # which breaks PBR when the source checkout is not owned by the
        # user installing it. LP#1969096
        def reset_userinfo(tarinfo):
            tarinfo.uid = tarinfo.gid = 0
            tarinfo.uname = tarinfo.gname = "root"
            return tarinfo

        if source.get('type') == 'url':
            self.logger.debug("Getting archive from %s", source['source'])
            try:
                r = requests.get(source['source'], timeout=self.conf.timeout)
            except requests_exc.Timeout:
                self.logger.exception(
                    'Request timed out while getting archive from %s',
                    source['source'])
                image.status = Status.ERROR
                return

            if r.status_code == 200:
                with open(dest_archive, 'wb') as f:
                    f.write(r.content)
            else:
                self.logger.error(
                    'Failed to download archive: status_code %s',
                    r.status_code)
                image.status = Status.ERROR
                return

        elif source.get('type') == 'git':
            clone_dir = '{}-{}'.format(dest_archive,
                                       source['reference'].replace('/', '-'))
            if os.path.exists(clone_dir):
                self.logger.info("Clone dir %s exists. Removing it.",
                                 clone_dir)
                shutil.rmtree(clone_dir)

            try:
                self.logger.debug("Cloning from %s", source['source'])
                git.Git().clone(source['source'], clone_dir)
                git.Git(clone_dir).checkout(source['reference'])
                reference_sha = git.Git(clone_dir).rev_parse('HEAD')
                self.logger.debug("Git checkout by reference %s (%s)",
                                  source['reference'], reference_sha)
            except Exception as e:
                self.logger.error("Failed to get source from git", image.name)
                self.logger.error("Error: %s", e)
                # clean-up clone folder to retry
                shutil.rmtree(clone_dir)
                image.status = Status.ERROR
                return

            with tarfile.open(dest_archive, 'w') as tar:
                tar.add(clone_dir, arcname=os.path.basename(clone_dir),
                        filter=reset_userinfo)

        elif source.get('type') == 'local':
            self.logger.debug("Getting local archive from %s",
                              source['source'])
            if os.path.isdir(source['source']):
                with tarfile.open(dest_archive, 'w') as tar:
                    tar.add(source['source'],
                            arcname=os.path.basename(source['source']),
                            filter=reset_userinfo)
            else:
                shutil.copyfile(source['source'], dest_archive)

        else:
            self.logger.error("Wrong source type '%s'", source.get('type'))
            image.status = Status.ERROR
            return

        # Set time on destination archive to epoch 0
        os.utime(dest_archive, (0, 0))

        return dest_archive

    def update_buildargs(self):
        buildargs = dict()
        if self.conf.build_args:
            buildargs = dict(self.conf.build_args)

        proxy_vars = ('HTTP_PROXY', 'http_proxy', 'HTTPS_PROXY',
                      'https_proxy', 'FTP_PROXY', 'ftp_proxy',
                      'NO_PROXY', 'no_proxy')

        for proxy_var in proxy_vars:
            if proxy_var in os.environ and proxy_var not in buildargs:
                buildargs[proxy_var] = os.environ.get(proxy_var)

        if not buildargs:
            return None
        return buildargs

    def builder(self, image):

        def make_an_archive(items, arcname, item_child_path=None):
            if not item_child_path:
                item_child_path = arcname
            archives = list()
            items_path = os.path.join(image.path, item_child_path)
            for item in items:
                archive_path = self.process_source(image, item)
                if image.status in STATUS_ERRORS:
                    raise ArchivingError
                archives.append(archive_path)
            if archives:
                for archive in archives:
                    with tarfile.open(archive, 'r') as archive_tar:
                        archive_tar.extractall(path=items_path)
            else:
                try:
                    os.mkdir(items_path)
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        self.logger.info(
                            'Directory %s already exist. Skipping.',
                            items_path)
                    else:
                        self.logger.error('Failed to create directory %s: %s',
                                          items_path, e)
                        image.status = Status.CONNECTION_ERROR
                        raise ArchivingError
            arc_path = os.path.join(image.path, '%s-archive' % arcname)

            # NOTE(jneumann): Change ownership of files to root:root. This
            # avoids an issue introduced by the fix for git CVE-2022-24765,
            # which breaks PBR when the source checkout is not owned by the
            # user installing it. LP#1969096
            def reset_userinfo(tarinfo):
                tarinfo.uid = tarinfo.gid = 0
                tarinfo.uname = tarinfo.gname = "root"
                return tarinfo

            with tarfile.open(arc_path, 'w') as tar:
                tar.add(items_path, arcname=arcname, filter=reset_userinfo)
            return len(os.listdir(items_path))

        self.logger.debug('Processing')

        if image.status in [Status.SKIPPED, Status.UNBUILDABLE]:
            self.logger.info('Skipping %s' % image.name)
            return

        if image.status == Status.UNMATCHED:
            return

        if (image.parent is not None and
                image.parent.status in STATUS_ERRORS):
            self.logger.error('Parent image error\'d with message "%s"',
                              image.parent.status)
            image.status = Status.PARENT_ERROR
            return

        image.status = Status.BUILDING
        image.start = datetime.datetime.now()
        self.logger.info('Building started at %s' % image.start)

        if image.source and 'source' in image.source:
            self.process_source(image, image.source)
            if image.status in STATUS_ERRORS:
                return

        if self.conf.install_type == 'source':
            try:
                plugins_am = make_an_archive(image.plugins, 'plugins')
            except ArchivingError:
                self.logger.error(
                    "Failed turning any plugins into a plugins archive")
                return
            else:
                self.logger.debug(
                    "Turned %s plugins into plugins archive",
                    plugins_am)
            try:
                additions_am = make_an_archive(image.additions, 'additions')
            except ArchivingError:
                self.logger.error(
                    "Failed turning any additions into a additions archive")
                return
            else:
                self.logger.debug(
                    "Turned %s additions into additions archive",
                    additions_am)

        # Pull the latest image for the base distro only
        pull = self.conf.pull if image.parent is None else False

        buildargs = self.update_buildargs()
        try:
            for stream in self.dc.build(path=image.path,
                                        tag=image.canonical_name,
                                        nocache=not self.conf.cache,
                                        rm=True,
                                        decode=True,
                                        network_mode=self.conf.network_mode,
                                        pull=pull,
                                        forcerm=self.forcerm,
                                        buildargs=buildargs):
                if 'stream' in stream:
                    for line in stream['stream'].split('\n'):
                        if line:
                            self.logger.info('%s', line)
                if 'errorDetail' in stream:
                    image.status = Status.ERROR
                    self.logger.error('Error\'d with the following message')
                    for line in stream['errorDetail']['message'].split('\n'):
                        if line:
                            self.logger.error('%s', line)
                    return

            if image.status != Status.ERROR and self.conf.squash:
                self.squash()
        except docker.errors.DockerException:
            image.status = Status.ERROR
            self.logger.exception('Unknown docker error when building')
        except Exception:
            image.status = Status.ERROR
            self.logger.exception('Unknown error when building')
        else:
            image.status = Status.BUILT
            now = datetime.datetime.now()
            self.logger.info('Built at %s (took %s)' %
                             (now, now - image.start))

    def squash(self):
        image_tag = self.image.canonical_name
        image_id = self.dc.inspect_image(image_tag)['Id']

        parent_history = self.dc.history(self.image.parent_name)
        parent_last_layer = parent_history[0]['Id']
        self.logger.info('Parent lastest layer is: %s' % parent_last_layer)

        utils.squash(image_id, image_tag, from_layer=parent_last_layer,
                     cleanup=self.conf.squash_cleanup,
                     tmp_dir=self.conf.squash_tmp_dir)
        self.logger.info('Image is squashed successfully')


class WorkerThread(threading.Thread):
    """Thread that executes tasks until the queue provides a tombstone."""

    #: Object to be put on worker queues to get them to die.
    tombstone = object()

    def __init__(self, conf, queue):
        super(WorkerThread, self).__init__()
        self.queue = queue
        self.conf = conf
        self.should_stop = False

    def run(self):
        while not self.should_stop:
            task = self.queue.get()
            if task is self.tombstone:
                # Ensure any other threads also get the tombstone.
                self.queue.put(task)
                break
            try:
                for attempt in range(self.conf.retries + 1):
                    if self.should_stop:
                        break
                    LOG.info("Attempt number: %s to run task: %s ",
                             attempt + 1, task.name)
                    try:
                        task.run()
                        if task.success:
                            break
                    except Exception:
                        LOG.exception('Unhandled error when running %s',
                                      task.name)
                    # try again...
                    task.reset()
                if task.success and not self.should_stop:
                    for next_task in task.followups:
                        LOG.info('Added next task %s to queue',
                                 next_task.name)
                        self.queue.put(next_task)
            finally:
                self.queue.task_done()


class KollaWorker(object):

    def __init__(self, conf):
        self.conf = conf
        self.images_dir = self._get_images_dir()
        self.registry = conf.registry
        if self.registry:
            self.namespace = self.registry + '/' + conf.namespace
        else:
            self.namespace = conf.namespace
        self.base = conf.base
        self.use_dumb_init = conf.use_dumb_init
        self.base_tag = conf.base_tag
        self.install_type = conf.install_type
        self.tag = conf.tag
        self.repos_yaml = conf.repos_yaml
        self.base_arch = conf.base_arch
        self.debian_arch = self.base_arch
        if self.base_arch == 'aarch64':
            self.debian_arch = 'arm64'
        elif self.base_arch == 'x86_64':
            self.debian_arch = 'amd64'
        self.images = list()
        self.openstack_release = conf.openstack_release
        self.docker_healthchecks = conf.docker_healthchecks
        rpm_setup_config = ([repo_file for repo_file in
                             conf.rpm_setup_config if repo_file is not None])
        self.rpm_setup = self.build_rpm_setup(rpm_setup_config)

        if self.base in ['centos']:
            self.conf.distro_python_version = "3.6"
            self.distro_package_manager = 'dnf'
            self.base_package_type = 'rpm'
        elif self.base in ['debian']:
            self.conf.distro_python_version = "3.9"
            self.distro_package_manager = 'apt'
            self.base_package_type = 'deb'
        elif self.base in ['ubuntu']:
            self.conf.distro_python_version = "3.8"
            self.distro_package_manager = 'apt'
            self.base_package_type = 'deb'
        else:
            # Assume worst
            self.conf.distro_python_version = "3.6"

        if self.conf.distro_package_manager is not None:
            self.distro_package_manager = self.conf.distro_package_manager

        if self.conf.base_package_type:
            self.base_package_type = self.conf.base_package_type

        self.clean_package_cache = self.conf.clean_package_cache

        if (self.install_type == 'binary' and self.base == 'debian' and
                self.base_arch != 'x86_64'):
            LOG.info("Debian/binary target is available only for x86-64 "
                     "due to lack of packages for other architectures.")
            sys.exit(1)

        self.image_prefix = self.base + '-' + self.install_type + '-'
        if self.conf.infra_rename:
            self.infra_image_prefix = self.base + '-infra-'
        else:
            self.infra_image_prefix = self.image_prefix

        self.regex = conf.regex
        self.image_statuses_bad = dict()
        self.image_statuses_good = dict()
        self.image_statuses_unmatched = dict()
        self.image_statuses_skipped = dict()
        self.image_statuses_unbuildable = dict()
        self.image_statuses_allowed_to_fail = dict()
        self.maintainer = conf.maintainer
        self.distro_python_version = conf.distro_python_version

        docker_kwargs = docker.utils.kwargs_from_env()
        try:
            self.dc = docker.APIClient(version='auto', **docker_kwargs)
        except docker.errors.DockerException as e:
            self.dc = None
            if not (conf.template_only or
                    conf.save_dependency or
                    conf.list_images or
                    conf.list_dependencies):
                LOG.error("Unable to connect to Docker, exiting")
                LOG.info("Exception caught: {0}".format(e))
                sys.exit(1)

    def _get_images_dir(self):
        possible_paths = (
            PROJECT_ROOT,
            os.path.join(sys.prefix, 'share/kolla'),
            os.path.join(sys.prefix, 'local/share/kolla'),
            os.path.join(os.getenv('HOME', ''), '.local/share/kolla'),
            # NOTE(zioproto): When Kolla is used within a snap, the env var
            #                 $SNAP is the directory where the snap is mounted.
            #                 https://github.com/zioproto/snap-kolla
            #                 More info in snap packages https://snapcraft.io
            os.path.join(os.environ.get('SNAP', ''), 'share/kolla'))

        for path in possible_paths:
            image_path = os.path.join(path, 'docker')
            # NOTE(SamYaple): We explicitly check for the base folder to ensure
            #                 this is the correct path
            # TODO(SamYaple): Improve this to make this safer
            if os.path.exists(os.path.join(image_path, 'base')):
                LOG.info('Found the docker image folder at %s', image_path)
                return image_path
        else:
            raise exception.KollaDirNotFoundException('Image dir can not '
                                                      'be found')

    def build_rpm_setup(self, rpm_setup_config):
        """Generates a list of docker commands based on provided configuration.

        :param rpm_setup_config: A list of .rpm or .repo paths or URLs
                                 (can be empty)
        :return: A list of docker commands
        """
        rpm_setup = list()

        for config in rpm_setup_config:
            if config.endswith('.rpm'):
                # RPM files can be installed with dnf from file path or url
                cmd = "RUN dnf -y install {}".format(config)
            elif config.endswith('.repo'):
                if config.startswith('http'):
                    # Curl http://url/etc.repo to /etc/yum.repos.d/etc.repo
                    name = config.split('/')[-1]
                    cmd = "RUN curl -L {} -o /etc/yum.repos.d/{}".format(
                        config, name)
                else:
                    # Copy .repo file from filesystem
                    cmd = "COPY {} /etc/yum.repos.d/".format(config)
            elif not config:
                cmd = ''
            else:
                raise exception.KollaRpmSetupUnknownConfig(
                    'RPM setup must be provided as .rpm or .repo files.'
                    ' Attempted configuration was {}'.format(config)
                )

            rpm_setup.append(cmd)

        return rpm_setup

    def copy_apt_files(self):
        if self.conf.apt_sources_list:
            shutil.copyfile(
                self.conf.apt_sources_list,
                os.path.join(self.working_dir, "base", "sources.list")
            )

        if self.conf.apt_preferences:
            shutil.copyfile(
                self.conf.apt_preferences,
                os.path.join(self.working_dir, "base", "apt_preferences")
            )

    def copy_dir(self, src, dest):
        if not os.path.isdir(dest):
            shutil.copytree(src, dest)
        else:
            for file in os.listdir(src):
                src_path = os.path.join(src, file)
                dest_path = os.path.join(dest, file)
                if os.path.isdir(src_path):
                    self.copy_dir(src_path, dest_path)
                else:
                    shutil.copy2(src_path, dest_path)

    def setup_working_dir(self):
        """Creates a working directory for use while building."""
        if self.conf.work_dir:
            self.working_dir = os.path.join(self.conf.work_dir, 'docker')
        else:
            ts = time.time()
            ts = datetime.datetime.fromtimestamp(ts).strftime(
                '%Y-%m-%d_%H-%M-%S_')
            self.temp_dir = tempfile.mkdtemp(prefix='kolla-' + ts)
            self.working_dir = os.path.join(self.temp_dir, 'docker')
        self.copy_dir(self.images_dir, self.working_dir)
        for dir in self.conf.docker_dir:
            self.copy_dir(dir, self.working_dir)
        self.copy_apt_files()
        LOG.debug('Created working dir: %s', self.working_dir)

    def set_time(self):
        for root, dirs, files in os.walk(self.working_dir):
            for file_ in files:
                os.utime(os.path.join(root, file_), (0, 0))
            for dir_ in dirs:
                os.utime(os.path.join(root, dir_), (0, 0))
        LOG.debug('Set atime and mtime to 0 for all content in working dir')

    def _get_filters(self):
        filters = {
            'customizable': jinja_filters.customizable,
        }
        return filters

    def _get_methods(self):
        """Mapping of available Jinja methods.

        return a dictionary that maps available function names and their
        corresponding python methods to make them available in jinja templates
        """

        return {
            'debian_package_install': jinja_methods.debian_package_install,
            'handle_repos': jinja_methods.handle_repos,
        }

    def get_users(self):
        all_sections = (set(self.conf._groups.keys()) |
                        set(self.conf.list_all_sections()))
        ret = dict()
        for section in all_sections:
            match = re.search('^.*-user$', section)
            if match:
                user = self.conf[match.group(0)]
                ret[match.group(0)[:-5]] = {
                    'uid': user.uid,
                    'gid': user.gid,
                    'group': user.group,
                }
        return ret

    def create_dockerfiles(self):
        kolla_version = version.version_info.cached_version_string()
        supported_distro_name = common_config.DISTRO_PRETTY_NAME.get(
            self.base)
        for path in self.docker_build_paths:
            template_name = "Dockerfile.j2"
            image_name = path.split("/")[-1]
            ts = time.time()
            build_date = datetime.datetime.fromtimestamp(ts).strftime(
                '%Y%m%d')
            values = {'base_distro': self.base,
                      'base_image': self.conf.base_image,
                      'base_distro_tag': self.base_tag,
                      'base_arch': self.base_arch,
                      'repos_yaml': self.repos_yaml,
                      'use_dumb_init': self.use_dumb_init,
                      'base_package_type': self.base_package_type,
                      'debian_arch': self.debian_arch,
                      'docker_healthchecks': self.docker_healthchecks,
                      'supported_distro_name': supported_distro_name,
                      'image_prefix': self.image_prefix,
                      'infra_image_prefix': self.infra_image_prefix,
                      'install_type': self.install_type,
                      'namespace': self.namespace,
                      'openstack_release': self.openstack_release,
                      'tag': self.tag,
                      'maintainer': self.maintainer,
                      'kolla_version': kolla_version,
                      'image_name': image_name,
                      'users': self.get_users(),
                      'distro_python_version': self.distro_python_version,
                      'distro_package_manager': self.distro_package_manager,
                      'rpm_setup': self.rpm_setup,
                      'build_date': build_date,
                      'clean_package_cache': self.clean_package_cache}
            env = jinja2.Environment(  # nosec: not used to render HTML
                loader=jinja2.FileSystemLoader(self.working_dir))
            env.filters.update(self._get_filters())
            env.globals.update(self._get_methods())
            tpl_path = os.path.join(
                os.path.relpath(path, self.working_dir),
                template_name)

            template = env.get_template(tpl_path)
            if self.conf.template_override:
                tpl_dict = self._merge_overrides(self.conf.template_override)
                template_name = os.path.basename(list(tpl_dict.keys())[0])
                values['parent_template'] = template
                env = jinja2.Environment(  # nosec: not used to render HTML
                    loader=jinja2.DictLoader(tpl_dict))
                env.filters.update(self._get_filters())
                env.globals.update(self._get_methods())
                template = env.get_template(template_name)
            content = template.render(values, env=os.environ)
            content_path = os.path.join(path, 'Dockerfile')
            with open(content_path, 'w') as f:
                LOG.debug("Rendered %s into:", tpl_path)
                LOG.debug(content)
                f.write(content)
                LOG.debug("Wrote it to %s", content_path)

    def _merge_overrides(self, overrides):
        tpl_name = os.path.basename(overrides[0])
        with open(overrides[0], 'r') as f:
            tpl_content = f.read()
        for override in overrides[1:]:
            with open(override, 'r') as f:
                cont = f.read()
            # Remove extends header
            cont = re.sub(r'.*\{\%.*extends.*\n', '', cont)
            tpl_content += cont
        return {tpl_name: tpl_content}

    def find_dockerfiles(self):
        """Recursive search for Dockerfiles in the working directory."""
        self.docker_build_paths = list()
        path = self.working_dir
        filename = 'Dockerfile.j2'

        for root, dirs, names in os.walk(path):
            if filename in names:
                self.docker_build_paths.append(root)
                LOG.debug('Found %s', root.split(self.working_dir)[1])

        LOG.debug('Found %d Dockerfiles', len(self.docker_build_paths))

    def cleanup(self):
        """Remove temp files."""
        if not self.conf.work_dir:
            shutil.rmtree(self.temp_dir)

    def change_install_type(self, image, old_type, new_type):
        # NOTE(hrw): /self.base to make sure that we do not break image name
        image.canonical_name = image.canonical_name.replace(
            f'/{self.base}-{old_type}-',
            f'/{self.base}-{new_type}-')
        if image.children:
            for tmp_image in image.children:
                tmp_image.parent_name = image.canonical_name

    def filter_images(self):
        """Filter which images to build."""
        filter_ = list()

        if self.regex:
            filter_ += self.regex
        elif self.conf.profile:
            for profile in self.conf.profile:
                if profile not in self.conf.profiles:
                    self.conf.register_opt(cfg.ListOpt(profile,
                                                       default=[]),
                                           'profiles')
                if len(self.conf.profiles[profile]) == 0:
                    msg = 'Profile: {} does not exist'.format(profile)
                    raise ValueError(msg)
                else:
                    filter_ += self.conf.profiles[profile]

        # mark unbuildable images and their children
        base = self.base

        tag_element = r'(%s|%s|%s)' % (base,
                                       self.install_type,
                                       self.base_arch)
        tag_re = re.compile(r'^%s(\+%s)*$' % (tag_element, tag_element))
        unbuildable_images = set()

        if not self.conf.enable_unbuildable:
            for set_tag in UNBUILDABLE_IMAGES:
                if tag_re.match(set_tag):
                    unbuildable_images.update(UNBUILDABLE_IMAGES[set_tag])

        if unbuildable_images:
            for image in self.images:
                if image.name in unbuildable_images:
                    image.status = Status.UNBUILDABLE
                else:
                    # let's check ancestors
                    # if any of them is unbuildable then we mark it
                    # and then mark image
                    build_image = True
                    ancestor_image = image
                    while (ancestor_image.parent is not None):
                        ancestor_image = ancestor_image.parent
                        if ancestor_image.name in unbuildable_images or \
                           ancestor_image.status == Status.UNBUILDABLE:
                            build_image = False
                            ancestor_image.status = Status.UNBUILDABLE
                            break
                    if not build_image:
                        image.status = Status.UNBUILDABLE

        # When we want to build a subset of images then filter_ part kicks in.
        # Otherwise we just mark everything buildable as matched for build.

        # First, determine which buildable images match.
        if filter_:
            patterns = re.compile(r"|".join(filter_).join('()'))
            for image in self.images:
                # as we now list not buildable/skipped images we need to
                # process them otherwise list will contain also not requested
                # entries
                if image.status in (Status.MATCHED, Status.UNBUILDABLE):
                    continue
                if re.search(patterns, image.name):
                    image.status = Status.MATCHED

                    ancestor_image = image
                    while (ancestor_image.parent is not None and
                           ancestor_image.parent.status != Status.MATCHED):
                        ancestor_image = ancestor_image.parent
                        # Parents of a buildable image must also be buildable.
                        ancestor_image.status = Status.MATCHED
                    LOG.debug('Image %s matched regex', image.name)
                else:
                    image.status = Status.UNMATCHED
        else:
            for image in self.images:
                if image.status != Status.UNBUILDABLE:
                    image.status = Status.MATCHED

        if self.conf.infra_rename:
            for image in self.images:
                is_infra = True
                if image.name in BINARY_SOURCE_IMAGES:
                    # keep as is
                    is_infra = False
                else:
                    # let's check ancestors if any of them is binary/source
                    ancestor_image = image
                    while (ancestor_image.parent is not None):
                        ancestor_image = ancestor_image.parent
                        if ancestor_image.name in BINARY_SOURCE_IMAGES:
                            is_infra = False
                            break

                if is_infra:
                    self.change_install_type(image, self.install_type, 'infra')
                    pass

        # Next, mark any skipped images.
        for image in self.images:
            if image.status != Status.MATCHED:
                continue
            # Skip image if --skip-existing was given and image exists.
            if (self.conf.skip_existing and image.in_docker_cache()):
                LOG.debug('Skipping existing image %s', image.name)
                image.status = Status.SKIPPED
            # Skip image if --skip-parents was given and image has children.
            elif self.conf.skip_parents and image.children:
                LOG.debug('Skipping parent image %s', image.name)
                image.status = Status.SKIPPED

    def summary(self):
        """Walk the dictionary of images statuses and print results."""
        # For debug we print the logs again if the image error'd. This is to
        # help us debug and it will be extra helpful in the gate.
        for image in self.images:
            if image.status in STATUS_ERRORS:
                LOG.debug("Image %s failed", image.name)

        self.get_image_statuses()
        results = {
            'built': [],
            'failed': [],
            'not_matched': [],
            'skipped': [],
            'unbuildable': [],
        }

        if self.image_statuses_good:
            LOG.info("=========================")
            LOG.info("Successfully built images")
            LOG.info("=========================")
            for name in sorted(self.image_statuses_good.keys()):
                LOG.info(name)
                results['built'].append({
                    'name': name,
                })

        if self.image_statuses_bad or self.image_statuses_allowed_to_fail:
            LOG.info("===========================")
            LOG.info("Images that failed to build")
            LOG.info("===========================")
            all_bad_statuses = self.image_statuses_bad.copy()
            all_bad_statuses.update(self.image_statuses_allowed_to_fail)
            for name, status in sorted(all_bad_statuses.items()):
                if name in self.image_statuses_allowed_to_fail:
                    LOG.error('%s Failed with status: %s (allowed to fail)',
                              name, status.value)
                else:
                    LOG.error('%s Failed with status: %s', name, status.value)

                results['failed'].append({
                    'name': name,
                    'status': status.value,
                })
                if self.conf.logs_dir and status == Status.ERROR:
                    linkname = os.path.join(self.conf.logs_dir,
                                            "000_FAILED_%s.log" % name)
                    try:
                        os.lstat(linkname)
                        os.remove(linkname)
                    except OSError:
                        pass

                    os.symlink("%s.log" % name, linkname)

        if self.image_statuses_unmatched:
            LOG.debug("=====================================")
            LOG.debug("Images not matched for build by regex")
            LOG.debug("=====================================")
            for name in sorted(self.image_statuses_unmatched.keys()):
                LOG.debug(name)
                results['not_matched'].append({
                    'name': name,
                })

        if self.image_statuses_skipped:
            LOG.info("===================================")
            LOG.info("Images skipped due to build options")
            LOG.info("===================================")
            for name in sorted(self.image_statuses_skipped.keys()):
                LOG.info(name)
                results['skipped'].append({
                    'name': name,
                })

        if self.image_statuses_unbuildable:
            LOG.info("=========================================")
            LOG.info("Images not buildable due to build options")
            LOG.info("=========================================")
            for name in sorted(self.image_statuses_unbuildable.keys()):
                LOG.info(name)
                results['unbuildable'].append({
                    'name': name,
                })

        return results

    def get_image_statuses(self):
        if any([self.image_statuses_bad,
                self.image_statuses_good,
                self.image_statuses_unmatched,
                self.image_statuses_skipped,
                self.image_statuses_unbuildable,
                self.image_statuses_allowed_to_fail]):
            return (self.image_statuses_bad,
                    self.image_statuses_good,
                    self.image_statuses_unmatched,
                    self.image_statuses_skipped,
                    self.image_statuses_unbuildable,
                    self.image_statuses_allowed_to_fail)
        for image in self.images:
            if image.status == Status.BUILT:
                self.image_statuses_good[image.name] = image.status
            elif image.status == Status.UNMATCHED:
                self.image_statuses_unmatched[image.name] = image.status
            elif image.status == Status.SKIPPED:
                self.image_statuses_skipped[image.name] = image.status
            elif image.status == Status.UNBUILDABLE:
                self.image_statuses_unbuildable[image.name] = image.status
            else:
                if image.name in self.conf.allowed_to_fail:
                    self.image_statuses_allowed_to_fail[
                        image.name] = image.status
                else:
                    self.image_statuses_bad[image.name] = image.status
        return (self.image_statuses_bad,
                self.image_statuses_good,
                self.image_statuses_unmatched,
                self.image_statuses_skipped,
                self.image_statuses_unbuildable,
                self.image_statuses_allowed_to_fail)

    def build_image_list(self):
        def process_source_installation(image, section):
            installation = dict()
            # NOTE(jeffrey4l): source is not needed when the type is None
            if self.conf._get('type', self.conf._get_group(section)) is None:
                if image.parent_name is None:
                    LOG.debug('No source location found in section %s',
                              section)
            else:
                installation['type'] = self.conf[section]['type']
                installation['source'] = self.conf[section]['location']
                installation['name'] = section
                if installation['type'] == 'git':
                    installation['reference'] = self.conf[section]['reference']
            return installation

        all_sections = (set(self.conf._groups.keys()) |
                        set(self.conf.list_all_sections()))

        for path in self.docker_build_paths:
            # Reading parent image name
            with open(os.path.join(path, 'Dockerfile')) as f:
                content = f.read()

            image_name = os.path.basename(path)
            canonical_name = (self.namespace + '/' + self.image_prefix +
                              image_name + ':' + self.tag)
            parent_search_pattern = re.compile(r'^FROM.*$', re.MULTILINE)
            match = re.search(parent_search_pattern, content)
            if match:
                parent_name = match.group(0).split(' ')[1]
            else:
                parent_name = ''
            del match
            image = Image(image_name, canonical_name, path,
                          parent_name=parent_name,
                          logger=utils.make_a_logger(self.conf, image_name),
                          docker_client=self.dc)

            if self.install_type == 'source':
                # NOTE(jeffrey4l): register the opts if the section didn't
                # register in the kolla/common/config.py file
                if image.name not in self.conf._groups:
                    self.conf.register_opts(common_config.get_source_opts(),
                                            image.name)
                image.source = process_source_installation(image, image.name)
                for plugin in [match.group(0) for match in
                               (re.search('^{}-plugin-.+'.format(image.name),
                                          section) for section in
                                all_sections) if match]:
                    try:
                        self.conf.register_opts(
                            common_config.get_source_opts(),
                            plugin
                        )
                    except cfg.DuplicateOptError:
                        LOG.debug('Plugin %s already registered in config',
                                  plugin)
                    image.plugins.append(
                        process_source_installation(image, plugin))
                for addition in [
                    match.group(0) for match in
                    (re.search('^{}-additions-.+'.format(image.name),
                     section) for section in all_sections) if match]:
                    try:
                        self.conf.register_opts(
                            common_config.get_source_opts(),
                            addition
                        )
                    except cfg.DuplicateOptError:
                        LOG.debug('Addition %s already registered in config',
                                  addition)
                    image.additions.append(
                        process_source_installation(image, addition))

            self.images.append(image)

    def save_dependency(self, to_file):
        try:
            import graphviz
        except ImportError:
            LOG.error('"graphviz" is required for save dependency')
            raise
        dot = graphviz.Digraph(comment='Docker Images Dependency')
        dot.body.extend(['rankdir=LR'])
        for image in self.images:
            if image.status not in [Status.MATCHED]:
                continue
            dot.node(image.name)
            if image.parent is not None:
                dot.edge(image.parent.name, image.name)

        with open(to_file, 'w') as f:
            f.write(dot.source)

    def list_images(self):
        for count, image in enumerate([
            image for image in self.images if image.status == Status.MATCHED
        ]):
            print(count + 1, ':', image.name)

    def list_dependencies(self):
        match = False
        for image in self.images:
            if image.status in [Status.MATCHED]:
                match = True
            if image.parent is None:
                base = image
        if not match:
            print('Nothing matched!')
            return

        def list_children(images, ancestry):
            children = next(iter(ancestry.values()))
            for image in images:
                if image.status not in [Status.MATCHED]:
                    continue
                if not image.children:
                    children.append(image.name)
                else:
                    newparent = {image.name: []}
                    children.append(newparent)
                    list_children(image.children, newparent)

        ancestry = {base.name: []}
        list_children(base.children, ancestry)
        json.dump(ancestry, sys.stdout, indent=2)

    def find_parents(self):
        """Associate all images with parents and children."""
        sort_images = dict()

        for image in self.images:
            sort_images[image.canonical_name] = image

        for parent_name, parent in sort_images.items():
            for image in sort_images.values():
                if (image.parent_name == parent_name or image.parent_name ==
                        parent_name.replace(self.install_type, 'infra')):
                    parent.children.append(image)
                    image.parent = parent

    def build_queue(self, push_queue):
        """Organizes Queue list.

        Return a list of Queues that have been organized into a hierarchy
        based on dependencies
        """
        build_queue = queue.Queue()

        for image in self.images:
            if image.status in (Status.UNMATCHED, Status.SKIPPED,
                                Status.UNBUILDABLE):
                # Don't bother queuing up build tasks for things that
                # were not matched in the first place... (not worth the
                # effort to run them, if they won't be used anyway).
                continue
            # Build all root nodes, where a root is defined as having no parent
            # or having a parent that is explicitly being skipped.
            if image.parent is None or image.parent.status == Status.SKIPPED:
                build_queue.put(BuildTask(self.conf, image, push_queue))
                LOG.info('Added image %s to queue', image.name)

        return build_queue


def run_build():
    """Build container images.

    :return: A 6-tuple containing bad, good, unmatched, skipped,
    unbuildable and allowed to fail container image status dicts,
    or None if no images were built.
    """
    conf = cfg.ConfigOpts()
    common_config.parse(conf, sys.argv[1:], prog='kolla-build')

    if conf.debug:
        LOG.setLevel(logging.DEBUG)

    if conf.squash:
        squash_version = utils.get_docker_squash_version()
        LOG.info('Image squash is enabled and "docker-squash" version is %s',
                 squash_version)

    kolla = KollaWorker(conf)
    kolla.setup_working_dir()
    kolla.find_dockerfiles()
    kolla.create_dockerfiles()
    kolla.build_image_list()
    kolla.find_parents()
    kolla.filter_images()

    if conf.template_only:
        for image in kolla.images:
            if image.status == Status.MATCHED:
                continue

            shutil.rmtree(image.path)

        LOG.info('Dockerfiles are generated in %s', kolla.working_dir)
        return

    # We set the atime and mtime to 0 epoch to preserve allow the Docker cache
    # to work like we want. A different size or hash will still force a rebuild
    kolla.set_time()

    if conf.save_dependency:
        kolla.save_dependency(conf.save_dependency)
        LOG.info('Docker images dependency are saved in %s',
                 conf.save_dependency)
        return
    if conf.list_images:
        kolla.list_images()
        return
    if conf.list_dependencies:
        kolla.list_dependencies()
        return

    push_queue = queue.Queue()
    build_queue = kolla.build_queue(push_queue)
    workers = []

    with join_many(workers):
        try:
            for x in range(conf.threads):
                worker = WorkerThread(conf, build_queue)
                worker.daemon = True
                worker.start()
                workers.append(worker)

            for x in range(conf.push_threads):
                worker = WorkerThread(conf, push_queue)
                worker.daemon = True
                worker.start()
                workers.append(worker)

            # sleep until build_queue is empty
            while build_queue.unfinished_tasks or push_queue.unfinished_tasks:
                time.sleep(3)

            # ensure all threads exited happily
            push_queue.put(WorkerThread.tombstone)
            build_queue.put(WorkerThread.tombstone)
        except KeyboardInterrupt:
            for w in workers:
                w.should_stop = True
            push_queue.put(WorkerThread.tombstone)
            build_queue.put(WorkerThread.tombstone)
            raise

    if conf.summary:
        results = kolla.summary()
        if conf.format == 'json':
            print(json.dumps(results))
    kolla.cleanup()
    return kolla.get_image_statuses()
