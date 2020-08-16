# Crazy Eights

> Python implementation of crazy eights card ganme

## Requirements
- Python 3.8+ (python3 command should point to python3.8)
- make

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

## To run GUI
GUI depends on [Eel](https://github.com/samuelhwilliams/Eel), you need to install requirements first
```bash
$ pip install -r requirements.txt 
```

```bash
$ make run-gui
```

## Reference Interface
Only the graphical interface and animation were taken from references for the implementation. 
[card.js](https://github.com/einaregilsson/cards.js)
