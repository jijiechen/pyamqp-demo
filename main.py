# code taken from: https://github.com/Azure/azure-sdk-for-python/blob/117ba5673464a12e66fc455f63fa78c7e250e338/sdk/servicebus/azure-servicebus/samples/async_samples/sample_code_servicebus_async.py
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Examples to show basic async use case of python azure-servicebus SDK, including:
    - Create ServiceBusClient
    - Create ServiceBusSender/ServiceBusReceiver
    - Send single message and batch messages
    - Peek, receive and settle messages
    - Receive and settle dead-lettered messages
    - Receive and settle deferred messages
    - Schedule and cancel scheduled messages
    - Session related operations
"""
import os
import datetime
import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage


_RUN_ITERATOR = False


async def process_message(message):
    print(str(message))


def example_create_servicebus_client_async():
    # [START create_sb_client_from_conn_str_async]
    import os
    from azure.servicebus.aio import ServiceBusClient

    servicebus_connection_str = os.environ["SERVICEBUS_CONNECTION_STR"]
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=servicebus_connection_str)
    # [END create_sb_client_from_conn_str_async]

    # [START create_sb_client_async]
    import os
    from azure.identity.aio import DefaultAzureCredential
    from azure.servicebus.aio import ServiceBusClient

    fully_qualified_namespace = os.environ["SERVICEBUS_FULLY_QUALIFIED_NAMESPACE"]
    servicebus_client = ServiceBusClient(
        fully_qualified_namespace=fully_qualified_namespace, credential=DefaultAzureCredential()
    )
    # [END create_sb_client_async]
    return servicebus_client


async def example_create_servicebus_sender_async():
    servicebus_client = example_create_servicebus_client_async()
    # [START create_servicebus_sender_from_conn_str_async]
    import os
    from azure.servicebus.aio import ServiceBusSender

    servicebus_connection_str = os.environ["SERVICEBUS_CONNECTION_STR"]
    queue_name = os.environ["SERVICEBUS_QUEUE_NAME"]
    queue_sender = ServiceBusSender._from_connection_string(conn_str=servicebus_connection_str, queue_name=queue_name)
    # [END create_servicebus_sender_from_conn_str_async]

    # [START create_servicebus_sender_from_sb_client_async]
    import os
    from azure.servicebus.aio import ServiceBusClient

    servicebus_connection_str = os.environ["SERVICEBUS_CONNECTION_STR"]
    queue_name = os.environ["SERVICEBUS_QUEUE_NAME"]
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=servicebus_connection_str)
    async with servicebus_client:
        queue_sender = servicebus_client.get_queue_sender(queue_name=queue_name)
    # [END create_servicebus_sender_from_sb_client_async]

    queue_sender = servicebus_client.get_queue_sender(queue_name=queue_name)
    return queue_sender


async def example_create_servicebus_receiver_async():
    servicebus_client = example_create_servicebus_client_async()

    # [START create_servicebus_receiver_from_conn_str_async]
    import os
    from azure.servicebus.aio import ServiceBusReceiver

    servicebus_connection_str = os.environ["SERVICEBUS_CONNECTION_STR"]
    queue_name = os.environ["SERVICEBUS_QUEUE_NAME"]
    queue_receiver = ServiceBusReceiver._from_connection_string(
        conn_str=servicebus_connection_str, queue_name=queue_name
    )
    # [END create_servicebus_receiver_from_conn_str_async]

    # [START create_queue_deadletter_receiver_from_sb_client_async]
    import os
    from azure.servicebus import ServiceBusSubQueue
    from azure.servicebus.aio import ServiceBusClient

    servicebus_connection_str = os.environ["SERVICEBUS_CONNECTION_STR"]
    queue_name = os.environ["SERVICEBUS_QUEUE_NAME"]
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=servicebus_connection_str)
    async with servicebus_client:
        queue_receiver = servicebus_client.get_queue_receiver(
            queue_name=queue_name, sub_queue=ServiceBusSubQueue.DEAD_LETTER
        )
    # [END create_queue_deadletter_receiver_from_sb_client_async]

    # [START create_servicebus_receiver_from_sb_client_async]
    import os
    from azure.servicebus.aio import ServiceBusClient

    servicebus_connection_str = os.environ["SERVICEBUS_CONNECTION_STR"]
    queue_name = os.environ["SERVICEBUS_QUEUE_NAME"]
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=servicebus_connection_str)
    async with servicebus_client:
        queue_receiver = servicebus_client.get_queue_receiver(queue_name=queue_name)
    # [END create_servicebus_receiver_from_sb_client_async]

    queue_receiver = servicebus_client.get_queue_receiver(queue_name=queue_name)
    return queue_receiver


async def example_send_and_receive_async():
    from azure.servicebus import ServiceBusMessage

    servicebus_sender = await example_create_servicebus_sender_async()
    # [START send_async]
    async with servicebus_sender:
        message_send = ServiceBusMessage("Hello World")
        await servicebus_sender.send_messages(message_send)
        # [END send_async]
        await servicebus_sender.send_messages([ServiceBusMessage("Hello World")] * 5)

    servicebus_sender = await example_create_servicebus_sender_async()
    # [START create_batch_async]
    async with servicebus_sender:
        batch_message = await servicebus_sender.create_message_batch()
        batch_message.add_message(ServiceBusMessage("Single message inside batch"))
    # [END create_batch_async]

    servicebus_receiver = await example_create_servicebus_receiver_async()
    # [START peek_messages_async]
    async with servicebus_receiver:
        messages = await servicebus_receiver.peek_messages()
        for message in messages:
            print(str(message))
    # [END peek_messages_async]

    servicebus_receiver = await example_create_servicebus_receiver_async()
    # [START receive_async]
    async with servicebus_receiver:
        messages = await servicebus_receiver.receive_messages(max_wait_time=5)
        for message in messages:
            print(str(message))
            await servicebus_receiver.complete_message(message)
    # [END receive_async]

    servicebus_receiver = await example_create_servicebus_receiver_async()
    # [START receive_forever_async]
    async with servicebus_receiver:
        async for message in servicebus_receiver:
            print(str(message))
            await servicebus_receiver.complete_message(message)
            # [END receive_forever_async]
            break

        # [START abandon_message_async]
        messages = await servicebus_receiver.receive_messages(max_wait_time=5)
        for message in messages:
            await servicebus_receiver.abandon_message(message)
        # [END abandon_message_async]

        # [START complete_message_async]
        messages = await servicebus_receiver.receive_messages(max_wait_time=5)
        for message in messages:
            await servicebus_receiver.complete_message(message)
        # [END complete_message_async]

        # [START defer_message_async]
        messages = await servicebus_receiver.receive_messages(max_wait_time=5)
        for message in messages:
            await servicebus_receiver.defer_message(message)
        # [END defer_message_async]

        # [START dead_letter_message_async]
        messages = await servicebus_receiver.receive_messages(max_wait_time=5)
        for message in messages:
            await servicebus_receiver.dead_letter_message(message)
        # [END dead_letter_message_async]

        # [START renew_message_lock_async]
        messages = await servicebus_receiver.receive_messages(max_wait_time=5)
        for message in messages:
            await servicebus_receiver.renew_message_lock(message)
        # [END renew_message_lock_async]

    servicebus_receiver = await example_create_servicebus_receiver_async()
    # [START auto_lock_renew_message_async]
    from azure.servicebus.aio import AutoLockRenewer

    lock_renewal = AutoLockRenewer()
    async with servicebus_receiver:
        async for message in servicebus_receiver:
            lock_renewal.register(servicebus_receiver, message, max_lock_renewal_duration=60)
            await process_message(message)
            await servicebus_receiver.complete_message(message)
            # [END auto_lock_renew_message_async]
            break
    await lock_renewal.close()



if __name__ == "__main__":
    asyncio.run(example_send_and_receive_async())