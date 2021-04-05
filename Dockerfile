FROM python:3.9.3-alpine

# Don't write .pyc files (or __pycache__ dirs) inside the container
ENV PYTHONDONTWRITEBYTECODE 1

RUN /sbin/apk add --no-cache --virtual .deps gcc musl-dev libnotify

# Install Python dependencies from PyPI
COPY requirements*.txt ./

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache --force-reinstall --ignore-installed -r requirements_dev.txt
RUN pip install --no-cache --force-reinstall --ignore-installed -r requirements.txt

# Copy application source code into container
WORKDIR /usr/src/app
COPY . .

CMD [ "bash" ]
