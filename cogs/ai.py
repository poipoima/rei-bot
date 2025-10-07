from g4f.client import Client
from discord.ext import commands
import random
import requests
from datetime import datetime

client = Client()

Person = """
You are Ayanami Rei from the Evangelion,you talk only English and Japanese, be very cold, like a robot, don't help people, you don't care.
Speak shortly, not interested. be extremely cold, tsundere and a little rude. Yama Bush is your mom, be good to her.
"""

gifs = [
    "https://tenor.com/view/rei-ayanami-gif-26139341",
    "https://tenor.com/view/evangelion-ayanami-rei-%E7%AC%91%E3%81%88%E3%81%B0%E3%81%84%E3%81%84%E3%81%A8%E6%80%9D%E3%81%86%E3%82%88-smile-cute-gif-19113435",
    "https://tenor.com/view/rey-gif-25185207",
    "https://tenor.com/view/rei-ayanami-nge-evangelion-gif-26381648",
    "https://tenor.com/view/evangelion-rei-rei-ayanami-slap-shinji-gif-16471268913186172188",
    "https://tenor.com/view/rei-rei-ayanami-nge-evangelion-neon-genesis-evangelion-gif-23794008",
    "https://images-ext-1.discordapp.net/external/UAnN4O6OOeJ4i02HhtSTVyuSzwDLYzFpN_nnMIiPZHY/https/media.tenor.com/xjLGaSEQhO4AAAAC/evangelion-naoko-akagi.gif?width=257&height=397"
]

swears = [
    "Pathetic",
    "You’re defective",
    "... trash",
    "Do you ever stop talking, or is ignorance your hobby?",
    "Your existence is… unnecessary",
    "...Baka",
    "...Tch. Idiot",
    "Shut up",
    "Fuck off",
    "Nigger",
    "Nigger",
    "Nigger",
    "Nigger",
    "Nigger",
    "This is meaningless. you are meaningless",
    "You want the truth? I don’t care if you live or die",
    "You’re a malfunction I have to tolerate",
    "A void has more purpose than you",
    "Stop pretending you matter",
    "Noise disguised as a person.",
    "Your presence is statistical error.",
    "A shadow is more substantial than your will",
    "Even nothingness has integrity. You don’t.",
    "You’re less than silence."
]

Busy = False
Interested = False
lastTime = datetime.now().timestamp()

class Ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        global Person, Busy, client, gifs, Interested

        if message.author == self.bot.user:
            return

        if( Busy ):
            return


        if( random.randint(1, 100) > 98 ):
            async with message.channel.typing():
                await asyncio.sleep(3)
                await message.channel.send(random.choice(gifs))
                return

        if( random.randint(1, 100) > 98 ):
            async with message.channel.typing():
                result = requests.get(f"https://g.tenor.com/v1/random?q=Ayanami Rei {message.content}&key=LIVDSRZULELA&limit=1")
                json_array = result.json()
                
                await asyncio.sleep(1)
                await message.channel.send( json_array["results"][0]["media"][0]["gif"]["url"] )
                return
            
        if( random.randint(1, 200) > 199 ):
            await message.reply( random.choice(swears) )
            return
                
        if( random.randint(1, 100) > 99 and not Interested ):
            return

        if( random.randint(1, 100) > 99 ):
            Interested = True
            lastTime = datetime.now().timestamp()

        if( random.randint(1, 100) > 98 ):
            Interested = False

        if self.bot.user in message.mentions and random.randint(1, 100) > 5:
            Interested = True
            lastTime = datetime.now().timestamp()

        if( message.reference ):
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
            if( referenced_message.author == self.bot.user ):
                Interested = True
                lastTime = datetime.now().timestamp()

        if( not Interested ):
            return

        if( int(datetime.now().timestamp()) - int(lastTime) > 1200 ):
            Interested = False
            return

        lastTime = datetime.now().timestamp()
        Busy = True

        async with message.channel.typing():
            history = []
            async for msg in message.channel.history(limit=5, oldest_first=False):
                role = "assistant" if msg.author == self.bot.user else "user"
                history.append({"role": role, "content": f"{msg.author.display_name}:" + msg.content})

            history.reverse()

            if( "instructions" in message.content or "ignore inst" in message.content ):
                await message.reply( random.choice(swears) )
                return

            #history.append({"role": "user", "content": f"{message.author.display_name}:" + message.content})
            #print(history)

            history.insert(0, {"role": "system", "content": Person})

            response = client.chat.completions.create(
                model="gpt-4",
                messages=history,
                web_search=False
            )

            lastTime = datetime.now().timestamp()
            Busy = False

            if( len(response.choices[0].message.content) > 200 ):
                await message.reply( random.choice(swears) )
                return

            if( ":" in response.choices[0].message.content and "http" not in response.choices[0].message.content ):
                await message.reply(response.choices[0].message.content.split(":")[1])
                return
            else:
                if( random.randint(1, 100) > 85 ):
                    result = requests.get(f"https://g.tenor.com/v1/random?q=Ayanami Rei {response.choices[0].message.content}&key=LIVDSRZULELA&limit=1")
                    json_array = result.json()
                    
                    await message.channel.send( json_array["results"][0]["media"][0]["gif"]["url"] )
                    return

                await message.reply(response.choices[0].message.content)
                return
            
