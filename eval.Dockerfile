FROM python:3-alpine

RUN mkdir /app
WORKDIR /app
ADD eval.py /app

ENTRYPOINT [ "python", "/app/eval.py" ]

LABEL input_1="csv," \
    output="nbclustconfig,-o"
