FROM python:3.11.5-slim

ARG UNAME=niksk
ARG UID=2022
ARG GID=4004

RUN groupadd -g ${GID} ${UNAME} \
    && useradd -m -u ${UID} -g ${GID} -o -s /bin/bash ${UNAME}


WORKDIR /app

COPY mysite /app
COPY entrypoint.sh /

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r /app/requirements.txt

USER ${UNAME}

ENTRYPOINT ["/entrypoint.sh"]
