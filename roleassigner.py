from module import commandmodule
import discord

class roleassigner(commandmodule):
    def __init__(self):
        super().__init__('roleassigner', [], {
            'join': self.join,
            'leave': self.leave
        })

        self.roles = {
            'comput': '367283243931795457',
            'mathem': '367283499402657792',
            'applie': '367283552439762945',
            'mat-øk': '367283667136937984'
        }

    async def join(self, client, message, arguments):
        role_text = arguments[:6]
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
        role_text = arguments[:6]
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
