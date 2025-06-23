FROM python:3.12.8-slim AS builder

WORKDIR /server

COPY requirements.txt .

RUN pip install -r requirements.txt --prefix=/install

# 2nd stage
FROM python:3.12.8-slim 

COPY --from=builder /install /usr/local/

WORKDIR /server

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "/server/entrypoint.sh" ]

