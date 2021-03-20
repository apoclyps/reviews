from setuptools import setup


def _requires_from_file(filename):
    return open(filename).read().splitlines()


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="code review manager",
    packages=["code_review_manager"],
    version="0.0.1",
    license="MIT",
    description=("Code Review MAnager written in Python. Standalone client included."),
    author="Kyle Harrison",
    author_email="kyle.harrison.dev@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apoclyps/code-review-manager",
    download_url="https://github.com/apoclyps/code-review-manager/archive/0.0.1.tar.gz",
    keywords=["code review manager", "pull request review"],
    install_requires=_requires_from_file("requirements.txt"),
    entry_points={"console_scripts": ["review = cli:main"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.9",
    ],
)
