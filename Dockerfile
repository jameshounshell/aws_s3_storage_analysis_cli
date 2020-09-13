FROM python:3.7-buster
RUN pip3 install poetry
WORKDIR /app
ADD . /app
RUN poetry install
ENTRYPOINT ["poetry", "run", "python", "store/cli.py"]
CMD ["--help"]