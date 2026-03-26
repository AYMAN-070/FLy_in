PYTHON = python3
MAIN_FILE = fly_in.py
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
all: run
install:
		@echo "Installing system dependencies (tkinter)..."
		sudo apt update && sudo apt install -y python3-tk
		@echo "Installing python dependencies..."
		pip3 install -r requirements.txt
run:
		$(PYTHON) $(MAIN_FILE)
debug:
		$(PYTHON) -m pdb $(MAIN_FILE)
clean:
		find . -type d -name "__pycache__" -exec rm -rf {} +
		find . -type d -name ".mypy_cache" -exec rm -rf {} +
		find . -type f -name "*.pyc" -delete
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

re: clean all

.PHONY: all install run debug clean lint lint-strict re