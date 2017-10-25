import discord

from command import Command
from module import Module


class HelpModule(Module):
    def __init__(self):
        super().__init__('helpmodule', 'Module for printing help for modules', [], [
            Command('help', 'show available commands', self.help_handler)
        ], global_module=True)

    async def help_handler(self, client: discord.Client, message: discord.Message, arguments: str):
        modules = client.get_loaded_modules(message.author, message.channel)

        commands = []
        for module in modules:
            commands.extend(module.get_commands(message.author, message.channel))

        if len(commands) < 1:
            await client.send_message(message.channel, "No commands available in this channel")
            return

        message_text = '```\nAvailable commands:'

        for command in commands:
            message_text += f'\n\t{command.get_name():{15}} - {command.get_help()}'

        message_text += '\n```'

        await client.send_message(message.channel, message_text)


