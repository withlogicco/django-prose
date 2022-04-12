FROM ghcr.io/withlogicco/poetry:1.1.13-python-3.10-slim

COPY ./ ./
RUN --mount=type=cache,target=/root/.cache/pip --mount=type=cache,target=/root/.cache/pypoetry poetry install

COPY ./ ./
