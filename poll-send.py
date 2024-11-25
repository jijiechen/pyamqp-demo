#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Example to show sending message(s) to and receiving messages from a Service Bus Queue with session enabled asynchronously.
"""

import os
import asyncio
from datetime import datetime
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient

sys_print=print
SESSION_QUEUE_NAME = os.environ["SERVICEBUS_SESSION_QUEUE_NAME"]
SESSION_ID = os.environ["SERVICEBUS_SESSION_ID"]
SENDING_SHUTDOWN = os.environ.get("SENDING_SHUTDOWN", False)

def print(*args, **kw):
   sys_print("[%s]" % (datetime.now()),*args, **kw)

async def send_single_message(sender):
    message = ServiceBusMessage("Single session message", session_id=SESSION_ID)
    await sender.send_messages(message)


async def send_a_list_of_messages(sender):
    messages = [ServiceBusMessage("Session Message in list", session_id=SESSION_ID) for _ in range(10)]
    await sender.send_messages(messages)


async def send_batch_message(sender):
    batch_message = await sender.create_message_batch()
    for _ in range(10):
        try:
            batch_message.add_message(
                ServiceBusMessage("Session Message inside a ServiceBusMessageBatch", session_id=SESSION_ID)
            )
        except ValueError:
            # ServiceBusMessageBatch object reaches max_size.
            # New ServiceBusMessageBatch object can be created here to send more data.
            break
    await sender.send_messages(batch_message)

async def send_shutdown_message(sender):
    message = ServiceBusMessage("shutdown", session_id=SESSION_ID)
    await sender.send_messages(message)

async def send(client):
    while True:
        sender = client.get_queue_sender(queue_name=SESSION_QUEUE_NAME)
        async with sender:
            if isinstance(SENDING_SHUTDOWN, str) and SENDING_SHUTDOWN.lower() == "true":
                print('Sending ShutDown message to session ' + SESSION_ID + ' in queue ' + SESSION_QUEUE_NAME)
                await send_shutdown_message(sender)
                break
            else:
                print('Sending new messages to session ' + SESSION_ID + ' in queue ' + SESSION_QUEUE_NAME)
                await send_single_message(sender)
                await send_a_list_of_messages(sender)
                await send_batch_message(sender)
                print('Waiting for 10 seconds')
                await asyncio.sleep(10)
                sys_print('')


async def main():
    servicebus_connection_str = os.environ["SERVICEBUS_CONNECTION_STR"]
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=servicebus_connection_str)

    async with servicebus_client:
        await send(servicebus_client)

asyncio.run(main())