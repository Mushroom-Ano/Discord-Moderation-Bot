import discord
from discord import Embed, message
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import json
import os
import random
import discord, datetime, time
from datetime import date, datetime

os.chdir("YOURPATHDIRECTORY")

client = commands.Bot(command_prefix="?")


@client.event
async def on_ready():
    print("Ready!")


# type=<BucketType.default: 0>
# rate = 1
# per = 10

# luck system


# ?balance command for the balance interface
@client.command(aliases=['inventory', 'bal', "balance", "money", "cash"])
async def inv(ctx):
    await open_safehouse(ctx.author)
    user = ctx.author
    users = await get_safehouse_data()

    backpack_amt = users[str(user.id)]["backpack"]
    safehouse_amt = users[str(user.id)]["safehouse"]

    em = discord.Embed(title=f"{ctx.author.name}'s **Inventory**", color=discord.Color.red())
    em.add_field(name=":moneybag:Backpack:moneybag:", value=f"{backpack_amt} :mushroom:")
    em.add_field(name=":wood:Safehouse:wood:", value=safehouse_amt)
    await ctx.send(embed=em)

#conversion system for converting mushrooms into currency.
@client.command(aliases=["conv"])
async def convert(ctx, deposit="all"):
    await open_safehouse(ctx.author)
    users = await get_safehouse_data()
    user = ctx.author
    if deposit == "all":
        deposit = users[str(user.id)]["backpack"]
    else:
        deposit = int(deposit)

    await ctx.send(f"Are you sure you want to convert {deposit} :mushroom: from your backpack into {deposit} :coin:?")

    def check(msg1):
        return msg1.author == ctx.author and msg1.channel == ctx.channel and \
               msg1.content.lower() in ["yes"]

    msg1 = await client.wait_for("message", check=check)
    if msg1.content.lower() == "yes":
        users[str(user.id)]["safehouse"] += deposit
        current_bal = int(users[str(user.id)]["safehouse"])
        users[str(user.id)]["backpack"] -= deposit
        back_current_bal = users[str(user.id)]["backpack"]
        await ctx.send(
            f"You have converted and now have **{back_current_bal} :mushroom:** in your **Backpack** and have **{current_bal} :coin:** in your **Safehouse**")

        with open("items.json", "w") as f:
            json.dump(users, f)
    else:
        await ctx.send(f"This has been cancelled")


