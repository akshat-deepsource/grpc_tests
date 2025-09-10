# enki-grpc-client-test

 - Use `cli.py` to connect to gRPC client
 - Use `rmq_publisher` to publish object meta to a queue


### Envs required
 - CLIENT_RECONNECTION_TIMEOUT=<value in seconds>
 - RMQ_HOST=<rabbit mq host>
 - SESSION_ID=<queue name to which consumer connects>
