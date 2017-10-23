import discord
import asyncio
from discord_token import get_token


class imadabot(discord.Client):
    def __init__(self):
        super(imadabot, self).__init__()
        self.testing_channel = None
        
    def run(self, token):
        super(imadabot, self).run(token)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if not message.content.startswith('!'):
            return

        if message.content.startswith('!listen'):
            self.testing_channel = message.channel
            await self.send_message(message.channel, 'This is the testing channel')
        elif self.testing_channel == message.channel:
            if message.content.startswith('!test'):
                counter = 0
                tmp = await self.send_message(message.channel, 'Calculating messages...')
                async for log in self.logs_from(message.channel, limit=100):
                    if log.author == message.author:
                        counter += 1

                await self.edit_message(tmp, 'You have {} messages.'.format(counter))
            elif message.content.startswith('!sleep'):
                await asyncio.sleep(5)
                await self.send_message(message.channel, 'Done sleeping')


if __name__ == "__main__":
    bot = imadabot()
    bot.run(get_token())