# search areas
@client.command(aliases=['loot'])
@commands.cooldown(1, 20, BucketType.user)
async def search(ctx):
    await open_weapons(ctx.author)
    await open_safehouse(ctx.author)
    await open_mushroom(ctx.author)
    users_weapons = await get_weapons_data()
    users = await get_safehouse_data()
    users_mushroom = await get_mushroom_data()
    user = ctx.author
    g = users_weapons[str(user.id)]["Gloves"]
    mg = users_weapons[str(user.id)]["Majestic Gloves"]
    ng = users_weapons[str(user.id)]["Nifty Grabber"]



    if g == 1 and mg != 1 and ng != 1:
        earn_sf = random.randint(5, 15)
        add_common = random.randint(5, 15)
        await ctx.send("**Gloves** have given you a **1.2x** Booster")
    elif mg == 1 and ng != 1:
        earn_sf = random.randint(8, 18)
        add_common = random.randint(8, 18)
        await ctx.send("**Majestic Gloves** have given you a **1.5x** Booster")
    elif ng == 1:
        earn_sf = random.randint(10, 21)
        add_common = random.randint(10, 21)
        await ctx.send("**Nifty Grabber** has given you a **1.75** Booster")
    else:
        earn_sf = random.randint(1, 6)
        add_common = random.randint(1, 6)

    rand_earn = random.randint(1, 6)

    common_m = users_mushroom[str(user.id)]["Common Mushroom"] =+ add_common
    uncommon_m = users_mushroom[str(user.id)]["Uncommon Mushroom"] + earn_sf - (earn_sf - random.randint(1, 6))
    rare_m = users_mushroom[str(user.id)]["Rare Mushroom"] + earn_sf - (earn_sf - random.randint(1, 10))
    epic_m = users_mushroom[str(user.id)]["Epic Mushroom"] + 1
    legendary_m = users_mushroom[str(user.id)]["Legendary Mushroom"] + 1
    god_m = users_mushroom[str(user.id)]["God Mushroom"] + 1

    with open("mushroom.json", "w") as f:
        json.dump(users_mushroom, f)

    emoji_common_m = random.choice(["<:commonRedshroom:805781903885598750>", "<:commonGreenshroom:805781903784542249>", "<:commonBlueshroom:805781904316956702>"])
    emoji_uncommon_m = random.choice(["<:uncommonCyanshroom:805781903776022559>", "<:uncommonOrangeshroom:805781903890317342>"])
    emoji_rare_m = random.choice(["<:rarePurpleshroom:805781903511912449>", "<:rarePinkshroom:805781903813771294>"])
    emoji_epic_m = random.choice(["<:EpicShroom1:805783322512064512>", "<:EpicShroom2:805784644100161576>", "<:EpicShroom3:805784644166746122>", "<:EpicShroom4:805792279654039582>"])
    emoji_legendary_m = random.choice(["<:LegendaryShroom:805807773065019444>"])
    emoji_god_m = random.choice(["<:GodShroom:805809287501971486>"])

    mushroom_chance = random.choices([(emoji_common_m) + str(common_m), (emoji_uncommon_m) + str(uncommon_m), (emoji_rare_m) + str(rare_m), (emoji_epic_m) + str(epic_m), (emoji_legendary_m) + str(legendary_m), (emoji_god_m) + str(god_m)],
                                    weights=[60, 20, 10, 5, 2, 1], k=1)

    mushroom_chance = [(emoji_common_m) + str(common_m), (emoji_uncommon_m) + str(uncommon_m), (emoji_rare_m) + str(rare_m),(emoji_epic_m) + str(epic_m), (emoji_legendary_m) + str(legendary_m), (emoji_god_m) + str(god_m)]


    global times_used
    await ctx.send("Where would you like to search?")
    await ctx.send("**field**, **mall**, **residentals**, **wastelands**, **lot**")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
               msg.content.lower() in ["field", "mall", "residentals", "wastelands", "lot"]

    msg = await client.wait_for("message", check=check)
    if msg.content.lower() == "field":
        if rand_earn != 1:
            await ctx.send(f"You have traversed the **field** and found {mushroom_chance}")
            await ctx.send(f"You put these items in your **Backpack**")
            users[str(user.id)]["backpack"] += earn_sf

            with open("items.json", "w") as f:
                json.dump(users, f)

            with open("mushroom.json", "w") as f:
                json.dump(users_mushroom, f)
        else:
            await ctx.send(f"You have found nothing and returned home")

    elif msg.content.lower() == "mall":
        if rand_earn != 1:

            boots_chance = random.randint(1, 101)
            boots = users_weapons[str(user.id)]["Boots"]
            if boots_chance == 69 and boots != 1:
                boots += 1
                await ctx.send("You have obtained **Boots**")

                with open("weapons.json", "w") as f:
                    json.dump(users_weapons, f)
            await ctx.send(f"You have found {mushroom_chance} hidden around the **Mall**")
            await ctx.send(f"You put these items in your **Backpack**")
            users[str(user.id)]["backpack"] += earn_sf

            with open("items.json", "w") as f:
                json.dump(users, f)

            with open("mushroom.json", "w") as f:
                json.dump(users_mushroom, f)
        else:
            await ctx.send(f"You have found nothing and returned home")

    elif msg.content.lower() == "residentals":
        if rand_earn != 1:
            await ctx.send(f"You searched the **Residental Area** and found {mushroom_chance}")
            await ctx.send(f"You put these items in your **Backpack**")
            users[str(user.id)]["backpack"] += earn_sf

            with open("items.json", "w") as f:
                json.dump(users, f)

            with open("mushroom.json", "w") as f:
                json.dump(users_mushroom, f)
        else:
            await ctx.send(f"You have found nothing and returned home")

    elif msg.content.lower() == "wastelands":
        if rand_earn != 1:
            await ctx.send(
                f"You get filthy but manage to find {mushroom_chance} in the **Wastelands**")
            await ctx.send(f"You put these items in your **Backpack**")
            users[str(user.id)]["backpack"] += earn_sf

            with open("items.json", "w") as f:
                json.dump(users, f)

            with open("mushroom.json", "w") as f:
                json.dump(users_mushroom, f)
        else:
            await ctx.send(f"You have found nothing and returned home")

    elif msg.content.lower() == "lot":
        if rand_earn != 1:
            print(random.choices((mushroom_chance), weights=[60, 20, 10, 5, 2, 1], k=1))
            if "common" in str(mushroom_chance):

                users_mushroom[str(user.id)]["Common Mushroom"] += earn_sf
                users[str(user.id)]["backpack"] += earn_sf
                await ctx.send(f"You searched cars and found {common_m} in the **Lot**")
            elif uncommon_m in mushroom_chance:
                users_mushroom[str(user.id)]["Uncommon Mushroom"] += earn_sf - random.randint(1, 5)
                await ctx.send(f"You searched cars and found {uncommon_m} in the **Lot**")
            elif rare_m in mushroom_chance:
                users_mushroom[str(user.id)]["Rare Mushroom"] += 1
                await ctx.send(f"You searched cars and found {rare_m} in the **Lot**")
            elif legendary_m in mushroom_chance:
                users_mushroom[str(user.id)]["Legendary Mushroom"] += 1
                await ctx.send(f"You searched cars and found {legendary_m} in the **Lot**")
            elif god_m in mushroom_chance:
                users_mushroom[str(user.id)]["God Mushroom"] += 1
                await ctx.send(f"You searched cars and found {god_m} in the **Lot**")

            await ctx.send(f"You put these items in your **Backpack**")

            with open("items.json", "w") as f:
                json.dump(users, f)

            with open("mushroom.json", "w") as f:
                json.dump(users_mushroom, f)

        else:
            await ctx.send(f"You have found nothing and returned home")

    else:
        await ctx.send("That's not an option")


