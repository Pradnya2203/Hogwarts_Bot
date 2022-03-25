
import nextcord
import os
import asyncio

from numpy import place
from words import word
from nextcord.ext import commands
from googleapiclient.discovery import build

from PIL import Image
import requests
from io import BytesIO
import random
from spells import spell

client=commands.Bot(command_prefix="/")
api_key = "AIzaSyB-nURmOoo-uL6gJUuodD26Tq71DJmv8ag"
client.remove_command("help")

@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency*1000)}ms")



@client.command(aliases=["show"])
async def showpic(ctx,*,search):
    ran = random.randint(0,9)
    resource = build("customsearch", "v1", developerKey =  api_key).cse()
    result = resource.list(q=f"{search}", cx="78dcaf05236f30018",searchType ="image").execute()
    url =  result["items"][ran]["link"]
    embed1 = nextcord.Embed(title= f"Here's your image ({search.title()})")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)



@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=5):
    await ctx.channel.purge(limit=amount+1)

@client.command()
async def welcome(ctx,user: nextcord.Member = None):
    if user == None:
        user= ctx.author
    kitty = Image.open("hogwarts_hp.jpg")
    asset = user.avatar.replace(size=128)
    data = BytesIO(await asset.read())
    pfp= Image.open(data)

    pfp = pfp.resize((85,85))
    kitty.paste(pfp, (56,113))
    kitty.save("profile.jpg")
    await ctx.send(file= nextcord.File("profile.jpg"))



@client.command()
async def help(ctx):
    em= nextcord.Embed(title= "Hogwarts Guide", description = "Use the prefix / to make use of the following commands", color= ctx.author.color)
    em.add_field(name="rules",value="Mentions the rules of the server ")   
    em.add_field(name="welcome",value="Welcomes you to Hogwarts")
    em.add_field(name="hogwarts_view",value="Take a glimse at Hogwarts")
    em.add_field(name="house",value="Select your house ")
    em.add_field(name= "identity", value= "Gives information about a student")
    em.add_field(name="show" , value="Searches up a random image on internet")
    em.add_field(name="ping",value="Mentions the time required to pong ")
    em.add_field(name="class_timer",value=" Countdowns the time in minutes and seconds ")
    em.add_field(name="meme",value="Shows up a random meme")
    em.add_field(name="clear",value="clears that many number of previous messages ")
    em.add_field(name="poll",value="Can use it to make polls on the server")   
    em.add_field(name="spell_game",value="Shows a random spell ")
    await ctx.send(embed=em)
    


@client.command()
async def rules(ctx):
    em= nextcord.Embed(title= "Rules at Hogwarts", description = "The rules of this wizarding school are: ", color= ctx.author.color)
    em.add_field(name= "1: ", value= "Students Who Became Animagi Must Register Or Face Jail Time\n")
    em.add_field(name="2: " , value="Do Not Violate The Laws Of Nature For Recreational Use\n")
    em.add_field(name="3: ",value="Even At Hogwarts, Cursed Objects Are Banned\n ")
    em.add_field(name="4: ",value="Fluffy's Room Is Off-Limits\n ")
    em.add_field(name="5: ",value="The Use And Brewing Of Dangerous Potions Is Forbidden\n")
    em.add_field(name="6: ",value="It Is Forbidden To Cheat By Way Of Magic")
    em.add_field(name="7: ",value="It Is Forbidden To Approach The Whomping Willow")
    em.add_field(name="8: ",value="Butterbeer Is Not Allowed On School Grounds ")
    em.add_field(name="9: ",value="Pointed Hats And Proper Attire Are Required")
    em.add_field(name="10: ",value="No Reading From The Restricted Section")
    em.add_field(name="11: ",value="No Entering Other House Dormitories")
    em.add_field(name="12: ",value="Do Not Enter The Forbidden Forest")
    await ctx.send(embed=em)
  

