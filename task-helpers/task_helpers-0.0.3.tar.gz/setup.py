#!/usr/bin/env python

from setuptools import find_packages, setup


def read_file(file_path):
    return open(file_path, "rt", encoding="utf-8").read()


setup(
    name="task_helpers",
    version="0.0.3",
    url="https://github.com/loievskyi/task_helpers",
    license="BSD",
    description="A package for creating task helpers.",
    read_file=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="Viacheslav Loievskyi",
    author_email="loievskyi.slava@gmail.com",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=["redis", "aioredis"],
    python_requires=">=3.8",
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    project_urls={
        "Source": "https://github.com/loievskyi/task_helpers",
    },
)
