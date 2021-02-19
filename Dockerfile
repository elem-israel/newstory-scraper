FROM python:3.7-slim-buster
WORKDIR /code
RUN set -x \
  && sed -i "s#deb http://deb.debian.org/debian buster main#deb http://deb.debian.org/debian buster main contrib non-free#g" /etc/apt/sources.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  # Firefox dependencies
  libgtk-3-0 libdbus-glib-1-2 libx11-xcb1 libxt6 \
  # Firefox downlader dependencies
  bzip2 \
  wget \
  gcc \
  g++ \
  # Install newesst Firefox
  && wget -q -O - "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64" | tar -xj -C /opt \
  && ln -s /opt/firefox/firefox /usr/bin/ \
  && wget -O '/tmp/requirements.txt' https://raw.githubusercontent.com/InstaPy/instapy-docker/master/requirements.txt \
  && pip install --no-cache-dir -U -r /tmp/requirements.txt \
  && apt-get purge -y --auto-remove \
  gcc \
  g++ \
  bzip2 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/requirements.txt \
  # Disabling geckodriver log file
  && sed -i "s#browser = webdriver.Firefox(#browser = webdriver.Firefox(service_log_path=os.devnull,#g" /usr/local/lib/python3.7/site-packages/instapy/browser.py \
  # Fix webdriverdownloader not handling asc files
  && sed -i "s#bitness in name]#bitness in name and name[-3:] != 'asc' ]#g" /usr/local/lib/python3.7/site-packages/webdriverdownloader/webdriverdownloader.py

ENV ACCEPT_EULA=Y
RUN set -x \
    && apt-get update \
    && apt-get install -y \
    curl \
    gnupg \
    build-essential \
    locales \
    apt-transport-https \
    vim \
# Microsoft SQL Server Prerequisites
    && cd /tmp \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && apt-get update \
    && apt-get -y --no-install-recommends install \
        unixodbc-dev \
        msodbcsql17 \
# Update odbcinst.ini to make sure full path to driver is listed
    && sed 's/Driver=psql/Driver=\/usr\/lib\/x86_64-linux-gnu\/odbc\/psql/' /etc/odbcinst.ini > /tmp/temp.ini \
    && mv -f /tmp/temp.ini /etc/odbcinst.ini \
    && pip install pyodbc==4.0.30 \
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

ADD src /usr/src/app/
COPY scripts/entrypoint.sh /usr/src/app/
RUN chmod 755 /usr/src/app/entrypoint.sh

ENTRYPOINT  ./entrypoint.sh
