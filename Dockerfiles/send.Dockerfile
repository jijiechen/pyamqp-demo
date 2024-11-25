FROM python:3.9 

ENV SERVICEBUS_CONNECTION_STR='Endpoint=sb://name.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=your-key'
ENV SERVICEBUS_SESSION_QUEUE_NAME='queue_name'
ENV SERVICEBUS_SESSION_ID='session_id'

ADD poll-send.py .
ADD requirements.txt .

RUN pip install -r requirements.txt
CMD ["python", "./poll-send.py"]