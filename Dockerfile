FROM python

COPY . .

RUN pip install -r requirements.txt git+https://github.com/twrecked/pyaarlo

CMD [ "python", "./notification.py" ]