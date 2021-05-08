from setuptools import find_namespace_packages, setup


def _requires_from_file(filename):
    return open(filename).read().splitlines()


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="reviews",
    packages=find_namespace_packages(include=["reviews.*"]),
    version="0.1.5",
    license="MIT",
    description=(
        "A terminal UI Dashboard for monitoring requests for code review across several Github repositories and pull requests."
    ),
    author="Kyle Harrison",
    author_email="kyle.harrison.dev@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apoclyps/reviews",
    download_url="https://github.com/apoclyps/reviews/archive/0.1.0.tar.gz",
    keywords=["Reviews", "pull request review"],
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