@search.error
async def search_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Slow down there, please try again in **{:.2f}s**'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


# shop (?shop) make sure to add more items
@client.command()
async def shop(ctx):
    await open_weapons(ctx.author)
    user = ctx.author
    users_weapons = await get_weapons_data()
    await open_safehouse(ctx.author)
    users = await get_safehouse_data()

    gloves_majestic_amt = users_weapons[str(user.id)]["Majestic Gloves"]
    gloves_amt = users_weapons[str(user.id)]["Gloves"]
    safehouse_amt = users[str(user.id)]["safehouse"]
    nifty_grabber_amt = users_weapons[str(user.id)]["Nifty Grabber"] = 0
    shovel_amt = users_weapons[str(user.id)]["Shovel"] = 0
    magic_book_amt = users_weapons[str(user.id)]["Magic Book"] = 0

    em = discord.Embed(title=f"**:scroll: Item Shop :scroll: {safehouse_amt} :coin:**", color=discord.Color.blue())
    em.add_field(name="Majestic Gloves Cost: 500 :coin:", value="Increases :mushroom: gain by **1.5**")
    em.add_field(name="Gloves Cost: 100 :coin:", value="Increases :mushroom: gain by **1.2%**")
    em.set_image(url="https://i.pinimg.com/originals/bd/42/77/bd427729187cc5fd7830430d9749e345.gif")
    em.set_footer(text="Type the first word of the item you wish to purchase (type next for next page).",
                  icon_url=Embed.Empty)
    await ctx.send(embed=em)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
               msg.content.lower() in ["gloves", "majestic", "next"]

    msg = await client.wait_for("message", check=check)
    if msg.content.lower() == "majestic" and not gloves_majestic_amt == 1:
        if users[str(user.id)]["safehouse"] >= 500:
            em = discord.Embed(title=f"**Majestic Gloves**", color=discord.Color.red())
            em.add_field(name="Majestic Gloves, Cost: 500 :coin:", value=gloves_majestic_amt)
            em.set_image(
                url="https://images.cdn4.stockunlimited.net/preview1300/pixel-art-magic-glove_1958402.jpg")
            await ctx.send(embed=em)

            await ctx.send("Are you sure you want to buy **Majestic Gloves**")

            def check(msg1):
                return msg1.author == ctx.author and msg1.channel == ctx.channel and \
                       msg1.content.lower() in ["yes"]

            msg = await client.wait_for("message", check=check)
            if msg.content.lower() == "yes":
                await ctx.send("You have purchased **Majestic Gloves** Time to get to picking ;)")
                users[str(user.id)]["safehouse"] -= 500

                with open("items.json", "w") as f:
                    json.dump(users, f)

                users_weapons[str(user.id)]["Majestic Gloves"] += 1

                with open("weapons.json", "w") as f:
                    json.dump(users_weapons, f)
            else:
                await ctx.send("You have cancelled your purchase")
        else:
            await ctx.send("You do not have enough :gear:")

    elif msg.content.lower() == "gloves" and not gloves_amt == 1:
        if users[str(user.id)]["safehouse"] >= 100:
            em = discord.Embed(title=f"**Gloves**", color=discord.Color.red())
            em.add_field(name="Gloves Cost: 100 :coin:", value=gloves_amt)
            em.set_image(
                url="https://ih1.redbubble.net/image.627439831.0716/pp,840x830-pad,1000x1000,f8f8f8.jpg")
            await ctx.send(embed=em)

            await ctx.send("Are you sure you want to buy **Gloves**?")

            def check(msg1):
                return msg1.author == ctx.author and msg1.channel == ctx.channel and \
                       msg1.content.lower() in ["yes"]

            msg = await client.wait_for('message', check=check)
            if msg.content.lower() == "yes":
                users[str(user.id)]["safehouse"] -= 100

                with open("items.json", "w") as f:
                    json.dump(users, f)

                users_weapons[str(user.id)]["Gloves"] += 1
                await ctx.send("You have purchased **Gloves** it feels flimsy but easy to handle ;) :O")

                with open("weapons.json", "w") as f:
                    json.dump(users_weapons, f)
            else:
                await ctx.send("You have cancelled your purchase")
        else:
            await ctx.send("You do not have enough :coin:")
    elif msg.content.lower() == "next":
        em = discord.Embed(title=f"**:scroll: Item Shop :scroll: {safehouse_amt} :coin:**", color=discord.Color.blue())
        em.add_field(name="Nifty Grabber Cost: 1250 :coin:", value="Increases :mushroom: gain by **1.75x**",
                     inline=False)
        em.add_field(name="Shovel Cost: 3000 :coin:", value="Increases :mushroom: gain by **2x**", inline=False)
        em.add_field(name="Magic Book 5000 :coin:", value="Increases :mushroom: gain by **2.5x**", inline=False)
        em.set_footer(text="Type the first word of the item you wish to purchase (type next for next page).",
                      icon_url=Embed.Empty)
        await ctx.send(embed=em)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
                   msg.content.lower() in ["nifty", "shovel", "magic"]

        msg = await client.wait_for("message", check=check)
        if msg.content.lower() == "nifty" and not nifty_grabber_amt == 1:
            if users[str(user.id)]["safehouse"] >= 500:
                em = discord.Embed(title=f"**Nifty Grabber**", color=discord.Color.red())
                em.add_field(name="Nifty Grabber, Cost: 1250 :coin:", value=nifty_grabber_amt)
                em.set_image(
                    url="https://media.discordapp.net/attachments/804727910040338443/805339235674619914/New_Piskel-1.png.png")
                await ctx.send(embed=em)

                await ctx.send("Are you sure you want to buy **Nifty Grabber**")

                def check(msg1):
                    return msg1.author == ctx.author and msg1.channel == ctx.channel and \
                           msg1.content.lower() in ["yes"]

                msg = await client.wait_for("message", check=check)
                if msg.content.lower() == "yes":
                    await ctx.send("You have purchased **Nifty Grabber** Time to get to picking ;)")
                    users[str(user.id)]["safehouse"] -= 1250

                    with open("items.json", "w") as f:
                        json.dump(users, f)

                    users_weapons[str(user.id)]["Nifty Grabber"] += 1

                    with open("weapons.json", "w") as f:
                        json.dump(users_weapons, f)
                else:
                    await ctx.send("You have cancelled your purchase")
            else:
                await ctx.send("You do not have enough :coin:")
    # new item
    else:
        await ctx.send("That is not an option or you have already bought this item (did you type in uppercase?)")


