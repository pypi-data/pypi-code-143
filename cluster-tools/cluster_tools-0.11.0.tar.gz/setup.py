# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cluster_tools', 'cluster_tools.schedulers']

package_data = \
{'': ['*']}

install_requires = \
['kubernetes>=23.3.0,<24.0.0']

setup_kwargs = {
    'name': 'cluster-tools',
    'version': '0.11.0',
    'description': 'Utility library for easily distributing code execution on clusters',
    'long_description': '# Cluster Tools\n\n[![CircleCI](https://circleci.com/gh/scalableminds/cluster_tools/tree/master.svg?style=svg)](https://circleci.com/gh/scalableminds/cluster_tools/tree/master)\n\nThis package provides python `Executor` classes for distributing tasks on a slurm cluster or via multi processing.\n\n## Example\n\n```python\nimport cluster_tools\n\ndef square(n):\n  return n * n\n\nif __name__ == \'__main__\':\n  strategy = "slurm"  # other valid values are "multiprocessing" and "sequential"\n  with cluster_tools.get_executor(strategy) as executor:\n    result = list(executor.map(square, [2, 3, 4]))\n    assert result == [4, 9, 16]\n```\n\n## Configuration\n\n### Slurm\n\nThe `cluster_tools` automatically determine the slurm limit for maximum array job size and split up larger job batches into multiple smaller batches.\nAlso, the slurm limit for the maximum number of jobs which are allowed to be submitted by a user at the same time is honored by looking up the number of currently submitted jobs and only submitting new batches if they fit within the limit.\n\nIf you would like to configure these limits independently, you can do so by setting the `SLURM_MAX_ARRAY_SIZE` and `SLURM_MAX_SUBMIT_JOBS` environment variables. You can also limit the maximum number of simultaneously running tasks within the slurm array job(s) by using the `SLURM_MAX_RUNNING_SIZE` environment variable.\n\n### Kubernetes\n\n#### Resource configuration\n\n| Key                 | Description                                                                                                                                                                                                                                                              | Example                                 |\n| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------- |\n| `namespace`         | Kubernetes namespace for the resources to be created. Will be created if not existent.                                                                                                                                                                                   | `cluster-tools`                         |\n| `node_selector`     | Which nodes to utilize for the processing. Needs to be a [Kubernetes `nodeSelector` object](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/).                                                                                                   | `{"kubernetes.io/hostname": "node001"}` |\n| `image`             | The docker image for the containerized jobs to run in. The image needs to have the same version of `cluster_tools` and the code to run installed and in the `PYTHONPATH`.                                                                                                | `scalableminds/voxelytics:latest`       |\n| `mounts`            | Additional mounts for the containerized jobs. The current working directory and the `.cfut` directory are automatically mounted.                                                                                                                                         | `["/srv", "/data"]`                     |\n| `cpu`               | [CPU requirements](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) for this job.                                                                                                                                                         | `4`                                     |\n| `memory`            | [Memory requirements](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) for this job. Not required, but highly recommended to avoid congestion. Without resource requirements, all jobs will be run in parallel and RAM will run out soon. | `16G`                                   |\n| `python_executable` | The python executable may differ in the docker image from the one in the current environment. For images based of `FROM python`, it should be `python`. Defaults to `python`.                                                                                            | `python3.8`                             |\n| `umask`             | `umask` for the jobs.                                                                                                                                                                                                                                                    | `0002`                                  |\n\n#### Notes\n\n- The jobs are run with the current `uid:gid`.\n- The jobs are removed 7 days after completion (successful or not).\n- The logs are stored in the `.cfut` directory. This is actually redundant, because Kubernetes also stores them.\n- Pods are not restarted upon error.\n- Requires Kubernetes ≥ 1.23.\n- [Kubernetes cluster configuration](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) is expected to be the same as for `kubectl`, i.e. in `~/.kube/config` or similar.\n\n## Dev Setup\n\n```\ncd dockered-slurm\ndocker-compose up -d\ndocker exec -it slurmctld bash\ndocker exec -it c1 bash\n```\n\nTests can be executed with `cd tests && poetry run pytest -s tests.py` after entering the container.\nLinting can be run with `./lint.sh`.\nCode formatting (black) can be run with `./format.sh`.\n\n## Credits\n\nThanks to [sampsyo/clusterfutures](https://github.com/sampsyo/clusterfutures) for providing the slurm core abstraction and [giovtorres/slurm-docker-cluster](https://github.com/giovtorres/slurm-docker-cluster) for providing the slurm docker environment which we use for CI based testing.\n',
    'author': 'scalable minds',
    'author_email': 'hello@scalableminds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scalableminds/webknossos-libs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
