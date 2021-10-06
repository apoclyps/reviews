FROM python:3.10.0-alpine

# Don't write .pyc files (or __pycache__ dirs) inside the container
ENV PYTHONDONTWRITEBYTECODE 1

RUN /sbin/apk add --no-cache --virtual .deps gcc musl-dev libffi-dev make

# Install Python dependencies from PyPI
COPY requirements*.txt ./

RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache --force-reinstall --ignore-installed -r requirements_dev.txt


# Copy application source code into container
WORKDIR /usr/src/app
COPY . .

CMD [ "bash" ]
