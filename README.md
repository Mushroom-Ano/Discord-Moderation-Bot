# Mushbot

Mushbot is a Discord bot designed for an interactive and fun experience involving gathering and managing virtual mushrooms and currency. Users can perform various actions like checking their balance, converting mushrooms to currency, searching for mushrooms in different areas, purchasing items from the shop, and more.

## Features

- **Balance and Inventory**: Check your current mushroom and coin balance.
- **Conversion System**: Convert mushrooms into coins.
- **Search Areas**: Search different areas for mushrooms with varying chances and rewards.
- **Item Shop**: Purchase items to boost your mushroom gathering efficiency.
- **Cooldown Management**: Manage command cooldowns to prevent spamming.

## Commands

- `?balance` or `?inv`: Displays the user's current inventory and balance.
- `?convert [amount]`: Converts mushrooms from the user's backpack into coins.
- `?search`: Searches different areas for mushrooms with a cooldown period.
- `?shop`: Displays the item shop where users can purchase items.
- `?farm`: (Under Development) Placeholder for farming functionality.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Mushbot.git
    cd Mushbot
    ```

2. Install the required dependencies:
    ```bash
    pip install discord.py
    ```

3. Create your `items.json`, `weapons.json`, and `mushroom.json` files in the root directory:
    ```json
    {
      "user_id": {
        "backpack": 0,
        "safehouse": 0
      }
    }
    ```

    ```json
    {
      "user_id": {
        "Majestic Gloves": 0,
        "Gloves": 0,
        "Nifty Grabber": 0,
        "Shovel": 0,
        "Magic Book": 0,
        "Boots": 0
      }
    }
    ```

    ```json
    {
      "user_id": {
        "Common Mushroom": 0,
        "Uncommon Mushroom": 0,
        "Rare Mushroom": 0,
        "Epic Mushroom": 0,
        "Legendary Mushroom": 0,
        "God Mushroom": 0
      }
    }
    ```

4. Replace `DISCORD_KEY` with your actual Discord bot token in the `client.run` statement.

5. Run the bot:
    ```bash
    python bot.py
    ```

## Code

```python
import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import json
import os
import random
from datetime import datetime

os.chdir("YOURPATHDIR")

client = commands.Bot(command_prefix="?")

@client.event
async def on_ready():
    print("Ready!")

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

    common_m = users_mushroom[str(user.id)]["Common Mushroom"] += add_common
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

    global times_used
    await ctx.send("Where would you like to search?")
    await ctx.send("**field**, **mall**, **residentals**, **wastelands**, **lot**")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
               msg.content.lower() in ["field", "mall", "residentals", "wastelands", "lot"]

    msg = await client.wait_for("message", check=check)
