import discord

from command import Command
from module import Module


class InformationModule(Module):
    def __init__(self):
        super().__init__('informationmodule', 'Module for printing help for modules', [], [
            Command('help', 'show available commands', self.help_handler),
            Command('info', 'information about bot', self.info_handler)
        ], global_module=True)

    async def info_handler(self, client: discord.Client, message: discord.Message, arguments: str):
        message_text = "I'm a bot made for the IMADA Discord channel. You can help develop me at "" \
                        ""https://github.com/MechaGK/imada-bot"
        await client.send_message(message.channel, message_text)

    async def help_handler(self, client: discord.Client, message: discord.Message, arguments: str):
        modules = client.get_loaded_modules(message.author, message.channel)

        commands = []
        for module in modules:
            commands.extend(module.get_commands(message.author, message.channel))

        if len(commands) < 1:
            await client.send_message(message.channel, "No commands available in this channel")
            return

        message_text = 'Available commands:\n```'

        for command in sorted(commands, key=lambda c: c.name):
            message_text += f'\n{command.get_name():{15}} - {command.get_help()}'

        message_text += '\n```\nAvailable commands are different for each channel'

        await client.send_message(message.channel, message_text)
