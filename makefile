TEST_DIR = ./game/test
TEST_FILE_PATTERN = *_test.py

test:
	python3 -m unittest discover -s ${TEST_DIR} -p "${TEST_FILE_PATTERN}"