FROM golang:1.19
WORKDIR /app
COPY go.mod go.sum main.go /app/
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/main
CMD ["/app/main"]
