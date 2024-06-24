# rabbitmq-app
A simple app to use RabbitMQ. The points-stream folder has one file to send messages to another file that saves the changes from these messages in the database. These files send and receive messages to update a customer's points.

## Development
Install Postgres
```
brew install postgresql@15
```

Install RabbitMQ
```
brew install rabbitmq@3.13.3
```

Start Postgres
```
brew install postgresql@15
```

Start RabbitMQ
```
brew start rabbitmq@3.13.3
```

Install backend dependencies
```
pip3 install -r requirements.txt
```

References: [RabbitMQ documentation tutorials](https://www.rabbitmq.com/tutorials) and [YouTube course: Python Microservices Full Course - Event-Driven Architecture with RabbitMQ](https://www.youtube.com/watch?v=ddrucr_aAzA)
