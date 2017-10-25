import asyncio
from typing import Any

import discord

from command import Command
from module import Module


class TestModule(Module):
    def __init__(self):
        super(TestModule, self).__init__('test', 'Module for testing that stuff works', [], [
            Command('test', 'getting number of messages sent by author', self.test),
            Command('sleep', 'bot will sleep for five seconds', self.sleep)
        ])

    async def test(self, client: discord.Client, message: discord.Message, arguments: str):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    async def sleep(self, client: discord.Client, message: discord.Message, arguments: str):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
