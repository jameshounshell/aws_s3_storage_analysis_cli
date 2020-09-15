# General
# =======
fmt:
	poetry run black .

install:
	pip3 install poetry
	poetry install

shell:
	poetry shell
# run this the first times starting the project
dev: install shell

cli:
	poetry run python store/cli.py

# Testing
# =======
unit_test_files = $(shell python3 -c "import glob; print(' '.join(glob.glob('store/**/*.py', recursive=True)))")

unit_test:
	poetry run pytest $(unit_test_files)

ptw:
	poetry run ptw $(unit_test_files)

integration_test:
	poetry run pytest

test:
	poetry run pytest tests $(unit_test_files)

speed_test:
	poetry run python3 -m timeit -n 1 -r 1 "import store; store.main()"

# Build
# =====
pyinstaller:
	poetry run pyinstaller -n store --onefile store/cli.py
	@printf "\n\nPlease copy the 'store' binary in 'dist/' to a folder on your path"

docker_build:
	docker build -t store .