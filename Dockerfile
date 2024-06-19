FROM python:3.11-slim-buster

WORKDIR /service

ADD . /service

RUN if [ -f /service/app/config/env.yml ]; then rm /service/app/config/env.yml; fi

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/service/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]