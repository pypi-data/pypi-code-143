#!/usr/bin/env python
import logging
import os
import sys
from os.path import abspath, dirname

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings

app_name = "edc_csf"
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    template_dirs=[os.path.join(base_dir, app_name, "tests", "templates")],
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    SUBJECT_VISIT_MODEL="edc_csf_app.subjectvisit",
    SUBJECT_VISIT_MISSED_MODEL="edc_appointment.subjectvisitmissed",
    SUBJECT_REQUISITION_MODEL="edc_csf_app.subjectrequisition",
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "simple_history",
        "multisite",
        "django_crypto_fields.apps.AppConfig",
        # "edc_action_item.apps.AppConfig",
        "edc_lab.apps.AppConfig",
        "edc_appointment.apps.AppConfig",
        "edc_crf.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_metadata.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_csf_app.apps.AppConfig",
        "edc_csf.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failures = DiscoverRunner(failfast=False, tags=tags).run_tests([f"{app_name}.tests"])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
