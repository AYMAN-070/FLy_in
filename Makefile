PYTHON = python3
MAIN_FILE = fly_in.py
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --explicit-package-bases
all: run
install:
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
		python3 -m flake8 fly_in.py src/
		@echo "--- Running Mypy---"
		python3 -m mypy $(MYPY_FLAGS) fly_in.py src/parsing.py src/simulation.py src/visualizer.py src/models.py

lint-strict:
		@echo "--- Running Flake8 . ---"
		python3 -m flake8 .
		@echo "--- Running Mypy --strict ---"
		python3 -m mypy --strict $(MYPY_FLAGS) fly_in.py src/parsing.py src/simulation.py src/visualizer.py src/models.py

re: clean all

.PHONY: all install run debug clean lint lint-strict re