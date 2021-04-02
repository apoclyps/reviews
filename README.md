# Code Review Manager

> Simplify code review!

### Quick Start

If you want to get up and running with Code Review Manager immediately, run:

```
docker-compose build cli && docker-compose run --rm cli python cli.py dashboard
```

[![asciicast](https://asciinema.org/a/LEs7tltVE3guhsLEEFGc5FDiD.svg)](https://asciinema.org/a/LEs7tltVE3guhsLEEFGc5FDiD)

### Getting Started

To build and run the CLI on your host, you will need Python 3.9, pip, and virtualenv to build and run `review`:

```bash
$ python3 -m venv env
$ source env/bin/activate
(env)$ pip install -r requirements_dev.txt
(env)$ pip install -r requirements.txt
(env)$ python cli.py dashboard
```

If you wish to keep a copy of code review manager on your host system forever, you can install and run it using:

```bash
$ export ENABLE_NOTIFICATIONS=true
$ export REPOSITORY_CONFIGURATION="apoclyps/code-review-manager"
$ pip install -e .
$ review dashboard
```

Alternatively, you can use docker to build an image and run that image with all of the necessary dependencies using the following commands:

```bash
$ docker-compose build cli
$ docker-compose run --rm cli python cli.py dashboard
```

### Testing

A test suite has been included to ensure Code Review Manager functions correctly:.

To run the entire test suite with verbose output, run the following:

```bash
$ pytest -vvv
```

Alternatively, to run a single set of tests.

```bash
$ pytest -vvv tests/models/test_delivery.py
```

All tests can be run within docker by using the following command:

```bash
$ docker-compose build pytest && docker-compose run --rm pytest
```

### Linting

To run individual linting steps:

```
docker-compose build
docker-compose run --rm black
docker-compose run --rm flake8
docker-compose run --rm isort
docker-compose run --rm mypy
docker-compose run --rm pylint
```

# Contributions

Please read [CONTRIBUTING.md](.github/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
