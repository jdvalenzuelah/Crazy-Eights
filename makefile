TEST_DIR = ./game/test
TEST_FILE_PATTERN = *_test.py

SERVER_DIR = game/game_service/

test:
	python3 -m unittest discover -s ${TEST_DIR} -p "${TEST_FILE_PATTERN}"

run-server:
	python3 ${SERVER_DIR}/server.py