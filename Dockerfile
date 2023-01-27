FROM ghcr.io/withlogicco/poetry:1.3.2-python-3.11

COPY ./ ./
RUN --mount=type=cache,target=/root/.cache/pip --mount=type=cache,target=/root/.cache/pypoetry poetry install

COPY ./ ./
