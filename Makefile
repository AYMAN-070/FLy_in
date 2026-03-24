PYTHON = python3
MAIN_FILE = fly_in.py

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
all: run
install:
		pip install -r requirements.txt
run:
		$(PYTHON) $(MAIN_FILE)
debug:
		$(PYTHON) -m pdb $(MAIN_FILE)
clean:
		rm -rf __pycache__
		rm -rf .mypy_cache
		rm -rf *.pyc
lint:
		@echo "--- Running Flake8---"
		python3 -m flake8 .
		@echo "--- Running Mypy---"
		python3 -m mypy $(MYPY_FLAGS) .

lint-strict:
		@echo "--- Running Flake8 . ---"
		python3 -m flake8 .
		@echo "--- Running Mypy --strict ---"
		python3 -m mypy --strict $(MYPY_FLAGS) .

.PHONY: install run debug clean lint