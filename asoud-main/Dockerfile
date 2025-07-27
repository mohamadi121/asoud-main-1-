FROM python:3.13-alpine

# Skip rust installation and other related dependencies
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CRYPTOGRAPHY_DONT_BUILD_RUST=1

WORKDIR /asoud

# Install runtime and build dependencies
# libffi-dev for cryptography
# libxml2-dev & libxslt-dev for lxml
# jpeg-dev zlib-dev for Pillow
# gettext for Django internationalization
# postgresql-client for PostgreSQL
RUN set -ex && apk add --no-cache \
    python3-dev \
    libffi-dev \
    zlib-dev \
    gettext

# copy requirements aGQoLJDZHx
COPY ./requirements.txt /asoud/requirements.txt

# Create python's env and install Django's dependencies
RUN set -ex \
    # Upgrade pip, setuptools, and wheel
    && pip install --no-cache-dir --upgrade pip \
    # Install Python dependencies
    && pip install --no-cache-dir -r /asoud/requirements.txt

# TODO: Add a non-root user for better security
# RUN addgroup -S appgroup && adduser -S appuser -G appgroup
# USER appuser

COPY . /asoud

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Ensure the entrypoint is executable
RUN chmod +x /asoud/entrypoint.sh

# Ensure the logs directory exists and is writable
RUN mkdir -p /asoud/logs && chmod -R 755 /asoud/logs

# run entrypoint.sh
ENTRYPOINT ["/asoud/entrypoint.sh"]