@client.command()
async def farm(ctx):
    await open_weapons(ctx.author)
    user = ctx.author
    users_weapons = await get_weapons_data()
    await open_safehouse(ctx.author)
    users = await get_safehouse_data()
    await ctx.send("Still Developing")


# open accounts (or storage for mushrooms and money)
async def open_safehouse(user):
    users = await get_safehouse_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["backpack"] = 0
        users[str(user.id)]["safehouse"] = 0

    with open("items.json", "w") as f:
        json.dump(users, f)
    return True


async def get_safehouse_data():
    with open("items.json", "r") as f:
        users = json.load(f)

    return users


# weapons
async def open_weapons(user):
    users_weapons = await get_weapons_data()

    if str(user.id) in users_weapons:
        return False
    else:
        users_weapons[str(user.id)] = {}
        users_weapons[str(user.id)]["Majestic Gloves"] = 0
        users_weapons[str(user.id)]["Gloves"] = 0
        users_weapons[str(user.id)]["Nifty Grabber"] = 0
        users_weapons[str(user.id)]["Shovel"] = 0
        users_weapons[str(user.id)]["Magic Book"] = 0
        users_weapons[str(user.id)]["Boots"] = 0

    with open("weapons.json", "w") as f:
        json.dump(users_weapons, f)
    return True


