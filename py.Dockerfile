FROM publysher/alpine-scipy:1.0.0-numpy1.14.0-python3.6-alpine3.7

RUN apk --no-cache add --virtual .builddeps g++ musl-dev && \
    pip install scikit-learn==0.19.1 && \
    apk del .builddeps && \
    rm -rf /root/.cache


RUN mkdir /app
WORKDIR /app
ADD main.py /app


ENTRYPOINT [ "python", "/app/main.py" ]

LABEL input_1="*|pred" \
    input_2="*|true,,static" \
    output="float_score,-o," \
    cpu="300m"
ENV CITYCOL=5
