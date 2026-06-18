import discord
import json
import re
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

def load_config():
    with open("words.json", "r", encoding="utf-8") as f:
        return json.load(f)

def contains_spoiler(text, word):
    pattern = r'\|\|[^|]*' + re.escape(word) + r'[^|]*\|\|'
    return bool(re.search(pattern, text, re.IGNORECASE))

def find_trigger_word(text, trigger_words):
    for word in trigger_words:
        if word.lower() in text.lower() and not contains_spoiler(text, word):
            return word
    return None

@client.event
async def on_ready():
    print(f"Bot connecté : {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    config = load_config()
    trigger_words = config.get("trigger_words", [])
    excluded_channels = config.get("excluded_channels", [])

    if message.channel.id in excluded_channels:
        return

    triggered_word = find_trigger_word(message.content, trigger_words)

    if triggered_word:
        await message.add_reaction("⚠️")

        message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"

        dm_message = f"""**🔔 Petite notification bienveillante**

Bonjour ! Ce message automatique t'est envoyé suite à ton message dans **{message.guild.name}**. Certains termes utilisés peuvent être sensibles pour d'autres membres : `{triggered_word}`.

**Pas d'inquiétude !**
Ceci n'est pas un avertissement (warn). Ton compte n'est pas pénalisé. C'est une simple notification informative pour le bien-être de la communauté.

**Pourquoi ce message ?**
- Pour t'aider à prendre conscience de l'impact de certains mots.
- Pour t'encourager à utiliser `||des spoilers||` sur les sujets sensibles.
- Pour garder cet espace sûr et accueillant pour tout le monde."""

        view = discord.ui.View()
        button = discord.ui.Button(
            label="Consulter ton message",
            url=message_link,
            style=discord.ButtonStyle.link
        )
        view.add_item(button)

        try:
            await message.author.send(dm_message, view=view)
        except discord.Forbidden:
            pass  # La personne a les DMs fermés

client.run(os.environ["DISCORD_TOKEN"])
