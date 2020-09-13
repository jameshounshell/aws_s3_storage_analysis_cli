install:
	pip3 install poetry
	poetry install

shell:
	poetry shell

dev: install shell