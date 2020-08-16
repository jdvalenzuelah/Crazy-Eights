TEST_DIR = ./game/test
TEST_FILE_PATTERN = *_test.py

SERVER_DIR = service
SERVER_HOST = 127.0.0.1
SERVER_PORT = 8080

CLIENT_DIR = service
USERNAME = Crazy

GUI_DIR = ./gui

test:
	python3 -m unittest discover -s ${TEST_DIR} -p "${TEST_FILE_PATTERN}"

run-server:
	python3 ${SERVER_DIR}/server.py ${SERVER_HOST} ${SERVER_PORT}

run-client:
	python3 ${CLIENT_DIR}/client_cli.py ${SERVER_HOST} ${SERVER_PORT} ${USERNAME}

run-gui:
	python3 ${GUI_DIR}/main.py ${SERVER_HOST} ${SERVER_PORT}