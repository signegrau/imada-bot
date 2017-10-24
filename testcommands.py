import asyncio


async def test(client, message, arguments):
    counter = 0
    tmp = await client.send_message(message.channel, 'Calculating messages...')
    async for log in client.logs_from(message.channel, limit=100):
        if log.author == message.author:
            counter += 1

    await client.edit_message(tmp, 'You have {} messages.'.format(counter))


async def sleep(client, message, arguments):
    await asyncio.sleep(5)
    await client.send_message(message.channel, 'Done sleeping')


test_commands = {
    "test": test
}