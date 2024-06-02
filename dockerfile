
FROM python:3.11

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --upgrade pip

RUN mkdir /web
WORKDIR /web


COPY /appka /web/appka
COPY /myapp /web/myapp
COPY manage.py /web/manage.py
COPY .env /web/.env


EXPOSE 8000

# Run the application:

CMD ["python", "manage.py","runserver","0.0.0.0:8000"]
