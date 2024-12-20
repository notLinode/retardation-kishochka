import discord
import get_ai_response as ai
import os
import random

# Retrieve sensitive information from an unlisted file
TOKEN: str
AKASH_API_KEY: str

with open("tokens.txt", "r") as file:
    temp = file.read().splitlines()
    TOKEN = temp[0]
    AKASH_API_KEY = temp[1]

# Declare the bot
intents = discord.Intents.default()
intents.guild_typing = True
intents.message_content = True

client = discord.Client(intents=intents)

#Declare global variables and constants
SETTING_MESSAGE_INTERVAL_MIN: int = 1
SETTING_MESSAGE_INTERVAL_MAX: int = 25
setting_message_interval: int = 1
setting_message_interval_is_random: bool = True
message_interval_random: int = 4

SETTING_OWN_MESSAGE_MEMORY_MIN: int = 1
SETTING_OWN_MESSAGE_MEMORY_MAX: int = 10
setting_own_message_memory: int = 1
recent_messages: list[str] = []
stylized_bot_messages: list[str] = []

banned_automsg_channels: list[int]

try:
    with open("stop-list.txt", "r") as file:
        banned_automsg_channels = [int(line) for line in file.readlines()]
except FileNotFoundError:
    with open("stop-list.txt", "w"):
        banned_automsg_channels = []

# Print a message when the bot is up
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Declare commands
@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    
    global recent_messages
    global stylized_bot_messages
    global setting_message_interval_is_random
    global message_interval_random

    if message.content.startswith("%prompt"):
        async with message.channel.typing():
            ai_response: str = ai.get_response(AKASH_API_KEY, message.content[8:])

            while len(ai_response) > 2000:
                await message.channel.send(ai_response[:2000])
                ai_response = ai_response[2000:]

            await message.channel.send(ai_response)
        return
    
    if message.content.startswith("%set-message-interval"):
        async with message.channel.typing():
            interval_str: str = message.content[22:].lower()
            
            if not interval_str.isnumeric() and interval_str != "random":
                await message.channel.send(f":prohibited: Неправильное значение интервала между сообщениями бота. Значение должно быть либо числом от `{SETTING_MESSAGE_INTERVAL_MIN}` до `{SETTING_MESSAGE_INTERVAL_MAX}`, либо `random`.")
                return

            if interval_str == "random":
                setting_message_interval_is_random = True
                message_interval_random = int(random.random() * 10) + 1

                await message.channel.send(f":white_check_mark: Интервал между сообщениями бота будет случайным для каждого сообщения.")
                return
            
            interval: int = int(interval_str)

            if interval < SETTING_MESSAGE_INTERVAL_MIN or interval > SETTING_MESSAGE_INTERVAL_MAX:
                await message.channel.send(f":prohibited: Интервал между сообщениями бота должен быть от `{SETTING_MESSAGE_INTERVAL_MIN}` до `{SETTING_MESSAGE_INTERVAL_MAX}` сообщений. Вы попытались установить: `{interval}`.")
                return

            global setting_message_interval
            setting_message_interval = interval
            setting_message_interval_is_random = False
            
            await message.channel.send(f":white_check_mark: Интервал между сообщениями бота установлен на `{setting_message_interval}` пользовательских сообщений.")
        return
    
    if message.content.startswith("%set-own-message-memory"):
        async with message.channel.typing():
            memory: int = int(message.content[24:])

            if memory < SETTING_OWN_MESSAGE_MEMORY_MIN or memory > SETTING_OWN_MESSAGE_MEMORY_MAX:
                await message.channel.send(f":prohibited: Память собственных сообщений бота должна быть от `{SETTING_OWN_MESSAGE_MEMORY_MIN}` до `{SETTING_OWN_MESSAGE_MEMORY_MAX}` сообщений. Вы попытались установить: `{memory}`.")
                return

            global setting_own_message_memory
            setting_own_message_memory = memory

            await message.channel.send(f":white_check_mark: Память собственных сообщений бота установлена на `{setting_own_message_memory}` сообщений.")
        return
    
    if message.content.startswith("%clear-memory"):
        async with message.channel.typing():
            recent_messages.clear()
            stylized_bot_messages.clear()
            await message.channel.send(f":white_check_mark: я всё заббыл нахуй")
        return        

    if message.content.startswith('%ping'):
        await message.channel.send('pong')
        return
    
    if message.content.startswith('%help'):
        async with message.channel.typing():
            help_msg: str = "```"
            help_msg += "\n%prompt [Сообщение: str] - обратиться к Llama 3.1 405B.\n"
            help_msg += "\n%set-message-interval [Интервал: int | random] - поставить количество пользовательских сообщений, после которого бот сам что-то напишет.\n"
            help_msg += "\n%set-own-message-memory [Память: int] - поставить количество собственных сообщений бота, которые он запомнит и учтёт при написании следующего своего сообщения.\n"
            help_msg += "\n%clear-memory - очищает память бота от своих и пользовательских сообщений.\n"
            help_msg += "\n%stop - запрещает боту автоматически отправлять сообщения в данный канал.\n"
            help_msg += "\n%ping - pong.\n"
            help_msg += "```"

            await message.channel.send(help_msg)
        return
    
    if message.content.startswith(("%stop", ";stop 2")):
        channel_id: int = message.channel.id

        with open("stop-list.txt", "r+") as file:
            if channel_id not in banned_automsg_channels:
                banned_automsg_channels.append(channel_id)
                await message.reply("извините я больше не буду сюда писать")

                file.seek(0, 2)
                file.write(str(channel_id) + "\n")
            else:
                banned_automsg_channels.remove(channel_id)
                await message.reply("ок я снова буду сюда писать")
                
                lines: list[str] = file.readlines()
                lines.remove(str(channel_id) + "\n")
                file.close()
                with open("stop-list.txt", "w") as file:
                    file.writelines(lines)

    if message.channel.id in banned_automsg_channels:
        return

    recent_messages.append(message.content)

    is_mentioned: bool = client.user in message.mentions
    is_mentioned_directly: bool = "мегаинвалид" in message.content.lower()

    if setting_message_interval_is_random:
        is_time_to_automessage: bool = message_interval_random <= 0
        message_interval_random = int(random.random() * 10) + 1 if is_time_to_automessage else message_interval_random - 1
    else:
        is_time_to_automessage: bool = len(recent_messages) >= setting_message_interval

    if is_mentioned or is_mentioned_directly or is_time_to_automessage:
        async with message.channel.typing():
            automessage: str = await ai.generate_automessage(AKASH_API_KEY, recent_messages, stylized_bot_messages)
            await message.channel.send(automessage)

            recent_messages.clear()


# Run the bot
client.run(TOKEN)
