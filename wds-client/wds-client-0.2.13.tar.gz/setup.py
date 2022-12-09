# coding: utf-8

"""
    Workspace Data Service

    This page lists both current and proposed APIs. The proposed APIs which have not yet been implemented are marked as deprecated. This is incongruous, but by using the deprecated flag, we can force swagger-ui to display those endpoints differently.  Error codes and responses for proposed APIs are likely to change as we gain more clarity on their implementation.  As of v0.2, all APIs are subject to change without notice.   # noqa: E501

    The version of the OpenAPI document: v0.2
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "wds-client"
VERSION = "0.2.13"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Workspace Data Service",
    author="OpenAPI Generator community",
    author_email="team@openapitools.org",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Workspace Data Service"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="BSD",
    long_description="""\
    This page lists both current and proposed APIs. The proposed APIs which have not yet been implemented are marked as deprecated. This is incongruous, but by using the deprecated flag, we can force swagger-ui to display those endpoints differently.  Error codes and responses for proposed APIs are likely to change as we gain more clarity on their implementation.  As of v0.2, all APIs are subject to change without notice.   # noqa: E501
    """
)
