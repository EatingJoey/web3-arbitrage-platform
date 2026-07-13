FROM golang:1.23.6

WORKDIR /app

COPY . .

RUN go mod download

CMD ["go", "run", "main.go"]