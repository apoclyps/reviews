from setuptools import find_namespace_packages, setup


def _requires_from_file(filename):
    return open(filename).read().splitlines()


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="reviews",
    packages=find_namespace_packages(include=["*"]),
    version="0.3.3",
    license="MIT",
    description=("A terminal UI dashboard to monitor requests for code " "review across Github repositories."),
    author="Kyle Harrison",
    author_email="kyle.harrison.dev@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://reviews-cli.dev/",
    download_url="https://pypi.org/project/reviews/",
    project_urls={
        "Funding": "https://ko-fi.com/apoclyps",
        "Say Thanks!": "https://twitter.com/apoclyps",
        "Source": "https://github.com/apoclyps/reviews",
        "Tracker": "https://github.com/apoclyps/reviews/issues",
    },
    keywords=["Reviews", "pull request review"],
    install_requires=_requires_from_file("requirements.txt"),
    entry_points={"console_scripts": ["reviews = reviews.cli.main:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.9",
        "Topic :: Terminals",
    ],
)
