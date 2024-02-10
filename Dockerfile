FROM public.ecr.aws/breezeware/python3.8-alpine:latest

WORKDIR /app

COPY . .

RUN mkdir -p /app/files

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi_upload:app"]