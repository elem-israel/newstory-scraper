FROM python:3.7-slim-buster
WORKDIR /code
RUN sed -i "s#deb http://deb.debian.org/debian buster main#deb http://deb.debian.org/debian buster main contrib non-free#g" /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
      # Firefox dependencies
      libgtk-3-0 libdbus-glib-1-2 libx11-xcb1 libxt6 \
      # Firefox downlader dependencies
      bzip2 \
      wget \
      gcc \
      g++ \
    # Install newesst firefox
    && wget -q -O - "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64"  | tar -xj -C /opt \
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
    && sed -i "320s#bitness in name]#bitness in name and name[-3:] != 'asc' ]#g" /usr/local/lib/python3.7/site-packages/webdriverdownloader/webdriverdownloader.py

RUN wget -O '/usr/local/lib/python3.7/site-packages/instapy/xpath_compile.py' https://raw.githubusercontent.com/InstaPy/instapy-docker/master/xpath_compile.py
ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

COPY requirements.txt /queue/
WORKDIR /queue
RUN pip install -r requirements.txt

COPY src /queue/src
COPY celeryconfig.py /queue/
COPY start_flower.sh /queue/
RUN chmod 755 start_flower.sh

ENTRYPOINT celery -A src worker --loglevel=info -Q * --concurrency 1