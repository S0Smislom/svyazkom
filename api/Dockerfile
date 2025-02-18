FROM snakepacker/python:all AS builder

WORKDIR /code
RUN python3.11 -m venv /code/venv
ENV PATH="/code/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --no-deps --upgrade -r requirements.txt
RUN find-libdeps /code/venv > /code/venv/pkgdeps.txt


FROM snakepacker/python:3.11

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

RUN mkdir -p /code/app && chown python:python /code/app
WORKDIR /code/app

COPY --chown=python:python --from=builder /code/venv /code/venv
RUN xargs -ra /code/venv/pkgdeps.txt apt-install

COPY --chown=python:python . .

USER 999

ENV PATH="/code/venv/bin:$PATH"
ENV PYTHONPATH="/code/app"
