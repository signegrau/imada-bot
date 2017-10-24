from module import commandmodule
import discord

class roleassigner(commandmodule):
    def __init__(self, config):
        super().__init__('roleassigner', [], {
            'join': self.join,
            'leave': self.leave
        })

        self.config = config

        self.roles = self.config['roles']

    async def join(self, client, message, arguments):
        role_text = arguments[:6].lower()
        member = message.author

        if role_text in self.roles:
            role = discord.utils.get(message.server.roles, id=self.roles[role_text])

            if role not in message.author.roles:
                await client.add_roles(member, role)
                await client.add_reaction(message, '👍')
            else:
                await client.add_reaction(message, '👀')
        else:
            await client.add_reaction(message, '❌')

    async def leave(self, client, message, arguments):
        role_text = arguments[:6].lower()
        member = message.author

        if role_text in self.roles:
            role = discord.utils.get(message.server.roles, id=self.roles[role_text])

            if role in message.author.roles:
                await client.remove_roles(member, role)
                await client.add_reaction(message, '👍')
            else:
                await client.add_reaction(message, '👀‍')
        else:
            await client.add_reaction(message, '❌')