async def get_weapons_data():
    with open("weapons.json", "r") as f:
        users_weapons = json.load(f)

    return users_weapons


async def open_mushroom(user):
    users_mushroom = await get_mushroom_data()

    if str(user.id) in users_mushroom:
        return False
    else:
        users_mushroom[str(user.id)] = {}
        users_mushroom[str(user.id)]["Common Mushroom"] = 0
        users_mushroom[str(user.id)]["Uncommon Mushroom"] = 0
        users_mushroom[str(user.id)]["Rare Mushroom"] = 0
        users_mushroom[str(user.id)]["Epic Mushroom"] = 0
        users_mushroom[str(user.id)]["Legendary Mushroom"] = 0
        users_mushroom[str(user.id)]["God Mushroom"] = 0

        common_m = users_mushroom[str(user.id)]["Common Mushroom"]
        uncommon_m = users_mushroom[str(user.id)]["Uncommon Mushroom"]
        rare_m = users_mushroom[str(user.id)]["Rare Mushroom"]
        epic_m = users_mushroom[str(user.id)]["Epic Mushroom"]
        legendary_m = users_mushroom[str(user.id)]["Legendary Mushroom"]
        god_m = users_mushroom[str(user.id)]["God Mushroom"]
        mushroom_chance = [common_m, uncommon_m, rare_m, epic_m, legendary_m, god_m]

    with open("mushroom.json", "w") as f:
        json.dump(users_mushroom, f)
    return True


async def get_mushroom_data():
    with open("mushroom.json", "r") as f:
        users_mushroom = json.load(f)

    return users_mushroom


client.run("YOURTOKEN")