@client.command(aliases=["user","info"])
async def identity(ctx, member: nextcord.Member):
    embed=nextcord.Embed(title=member.name , description= member.mention, color = nextcord.Colour.dark_purple())
    embed.add_field(name = "Roll Number: " , value= member.id , inline=True)
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(icon_url= ctx.author.avatar.url , text= f"Assigned by proffessor Albus Dumbledore")
    await ctx.send(embed=embed)

@client.command()
async def class_timer(ctx,minutes,seconds):
    try:
        minuteint=int(minutes)
        secondint=int(seconds)
      
        if secondint <=0:
            await ctx.send("Choose a valid time")
            raise BaseException

        while True:
            while True:
                secondint -= 1
                if secondint==0:
                    minuteint -=1
                    secondint +=59
                    break
                await asyncio.sleep(1)
            if minuteint<0:
                
                break
 
            
        await ctx.send(f"{ctx.author.mention} Your class is over")
        await ctx.send("https://i.pinimg.com/originals/65/9d/b5/659db59cb50f22096f3f30ad1ef3d223.jpg")
    except ValueError:
        await ctx.send("You must enter an integer")

@client.command()
async def meme(ctx):
    r =requests.get("https://memes.blademaker.tv/api?lang=en")
    res= r.json()
    title=res["title"]
    ups = res["ups"]
    downs=res["downs"]
    sub=res["subreddit"]
    m = nextcord.Embed(title = f"{title}\nSubreddit: {sub}" )
    m.set_image(url= res["image"])
    m.set_footer(text=f"👍:{ups} 👎:{downs}")
    await ctx.send(embed=m)


class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Confirmed", ephemeral=True)
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.grey)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Cancelled", ephemeral=True)
        self.value = False
        self.stop()

@client.command()
async def poll(ctx,*,message):
    view = Confirm()
    await ctx.send(f"{message}", view=view)

    await view.wait()
    yes = 0
    no =0
    if not view.value == None:
        print("Timed Out")
    if view.value == True:
        yes+=1
        print("Confirmed")
    if view.value == False:
        no+=1
        print("Cancelled")     
    
    em=nextcord.Embed(title="Poll" , description="The result of poll is", color = nextcord.Colour.dark_purple())
    em.add_field(name="For",value= f"{yes}")
    em.add_field(name="Against",value= f"{no}")

    await ctx.send(embed=em)

@client.command()
async def hogwarts_view(ctx):
    embed=nextcord.Embed(title="Click It", url="https://youtu.be/xBAeOTHtZVg")
    await ctx.send(embed=embed)

class Dropdown(nextcord.ui.Select):
    def __init__(self):
        selectOptions=[
            nextcord.SelectOption(label="GRYFFIDOR", description= "Brave, Nerve, Athletic, Courage, Chivalry and Daring"),
            nextcord.SelectOption(label="SLYTHERIN", description= "Resourcefulness, Cunning, Ambition, Determination, Leadership and Cleverness"),
            nextcord.SelectOption(label="HUFFLEPUFF", description= "Dedication, Hard working, Fairness, Patience, Kindness, Loyalty and Tolerance"),
            nextcord.SelectOption(label="RAVENCLAW", description= "Intelligence, Wit, Wisdom, Creativity, Acceptance, Originality and Individuality")

        ]
        super().__init__(placeholder="Select your house",min_values=1,max_values=1,options=selectOptions)

    async def callback(self,interaction: nextcord.Interaction):
        await interaction.response.send_message(f"You are entering {self.values[0]}")

class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())


@client.command()
async def house(ctx):
    view=DropdownView()
    await ctx.send("Choose your House",view=view)


@client.command()
async def spell_game(ctx):
    Spell= random.choice(spell)
    await ctx.send(Spell)



client.run("OTUyODc1OTU0NDQxNjk1MjYy.Yi8Y4w.d7bIfBTy8NljUWNaq1K1cb4QaAM")