#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Example to show sending message(s) to and receiving messages from a Service Bus Queue with session enabled asynchronously.
"""

import logging
import os
import sys
import asyncio
from datetime import datetime
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient

SESSION_QUEUE_NAME = os.environ["SERVICEBUS_SESSION_QUEUE_NAME"]
SESSION_ID = os.environ["SERVICEBUS_SESSION_ID"]
FULLY_QUALIFIED_NAMESPACE = os.environ["SERVICEBUS_FULLY_QUALIFIED_NAMESPACE"]
sys_print=print

def print(*args, **kw):
   sys_print("[%s]" % (datetime.now()),*args, **kw)

logger = logging.getLogger("azure.servicebus")
logger.setLevel(logging.DEBUG)
logging.getLogger("azure.servicebus._pyamqp.aio._cbs_async").setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

async def receive_batch_messages(receiver):
    session = receiver.session
    await session.set_state("START")

    continue_receiving = True
    while continue_receiving:
        print("Session state:", await session.get_state())
        received_msgs = await receiver.receive_messages(max_message_count=10, max_wait_time=300)
        for msg in received_msgs:
            print('new message: ' + str(msg))
            await receiver.complete_message(msg)
            await session.renew_lock()
            if str(msg) == "shutdown":
                continue_receiving = False
                await receiver.session.set_state("CLOSED")
                break
    await session.set_state("END")
    print("Session state:", await session.get_state())


async def main():
    servicebus_connection_str = os.environ["SERVICEBUS_CONNECTION_STR"]
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=servicebus_connection_str)

    async with servicebus_client:
        receiver = servicebus_client.get_queue_receiver(queue_name=SESSION_QUEUE_NAME, session_id=SESSION_ID)
        async with receiver:
            await receive_batch_messages(receiver)

        print("Receive is done.")


asyncio.run(main())