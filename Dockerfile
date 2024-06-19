FROM python:3.11-slim-buster

WORKDIR /service

ADD . /service

RUN pip install --no-cache-dir -r requirements.txt

# Make our shell script executable
RUN chmod +x entrypoint.sh

EXPOSE 8000

# Use our shell script as the entrypoint
ENTRYPOINT ["/service/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]