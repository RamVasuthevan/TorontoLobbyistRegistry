FROM python:3.10

RUN pip install --upgrade pip && \
    pip install pipenv && \
    echo 'if [ -f "Pipfile" ]; then pipenv shell; fi' >> ~/.bashrc
