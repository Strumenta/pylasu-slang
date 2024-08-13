FROM python:3.11.9-slim-bookworm

RUN apt-get update -y \
    && apt-get install -y \
        build-essential \
        git \
        curl \
        bash-completion \
  && pip install --upgrade pip setuptools \
  && apt-get clean && rm -f /var/lib/apt/lists/*_*

RUN echo "source /usr/share/bash-completion/completions/git" >> /root/.bashrc

RUN curl -sSL https://pdm-project.org/install-pdm.py | python3 - -p /usr/local

WORKDIR /workspace