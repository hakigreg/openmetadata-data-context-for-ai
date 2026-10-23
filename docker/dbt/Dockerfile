FROM python:3.12-slim

ARG DBT_CORE_VERSION=1.12.6
ARG DBT_POSTGRES_VERSION=1.11.0

RUN pip install --no-cache-dir \
    "dbt-core==${DBT_CORE_VERSION}" \
    "dbt-postgres==${DBT_POSTGRES_VERSION}"

ENTRYPOINT ["dbt"]
CMD ["--help"]
