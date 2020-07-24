FROM python:3.7-alpine

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

ENV HOST 0.0.0.0
ENV PORT 5001
ENV DEBUG true

EXPOSE 5001

RUN pip install gunicorn

COPY requirements.txt /api/
WORKDIR /api
RUN pip install -r requirements.txt

COPY src /api

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "3", "app:app"]