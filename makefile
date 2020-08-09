TEST_DIR = ./game/test
TEST_FILE_PATTERN = *_test.py

SERVER_DIR = game/game_service
SERVER_HOST = 127.0.0.1
SERVER_PORT = 8080

test:
	python3 -m unittest discover -s ${TEST_DIR} -p "${TEST_FILE_PATTERN}"

run-server:
	python3 ${SERVER_DIR}/server.py ${SERVER_HOST} ${SERVER_PORT}