FROM ghcr.io/withlogicco/poetry:1.8.3-python-3.12

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY ./ ./
