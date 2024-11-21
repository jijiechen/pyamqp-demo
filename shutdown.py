#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import os
import asyncio
import uuid

from azure.servicebus.aio import ServiceBusClient, AutoLockRenewer
from azure.servicebus import ServiceBusMessage, NEXT_AVAILABLE_SESSION
from azure.servicebus.exceptions import OperationTimeoutError


# Note: This must be a session-enabled queue.
SESSION_QUEUE_NAME = os.environ["SERVICEBUS_SESSION_QUEUE_NAME"]
SESSION_ID = os.environ["SERVICEBUS_SESSION_ID"]


async def send_async(queue_name):
    servicebus_connection_str = os.environ["SERVICEBUS_CONNECTION_STR"]
    client = ServiceBusClient.from_connection_string(conn_str=servicebus_connection_str)

    async with client.get_queue_sender(queue_name) as sender:
        await sender.send_messages(ServiceBusMessage("shutdown", session_id=SESSION_ID))

if __name__ == "__main__":
    asyncio.run(send_async(SESSION_QUEUE_NAME))