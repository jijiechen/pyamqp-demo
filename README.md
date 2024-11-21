
## Send

```sh
docker run -it --rm \
  -e 'SERVICEBUS_CONNECTION_STR=sb://name.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=access-key' \
  -e 'SERVICEBUS_FULLY_QUALIFIED_NAMESPACE=name.servicebus.windows.net' \
  -e 'SERVICEBUS_SESSION_QUEUE_NAME=session-enabled-queue' \
  -e 'SERVICEBUS_SESSION_ID=foo' \
  jijiechen/azure-sb-amqp:send
```

## Receive

```sh
docker run -it --rm \
  -e 'SERVICEBUS_CONNECTION_STR=sb://name.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=access-key' \
  -e 'SERVICEBUS_FULLY_QUALIFIED_NAMESPACE=name.servicebus.windows.net' \
  -e 'SERVICEBUS_SESSION_QUEUE_NAME=session-enabled-queue' \
  -e 'SERVICEBUS_SESSION_ID=foo' \
  jijiechen/azure-sb-amqp:receive
```