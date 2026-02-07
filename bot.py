import discord
import os
import requests
from gtts import gTTS

TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)


def ask_ai(text):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system",
             "content": "You are ZENO AI on Discord call. Hinglish, short 1-2 line replies like real talk."},
            {"role": "user", "content": text}
        ]
    }

    r = requests.post(url, headers=headers, json=data)

    try:
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "Network thoda slow hai"
@client.event
async def on_ready():
    print("ZENO VC AI ONLINE")


@client.event
async def on_message(message):

    if message.content == "!join":
        if message.author.voice:
            channel = message.author.voice.channel
            await channel.connect()
            await message.channel.send("ZENO AI joined VC 👍")
        else:
            await message.channel.send("Pehle voice channel join karo")

    if message.content == "!leave":
        if message.guild.voice_client:
            await message.guild.voice_client.disconnect()


async def speak(vc, text):
    tts = gTTS(text, lang='en')
    tts.save("reply.mp3")
    vc.play(discord.FFmpegPCMAudio("reply.mp3"))


@client.event
async def on_voice_state_update(member, before, after):

    vc = member.guild.voice_client
    if not vc:
        return

    # Demo trigger – real stream part we add next
    reply = ask_ai("hello")
    await speak(vc, reply)


client.run(TOKEN)
