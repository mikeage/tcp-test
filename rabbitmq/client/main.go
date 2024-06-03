package main

import (
	"crypto/tls"
	"log"
	"net/url"
	"os"

	"github.com/rabbitmq/amqp091-go"
)

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func main() {
	addr := os.Getenv("RMQ_CONNECTION_STRING")

	url, err := url.Parse(addr)
	failOnError(err, "Failed to parse RMQ_CONNECTION_STRING")

	// Create a custom TLS configuration if the scheme is "amqps"
	var tlsConfig *tls.Config
	if url.Scheme == "amqps" {
		tlsConfig = &tls.Config{
			InsecureSkipVerify: true,
		}
	}

	// Dial with or without TLS based on the URL scheme
	var conn *amqp091.Connection
	if tlsConfig != nil {
		conn, err = amqp091.DialTLS(addr, tlsConfig)
	} else {
		conn, err = amqp091.Dial(addr)
	}
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()
	channelClose := conn.NotifyClose(make(chan *amqp091.Error))
	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"hello", // name
		false,   // durable
		false,   // delete when unused
		false,   // exclusive
		false,   // no-wait
		nil,     // arguments
	)
	failOnError(err, "Failed to declare a queue")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failOnError(err, "Failed to register a consumer")

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	for {
		select {
		case err := <-channelClose:
			// If err is nil - this is normal close which called during tear down - so ignore it
			if err != nil {
				failOnError(err, "RabbitMQ Channel Error")
			}
		case data := <-msgs:
			log.Printf("Received a message: %s", data.Body)
		}
	}

}
