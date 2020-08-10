# Crazy Eights

> Python implementation of crazy eights card ganme

## To run tests
```bash
$ make test
```

## To run server
```bash
$ make run-server
```

by default runs on port 8080, to use another port run
```bash
$ make run-server SERVER_PORT=<port>
```

## To run client
To start a cli ui with no dependencies run:
```bash
$ make run-client SERVER_HOST=<ip> SERVER_PORT=<port> USERNAME=<usename>
```