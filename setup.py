from setuptools import find_namespace_packages, setup


def _requires_from_file(filename):
    return open(filename).read().splitlines()


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="reviews",
    packages=find_namespace_packages(include=["reviews.*"]),
    version="0.1.2",
    license="MIT",
    description=("Code Review Manager written in Python. Standalone client included."),
    author="Kyle Harrison",
    author_email="kyle.harrison.dev@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apoclyps/code-review-manager",
    download_url="https://github.com/apoclyps/code-review-manager/archive/0.1.0.tar.gz",
    keywords=["code review manager", "pull request review"],
    install_requires=_requires_from_file("requirements.txt"),
    entry_points={"console_scripts": ["reviews = cli:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.9",
        "Topic :: Terminals",
    ],
)
