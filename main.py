import asyncio
import os
import uuid
import discord
from discord.ext import commands
from pymongo import MongoClient
from forex_python.converter import CurrencyCodes
from datetime import datetime

c = CurrencyCodes()
cluster = MongoClient(os.environ['CLUSTER'])

db = cluster["MeowShop"]
serv = db["Server"]
carts = db["Carts"]
prods = db["Products"]
orders = db["Orders"]
prefix = db["Prefix"]


async def get_prefix(bot, message):
    if isinstance(message.channel, discord.DMChannel):
        return "$"
    elif isinstance(message.channel, discord.TextChannel):
        guild_id = message.guild.id
        # you can do something here with the guild obj, open a file and return something different per guild
        custom_prefix = prefix.find_one({"_id": guild_id})["prefix"]
        return custom_prefix


intents = discord.Intents.default()
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.remove_command('help')

def listToString(s):
    str1 = ""

    for element in s:
        str1 += (element + " ")

        # return string
    return str1


def printOrder(title, description, footer, orderCheck, servInf):
    embedVar = discord.Embed(title=title, description=description, color=0xffcccc)
    items = orderCheck["items"]
    for key in items:
        value = "Price: `" + servInf["currency"] + " " + str(items[key][0]) + "` Quantity: `" \
                + str(items[key][1]) + "` Item ID: `" + items[key][2] + "`\nDescription:\n" + items[key][3]
        embedVar.add_field(name=key, value=value, inline=False)
    embedVar.add_field(name="Sub-Total",
                       value="`" + servInf["currency"] + " " + str(orderCheck["subtotal"]) + "`",
                       inline=False)
    embedVar.add_field(name="Shipping",
                       value="`" + servInf["currency"] + " " + str(orderCheck["shipping"]) + "`",
                       inline=False)
    embedVar.add_field(name="Total", value="`" + servInf["currency"] + " " + str(orderCheck["total"]) + "`",
                       inline=False)
    embedVar.set_footer(text=footer)
    return embedVar


@bot.event
async def on_ready():
    print("bot ready")


@bot.event
async def on_reaction_add(self, payload):
    pass


@bot.event
async def on_guild_join(guild):
    default_prefix = {"_id": guild.id, "prefix": "$"}
    prefix.insert_one(default_prefix)


@bot.command()
@commands.guild_only()
async def setprefix(ctx, new_prefix):
    old_prefix = prefix.find_one({"_id": ctx.guild.id})["prefix"]
    prefix.find_one_and_update({"_id": ctx.guild.id}, {"$set": {"prefix": new_prefix}})
    embedVar = discord.Embed(title="Prefix updated",
                             description="Old prefix: `" + old_prefix + "`\nNew prefix: `" + new_prefix + "`",
                             color=0xffcccc)
    await ctx.send(embed=embedVar)


@bot.command()
@commands.guild_only()
async def setname(ctx, item_id, *name):
    name = listToString(name)
    result = prods.find_one_and_update({"_id": item_id, "serverID": ctx.guild.id}, {"$set": {"name": name}})
    embedVar = discord.Embed(title="Product name change.",
                             description="Name change for item: `" + item_id + "`",
                             color=0xffcccc)
    if result is None:
        embedVar.add_field(name="Item not found.", value="The item with the given item ID does not exist", inline=False)
    else:
        embedVar.add_field(name="Name change successful",
                           value="Changed item name from **" + result["name"] + "** to **" + name + "**", inline=False)
    await ctx.send(embed=embedVar)


@bot.command()
@commands.guild_only()
async def setdesc(ctx, item_id, *desc):
    desc = listToString(desc)
    result = prods.find_one_and_update({"_id": item_id, "serverID": ctx.guild.id}, {"$set": {"desc": desc}})
    embedVar = discord.Embed(title="Product description change.",
                             description="Description change for item: `" + item_id + "`",
                             color=0xffcccc)
    if result is None:
        embedVar.add_field(name="Item not found.", value="The item with the given item ID does not exist", inline=False)
    else:
        embedVar.add_field(name="Description change successful",
                           value="Changed item description from **" + result["desc"] + "** to **" + desc + "**", inline=False)
    await ctx.send(embed=embedVar)


@bot.command()
@commands.guild_only()
async def setcount(ctx, item_id, count):
    count = int(count)
    embedVar = discord.Embed(title="Product Count change.",
                             description="Count change for item: `" + item_id + "`",
                             color=0xffcccc)
    if count < 0:
        embedVar.add_field(name="Invalid Count",
                           value="Count must be greater than or equal to 0!",
                           inline=False)
        await ctx.send(embed=embedVar)
    else:
        result = prods.find_one_and_update({"_id": item_id, "serverID": ctx.guild.id}, {"$set": {"count": count}})

        if result is None:
            embedVar.add_field(name="Item not found.", value="The item with the given item ID does not exist",
                               inline=False)
        else:
            embedVar.add_field(name="Count change successful",
                               value="Changed item Count from **" + str(result["count"]) + "** to **" + str(count) + "**",
                               inline=False)
        await ctx.send(embed=embedVar)


@bot.command()
@commands.guild_only()
async def setprice(ctx, item_id, price):
    price = int(price)
    embedVar = discord.Embed(title="Product Count change.",
                             description="Count change for item: `" + item_id + "`",
                             color=0xffcccc)
    if price < 0:
        embedVar.add_field(name="Invalid Price",
                           value="P must be greater than or equal to 0!",
                           inline=False)
        await ctx.send(embed=embedVar)
    else:
        result = prods.find_one_and_update({"_id": item_id, "serverID": ctx.guild.id}, {"$set": {"price": price}})

        if result is None:
            embedVar.add_field(name="Item not found.", value="The item with the given item ID does not exist",
                               inline=False)
        else:
            embedVar.add_field(name="Price change successful",
                               value="Changed item price from **" + str(result["price"]) + "** to **" + str(price) + "**",
                               inline=False)
        await ctx.send(embed=embedVar)


@bot.command()
async def help(ctx):
    embedVar = discord.Embed(title="Help", description="Command List.", color=0xffcccc)
    embedVar.add_field(name="**Owner commands**", value="Commands for server owner. Guild only commands.", inline=False)
    embedVar.add_field(name="`setup <currency code> <shipping cost>`",
                       value="Setup server shop. Must be used before shop is initialized.", inline=False)
    embedVar.add_field(name="`setprefix <new prefix>`",
                       value="Setup server prefix. Default prefix and DM prefix is `$`.", inline=False)
    embedVar.add_field(name="`confirm <order code>`",
                       value="Confirm order has been paid. Use after payment is received.", inline=False)
    embedVar.add_field(name="`refund <order code>`",
                       value="Confirm refund request. Use when payment has been refunded to the user.",
                       inline=False)
    embedVar.add_field(name="`addp <item name> <price> <count> <*desciption>`", value="Add a product for sale.",
                       inline=False)
    embedVar.add_field(name="`delp <item id>`", value="Delete a product.", inline=False)
    embedVar.add_field(name="`setname <item id> <new name>`",
                       value="Set item name. Can be used to change item name to multiple words.", inline=False)
    embedVar.add_field(name="`setdesc <item id> <new description>`", value="Set item description.", inline=False)
    embedVar.add_field(name="`setcount <item id> <new count>`", value="Set item count.", inline=False)
    embedVar.add_field(name="`setprice <item id> <new price>`", value="Set item price.", inline=False)
    embedVar.add_field(name="`setcurrency <currency code>`", value="Set shop currency.", inline=False)
    embedVar.add_field(name="`setshipping <shipping cost>`", value="Set shop shipping price.", inline=False)
    embedVar.add_field(name="`addpayment <payment type> <payment instruction>`", value="Add payment option.",
                       inline=False)
    embedVar.add_field(name="`delpayment <payment type>`", value="Delete payment option.", inline=False)
    embedVar.add_field(name="`pending`", value="List unconfirmed orders.\n\n", inline=False)

    embedVar.add_field(name="**User commands**",
                       value="Commands for buyer. DM only commands. `products` can be used within the server.",
                       inline=False)
    embedVar.add_field(name="`info <server code>`", value="Server shop info.", inline=False)
    embedVar.add_field(name="`products <server code>`", value="Show products for sale.", inline=False)
    embedVar.add_field(name="`payments <server code>`", value="Show payment methods.", inline=False)
    embedVar.add_field(name="`add <server code> <item id> <quantity>`", value="Add an item to your cart.", inline=False)
    embedVar.add_field(name="`remove <server code> <item id> <quantity>`", value="Remove items from your cart.", inline=False)
    embedVar.add_field(name="`cart <server code>`", value="Show cart.", inline=False)
    embedVar.add_field(name="`checkout <server code>`", value="Checkout cart.", inline=False)
    embedVar.add_field(name="`cancel <order code>`", value="Cancel your order. Use when payment has not been sent yet.", inline=False)
    embedVar.add_field(name="`rrefund <order code>`", value="Request a refund. Use when payment is sent.", inline=False)

    await ctx.send(embed=embedVar)


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def setup(ctx, currCode: str, shippingCost: int):
    embedVar = discord.Embed(title="Setup", description="Shop setup", color=0xffcccc)
    item = serv.find_one({"_id": ctx.guild.id})
    currency = c.get_symbol(currCode)
    manager = [ctx.guild.owner]
    if item is None:
        if currency is not None:
            searchCode = uuid.uuid4().hex[:8]
            newSet = {"_id": ctx.guild.id, "currency": currCode, "shippingCost": shippingCost, "searchCode": searchCode
                , "payments": dict(), "manager": manager}
            serv.insert_one(newSet)
            embedVar.add_field(name="Updated Shop",
                               value="Currency: " + currCode + "\nShipping Cost: " + str(shippingCost)
                                     + "\nSearch Code: " + searchCode,
                               inline=False)
        elif currency is None:
            embedVar.add_field(name="Invalid Currency", value="Enter a currency found in ISO 4217.", inline=True)
    else:
        updatedServ = serv.find_one_and_update({"_id": ctx.guild.id}, {
            "$set": {"_id": ctx.guild.id, "currency": currCode, "shippingCost": shippingCost}})
        embedVar.add_field(name="Updated Shop", value="Currency: " + currCode + "\nShipping Cost: " + str(shippingCost)
                                                      + "\nSearch Code: " + item["searchCode"],
                           inline=False)
    await ctx.send(embed=embedVar)


# currently unusable
@bot.command()
@commands.is_owner()
@commands.guild_only()
async def addmgr(ctx, role):
    servInf = serv.find_one({"_id": ctx.guild.id})
    embedVar = discord.Embed(title="Add manager", description="Add shop manager", color=0xffcccc)
    guildData = bot.get_guild(servInf["_id"])

    if servInf is None:
        embedVar.add_field(name="Shop not setup",
                           value="Setup server shop using `$setup`", inline=False)
    else:
        if isinstance(role, int):
            checkRole = guildData.get_role(role.id)
            if checkRole is None:
                embedVar.add_field(name="Role not found",
                                   value="Role dies not exist in the server.", inline=False)
            else:
                managers = servInf["manager"]
                managers.append(role)
                embedVar.add_field(name="Added Manager",
                                   value="Added Role: `" + role + "` to the Manager List", inline=False)
        elif isinstance(role, discord.Role):

            checkRole = guildData.get_role(role.id)
            if checkRole is None:
                embedVar.add_field(name="Role not found",
                                   value="Role dies not exist in the server.", inline=False)
            else:
                managers = servInf["manager"]
                managers.append(role.id)
                embedVar.add_field(name="Added Manager",
                                   value="Added Role: `" + role + "` to the Manager List", inline=False)


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def confirm(ctx, orderCode: str):
    servInf = serv.find_one({"_id": ctx.guild.id})
    order = orders.find_one({"_id": orderCode, "searchCode": servInf["searchCode"]})
    if order is None:
        embedVar = discord.Embed(title="Order confirmation", description="Order Code: " + orderCode, color=0xffcccc)
        embedVar.add_field(name="Order Code not found.", value="The order for the given order code does not exist",
                           inline=False)
        await ctx.send(embed=embedVar)
    else:

        items = order["items"]

        embedVar = printOrder("Order confirmation",
                              "Order Code: " + orderCode,
                              "React to process order", order, servInf)
        embedVar.add_field(name="Order Date and Time", value=str(order["orderDate"]),inline=False)
        message = await ctx.send(embed=embedVar)
        await message.add_reaction('✅')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.author.send("Checkout timed out")
        else:
            processTime = "Time Processed: " + str(datetime.utcnow())
            embedVar1 = discord.Embed(title="Order Confirmed",
                                      description="The order `" + orderCode + "` has been confirmed. Payment Received.",
                                      color=0xffcccc)
            embedVar1.set_footer(text=processTime)
            await ctx.send(embed=embedVar1)

            embedVar2 = printOrder("Order Confirmed",
                                   "The order `" + orderCode + "` has been confirmed. Payment Received.",
                                   processTime, order, servInf)
            buyer = bot.get_user(order["userID"])
            await buyer.send(embed=embedVar2)
            orders.find_one_and_update({"_id": orderCode}, {"$set": {"processed": True}})


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def refund(ctx, orderCode: str):
    servInf = serv.find_one({"_id": ctx.guild.id})
    order = orders.find_one({"_id": orderCode, "searchCode": servInf["searchCode"]})
    embedVar = discord.Embed(title="Confirm Refund",
                             description="Order Code: " + orderCode +
                                         "\nMake sure to refund payment before sending this refund confirmation",
                             color=0xffcccc)
    if order is None:
        embedVar.add_field(name="Order Code not found.", value="The order for the given order code does not exist",
                           inline=False)
        await ctx.send(embed=embedVar)
    else:
        if not order["refundRequest"]:
            embedVar.add_field(name="Order has not been requested for refund.",
                               value="The buyer has not requested a refund for this order.",
                               inline=False)
            await ctx.send(embed=embedVar)
        elif order["refunded"]:
            embedVar.add_field(name="Order has already been refunded",
                               value="This order is already refunded.",
                               inline=False)
            await ctx.send(embed=embedVar)
        else:
            embedVar = printOrder("Confirm Refund", "Order Code: " + orderCode +
                                  "\nMake sure to refund payment before sending this refund confirmation",
                                  "React to confirm refund", order, servInf)
            embedVar.add_field(name="Order Date and Time", value=str(order["orderDate"]), inline=False)
            message = await ctx.send(embed=embedVar)
            await message.add_reaction('✅')

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '✅'

            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.author.send("Checkout timed out")
            else:
                processTime = "Time Processed: " + str(datetime.utcnow())
                embedVar1 = discord.Embed(title="Order Refunded",
                                          description="The order `" + orderCode +
                                                      "` has been confirmed to be refunded.",
                                          color=0xffcccc)
                embedVar1.set_footer(text=processTime)
                await ctx.send(embed=embedVar1)

                embedVar2 = printOrder("Order Refunded", "The order `" + orderCode +
                                       "` has been confirmed to be refunded.", processTime, order, servInf)
                embedVar2.add_field(name="Order Date and Time", value=str(order["orderDate"]), inline=False)

                buyer = bot.get_user(order["userID"])
                await buyer.send(embed=embedVar2)
                orders.find_one_and_update({"_id": orderCode}, {"$set": {"refunded": True}})


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def pending(ctx):
    servInf = serv.find_one({"_id": ctx.guild.id})
    order = orders.find({"searchCode": servInf["searchCode"], "processed": False})
    embedVar = discord.Embed(title="Pending orders", description="Unprocessed/unconfirmed orders.", color=0xffcccc)
    for item in order:
        user = bot.get_user(item["userID"])
        embedVar.add_field(name="Order Code: " + item["_id"],
                           value="Total: `" + str(item["total"]) + "`\nUser: `" + user.name +"#" + user.discriminator
                                 + "`\nOrder Date: `" + str(item["orderDate"]) + "`",
                           inline=False)
        await ctx.send(embed=embedVar)


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def check(ctx, orderCode):
    servInf = serv.find_one({"_id": ctx.guild.id})
    order = orders.find_one({"_id": orderCode, "searchCode": servInf["searchCode"]})
    if order is None:
        embedVar = discord.Embed(title="Order Details", description="Order Code: " + orderCode, color=0xffcccc)
        embedVar.add_field(name="Order does not exist.", value="Order with given order code does not exist.",
                           inline=False)
    else:
        user = bot.get_user(order["userID"])
        embedVar = printOrder("Order Details", "Order Code: " + orderCode, "User: " + user.name + "#" +
                              user.discriminator + "\nOrder Date: " + str(order["orderDate"]) + "", order, servInf)
        embedVar.add_field(name="Processed/Confirmed:", value=order["processed"],
                           inline=False)
        embedVar.add_field(name="Refund Request:", value=order["refundRequest"],
                           inline=False)
        embedVar.add_field(name="Refunded:", value=order["refunded"],
                           inline=False)

        await ctx.send(embed=embedVar)


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def addp(ctx, name: str, price: float, count: int, *desc):
    servInf = serv.find_one({"_id": ctx.guild.id})
    code = uuid.uuid4().hex[:8]
    desc = listToString(desc)
    newProd = {"_id": code,
               "name": name,
               "price": price,
               "count": count,
               "desc": desc,
               "serverID": ctx.guild.id}
    prods.insert_one(newProd)
    result = prods.find_one({"_id": code})
    description = "Succesfully added: `" + result["name"] + "`"
    value = "Price: `" + servInf["currency"] + " " + str(result["price"]) + "` Count: `" + str(
        result["count"]) + "` Code: `" + result["_id"] + "`\n\n Description: \n" + result["desc"]
    embedVar = discord.Embed(title="Product Added", description=description, color=0xffcccc)
    embedVar.add_field(name="Details", value=value, inline=True)
    await ctx.send(embed=embedVar)


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def delp(ctx, code: str):
    servInf = serv.find_one({"_id": ctx.guild.id})
    deleted = prods.find_one_and_delete({"_id": code, "serverID": ctx.guild.id})
    name = "Successfully deleted: `" + deleted["name"] + "`"
    value = "Price: `" + servInf["currency"] + " " + str(deleted["price"]) + "` Count: `" + str(
        deleted["count"]) + "` Code: `" + deleted[
                "_id"] + "`\n Description: \n" + deleted["desc"]
    embedVar = discord.Embed(title="Delete Status", description="", color=0xffcccc)
    embedVar.add_field(name=name, value=value, inline=True)
    await ctx.send(embed=embedVar)


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def setcurrency(ctx, currcode: str):
    item = serv.find_one({"_id": ctx.guild.id})
    currency = c.get_symbol(currcode)
    embedVar = discord.Embed(title="Set Currency", description="", color=0xffcccc)

    if currency is None:
        embedVar.add_field(name="Invalid Currency", value="Enter a currency found in ISO 4217.", inline=True)
    if currency is not None and item is None:
        embedVar.add_field(name="Shop not setup", value="Setup Shop using $setup", inline=True)
    elif currency is not None and item is not None:
        updatedCurr = serv.find_one_and_update({"_id:": ctx.guild.id}, {"$set": {"currency": currcode}})
        embedVar.add_field(name="Updated Currency",
                           value="Updated store currency to " + currcode + " (" + currency + ")", inline=True)
    await ctx.send(embed=embedVar)


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def setshipping(ctx, cost: float):
    item = serv.find_one({"_id": ctx.guild.id})
    embedVar = discord.Embed(title="Set Shipping Cost", description="", color=0xffcccc)
    if item is None:
        embedVar.add_field(name="Shop not setup", value="Setup Shop using $setup", inline=True)
    else:
        updatedCurr = serv.find_one_and_update({"_id:": ctx.guild.id}, {"$set": {"shippingCost": cost}})
        embedVar.add_field(name="Updated Shipping", value="Shipping Price: `" + item["currency"] + " " + str(cost),
                           inline=True)
    await ctx.send(embed=embedVar)


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def addpayment(ctx, paymentType: str, *instruction):
    item = serv.find_one({"_id": ctx.guild.id})
    instruction = listToString(instruction)
    embedVar = discord.Embed(title="Add Payment", description="Add a payment option.", color=0xffcccc)
    if item is None:
        embedVar.add_field(name="Shop not setup.", value="Setup shop using `$setup`",
                           inline=True)
    else:
        item["payments"][paymentType] = instruction
        options = item["payments"]
        newSet = {"payments": options}
        serv.find_one_and_update({"_id": ctx.guild.id}, {"$set": newSet})
        embedVar.add_field(name=paymentType, value="Option Instruction:\n" + instruction, inline=True)

    await ctx.send(embed=embedVar)


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def delpayment(ctx, type: str):
    item = serv.find_one({"_id": ctx.guild.id})
    embedVar = discord.Embed(title="Set Payment", description="Add a payment option.", color=0xffcccc)
    if item is None:
        embedVar.add_field(name="Shop not setup.", value="Setup shop using `$setup`",
                           inline=True)
    else:
        options = item["payments"]
        if type in options:
            options.pop(type)
            newSet = {"payments": options}
            serv.find_one_and_update({"_id": ctx.guild.id}, {"$set": newSet})
            embedVar.add_field(name="Pay option removed", value="Removed **" + type + "** as a payment option.",
                               inline=False)
        else:
            embedVar.add_field(name="Pay option not found",
                               value="Possible typo or the payment option was never added.",
                               inline=False)

    await ctx.send(embed=embedVar)


@bot.command()
async def info(ctx, searchCode: str = None):
    embedVar = discord.Embed(title="Shop Info", description=" ", color=0xffcccc)
    if searchCode is None:
        item = serv.find_one({"_id": ctx.guild.id})
        embedVar.add_field(name="Currency", value="`" + item["currency"] + "`",
                           inline=False)
        embedVar.add_field(name="Shipping Cost", value="`" + str(item["shippingCost"]) + "`",
                           inline=False)
        embedVar.add_field(name="Search Code", value="`" + item["searchCode"] + "`",
                           inline=False)
        options = "💳: "
        for key in item["payments"]:
            options += (key + ",")
        options = options[:-1]
        print(options)
        embedVar.add_field(name="Payment Options", value=options, inline=False)
    else:
        item = serv.find_one({"searchCode": searchCode})
        embedVar.add_field(name="Currency", value="`" + item["currency"] + "`",
                           inline=False)
        embedVar.add_field(name="Shipping Cost", value="`" + str(item["shippingCost"]) + "`",
                           inline=False)
        embedVar.add_field(name="Search Code", value="`" + item["searchCode"] + "`",
                           inline=False)
        options = " "
        for key in item["payments"]:
            options += (item["payments"][key] + ",")
        options = options[:-1]
        print(options)
        embedVar.add_field(name="Payment Options", value=options, inline=False)
    await ctx.send(embed=embedVar)


@bot.command()
async def products(ctx, searchCode: str = None):
    embedVar = discord.Embed(title="Products", description="Product List.", color=0xffcccc)
    if searchCode is None:
        servInf = serv.find_one({"_id": ctx.guild.id})
        results = prods.find({"serverID": ctx.guild.id})
        for product in results:
            name = product["name"]
            value = "Price: `" + servInf["currency"] + " " + str(product["price"]) + "` Count: `" + str(
                product["count"]) + "` Item ID: `" + product[
                        "_id"] + "`\n" + product["desc"]
            embedVar.add_field(name=name, value=value, inline=False)
    else:
        servInf = serv.find_one({"searchCode": searchCode})
        results = prods.find({"serverID": servInf["_id"]})
        for product in results:
            name = product["name"]
            value = "Price: `" + servInf["currency"] + " " + str(product["price"]) + "` Count: `" + str(
                product["count"]) + "` Item ID: `" + product[
                        "_id"] + "`\n" + product["desc"]
            embedVar.add_field(name=name, value=value, inline=False)

    await ctx.send(embed=embedVar)


@bot.command()
async def payments(ctx, searchCode: str = None):
    embedVar = discord.Embed(title="Payment Options", description="List of available payment options.", color=0xffcccc)
    if searchCode is None:
        servInf = serv.find_one({"_id": ctx.guild.id})
        for key in servInf["payments"]:
            embedVar.add_field(name=key, value=servInf["payments"][key], inline=False)
    else:
        servInf = serv.find_one({"searchCode": searchCode})
        for key in servInf["payments"]:
            embedVar.add_field(name=key, value=servInf["payments"][key], inline=False)
    await ctx.send(embed=embedVar)


@bot.command()
@commands.dm_only()
async def add(ctx, serverCode: str, code: str, quant: int):
    servInf = serv.find_one({"searchCode": serverCode})
    item = prods.find_one({"_id": code, "serverID": servInf["_id"]})
    value = "Price: `" + servInf["currency"] + " " + str(item["price"]) + "` Quantity: in cart`" + str(
        quant) + "` Item ID: `" + item["_id"] + "`\n Description: \n" + item["desc"]
    embedVar = discord.Embed(title="Add to Cart", description="", color=0xffcccc)
    if quant <= 0:
        embedVar.add_field(name="Invalid Quantity", value="You must order at least 1 item.", inline=True)
    elif item is None:
        embedVar.add_field(name="Item code does not exist", value="No items correspond with the code given.",
                           inline=True)
    elif item is not None and item["count"] < quant:
        embedVar.add_field(name="Invalid Quantity", value="Order count beyond what is in-stock", inline=True)
    elif item is not None and item["count"] >= quant:
        existCart = carts.find_one({"userID": ctx.author.id, "serverID": servInf["_id"], "itemCode": item["_id"]})
        if existCart is not None and item["count"] < (quant + existCart["quantity"]):
            embedVar.add_field(name="Invalid Quantity",
                               value="Order count beyond what is in-stock.Your cart contains this item.", inline=True)
        elif existCart is not None and item["count"] >= (quant + existCart["quantity"]):
            myquery = {"userID": ctx.author.id, "serverID": servInf["_id"], "itemCode": item["_id"]}
            newquantity = {"quantity": quant + existCart["quantity"]}
            carts.update_one(myquery, {"$set": newquantity})
            name = "Updated Quantity of item `" + item["name"] + "`"
            embedVar.add_field(name=name, value="Order count beyond what is in-stock.Your cart contains this item.",
                               inline=True)
        elif existCart is None:
            cartID = uuid.uuid4().hex[:8]
            addToCart = {"_id": cartID,
                         "userID": ctx.author.id,
                         "serverID": servInf["_id"],
                         "itemCode": item["_id"],
                         "quantity": quant}
            carts.insert_one(addToCart)
            name = "Successfully added: `" + item["name"] + "` to cart."
            embedVar.add_field(name=name, value=value, inline=True)
    await ctx.send(embed=embedVar)


@bot.command()
@commands.dm_only()
async def remove(ctx, serverCode: str, code: str, quant: int):
    embedVar = discord.Embed(title="Removed from cart", description="", color=0xffcccc)
    servInf = serv.find_one({"searchCode": serverCode})
    item = carts.find_one({"itemCode": code, "userID": ctx.author.id, "serverID": servInf["_id"]})
    if item is None:
        embedVar.add_field(name="Item not found in your cart.",
                           value="The item you are looking for is not in your cart. Check your cart using: `$cart servercode`",
                           inline=True)
    elif item is not None:
        details = prods.find_one({"_id": code, "serverID": servInf["_id"]})
        if quant >= item["quantity"]:
            deleted = carts.find_one_and_delete({"itemCode": code, "userID": ctx.author.id, "serverID": servInf["_id"]})
            embedVar.add_field(name="Deleted Items: `" + details["name"] + "`",
                               value="Removed the item from your cart. Check your cart using: `$cart`\n" +
                                     "`" + details["name"] + "`\n Quantity removed: `" + str(quant) + "` Price: `"
                                     + details["price"] + "` Item ID: `" + code + "`\n\nDescription: \n" + details[
                                         "desc"],
                               inline=True)
        elif quant < item["quantity"]:
            carts.update_one({"itemCode": code, "userID": ctx.author.id, "serverID": servInf["_id"]},
                             {"$set": {"quantity": item["quantity"] - quant}})
            embedVar.add_field(name="Deleted `" + str(quant) + " " + details["name"] + "` from your cart.",
                               value="Removed the item(s) from your cart. Check your cart using: `$cart`\n\n" +
                                     "`" + details["name"] + "`\n Quantity in your cart: `" + str(
                                   item["quantity"] - quant) + "` Price: `" + servInf["currency"] + " " + str(
                                   details["price"]) + "` Item ID: `" + code + "`\n\nDescription: \n" + details["desc"],
                               inline=True)
    await ctx.send(embed=embedVar)


@bot.command()
@commands.dm_only()
async def cart(ctx, serverCode: str):
    servInf = serv.find_one({"searchCode": serverCode})
    embedVar = discord.Embed(title="Your Cart", description="", color=0xffcccc)
    results = carts.find({"userID": ctx.author.id, "serverID": servInf["_id"]})
    if results.count() == 0:
        embedVar.add_field(name="Empty cart", value="Your cart is empty", inline=False)
        await ctx.send(embed=embedVar)
    else:
        for item in results:
            product = prods.find_one({"_id": item["itemCode"], "serverID": servInf["_id"]})
            name = product["name"]
            if product["count"] >= item["quantity"]:
                value = "Price: `" + servInf["currency"] + " " + str(product["price"]) + "` Quantity: `" + str(
                    item["quantity"]) + "` Item ID: `" + product[
                            "_id"] + "`\n\nDescription:\n" + product["desc"]
                embedVar.add_field(name=name, value=value, inline=False)
            else:
                value = "Out of stock or ordering too many.\n Available Items: `" + str(item["quantity"]) \
                        + "` Order quantity: `" + str(product["count"])
                embedVar.add_field(name=name, value=value, inline=False)
            await ctx.send(embed=embedVar)


@bot.command()
@commands.dm_only()
async def checkout(ctx, serverCode: str):
    embedVar = discord.Embed(title="Checkout", description="", color=0xffcccc)
    servInf = serv.find_one({"searchCode": serverCode})
    results = carts.find({"userID": ctx.author.id, "serverID": servInf["_id"]})
    items = {}
    subtotal = 0
    total = 0
    shipping = 0
    if results.count() == 0:
        embedVar.add_field(name="Empty cart", value="Add products to your cart to checkout.", inline=False)
        await ctx.send(embed=embedVar)
    else:
        for item in results:
            product = prods.find_one({"_id": item["itemCode"], "serverID": servInf["_id"]})
            name = product["name"]
            if product["count"] >= item["quantity"]:
                value = "Price: `" + servInf["currency"] + " " + str(product["price"]) + "` Quantity: `" + str(
                    item["quantity"]) + "` Item ID: `" + product[
                            "_id"] + "`\nDescription:\n" + product["desc"]
                subtotal = subtotal + product["price"] * item["quantity"]
                items[name] = (product["price"], item["quantity"], product["_id"], product["desc"])
                embedVar.add_field(name=name, value=value, inline=False)
            else:
                value = "Order cancelled. Out of stock or ordering too many.\n Available Items: `" \
                        + str(product["count"]) + "` Order quantity: `" + str(item["quantity"])
                embedVar.add_field(name=name, value=value, inline=False)
        embedVar.add_field(name="Sub-Total", value="`" + servInf["currency"] + " " + str(subtotal) + "`", inline=False)
        if subtotal != 0:
            embedVar.add_field(name="Shipping",
                               value="`" + servInf["currency"] + " " + str(servInf["shippingCost"]) + "`",
                               inline=False)
            shipping = servInf["shippingCost"]
            total = total + subtotal + shipping
        else:
            total = subtotal
        embedVar.add_field(name="Total", value="`" + servInf["currency"] + " " + str(total) + "`", inline=False)
        embedVar.set_footer(text="React to confirm order")
        message = await ctx.send(embed=embedVar)
        await message.add_reaction('✅')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.author.send("Checkout timed out")
        else:
            orderID = uuid.uuid4().hex[:8]
            dt = datetime.utcnow()
            newOrder = {"_id": orderID, "userID": ctx.author.id, "searchCode": servInf["searchCode"], "items": items,
                        "subtotal": subtotal, "shipping": shipping, "total": total, "orderDate": dt,
                        "messageID": message.id, "processed": False, "refunded": False, "refundRequest": False}
            orders.insert_one(newOrder)

            embedVar1 = discord.Embed(title="Order Code: " + newOrder["_id"], description="Order Date: " + str(dt),
                                      color=0xffcccc)
            for key in items:
                value = "Price: `" + servInf["currency"] + " " + str(items[key][0]) + "` Quantity: `" \
                        + str(items[key][1]) + "` Item ID: `" + items[key][2] + "`\nDescription:\n" + items[key][3]
                embedVar1.add_field(name=key, value=value, inline=False)
            embedVar1.add_field(name="Sub-Total",
                                value="`" + servInf["currency"] + " " + str(newOrder["subtotal"]) + "`",
                                inline=False)
            embedVar1.add_field(name="Shipping",
                                value="`" + servInf["currency"] + " " + str(newOrder["shipping"]) + "`",
                                inline=False)
            embedVar1.add_field(name="Total", value="`" + servInf["currency"] + " " + str(newOrder["total"]) + "`",
                                inline=False)
            await ctx.send(embed=embedVar1)

            embedVar2 = discord.Embed(title="Payment Options", description="List of available payment options.",
                                      color=0xffcccc)
            for key in servInf["payments"]:
                embedVar2.add_field(name=key, value=servInf["payments"][key], inline=False)

            for item in items:
                prods.find_one_and_update({"_id": items[item][2], "serverID": servInf["_id"]},
                                          {"$inc": {"count": -items[item][1]}})
                carts.find_one_and_delete(
                    {"userID": ctx.author.id, "serverID": servInf["_id"], "itemCode": items[item][2]})

            await ctx.send(embed=embedVar2)

            owner = bot.get_user(bot.get_guild(servInf["_id"]).owner_id)
            await owner.send(embed=embedVar1)


@bot.command()
@commands.dm_only()
async def cancel(ctx, orderCode):
    embedVar = discord.Embed(title="Order Cancellation", description="Order Code: " + orderCode, color=0xffcccc)
    orderCheck = orders.find_one({"_id": orderCode, "userID": ctx.author.id})
    if orderCheck is None:
        embedVar.add_field(name="Order not found.", value="No order found with the given order code.", inline=False)
        await ctx.send(embed=embedVar)
    else:
        if orderCheck["processed"]:
            embedVar.add_field(name="Order has already been paid and processed.",
                               value="To request a refund use `$rrefund orderCode`", inline=False)
            await ctx.send(embed=embedVar)
        else:
            servInf = serv.find_one({"searchCode": orderCheck["searchCode"]})
            embedVar = printOrder("Order Cancellation", "Order Code: " + orderCode,
                                  "React to confirm order cancellation", orderCheck, servInf)
            message = await ctx.send(embed=embedVar)
            await message.add_reaction('✅')

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '✅'

            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.author.send("Timed out")
            else:
                items = orderCheck["items"]
                for item in items:
                    prods.find_one_and_update({"_id": items[item][2], "serverID": servInf["_id"]},
                                              {"$inc": {"count": items[item][1]}})

                orders.find_one_and_delete({"_id": orderCode, "userID": ctx.author.id})
                cancelTime = str(datetime.utcnow())
                embedVar1 = discord.Embed(title="Order Cancelled", description="Cancelled Order: " + orderCode,
                                          color=0xffcccc)
                embedVar1.set_footer(text=cancelTime)
                embedVar.title = "Order Cancelled"
                embedVar.description = "Order `" + orderCode + "` has been cancelled"
                embedVar.set_footer(text=cancelTime)

                await ctx.send(embed=embedVar1)
                owner = bot.get_user(bot.get_guild(servInf["_id"]).owner_id)
                await owner.send(embed=embedVar)


@bot.command()
@commands.dm_only()
async def rrefund(ctx, orderCode):
    embedVar = discord.Embed(title="Request Refund", description="Order Code: " + orderCode, color=0xffcccc)
    orderCheck = orders.find_one({"_id": orderCode, "userID": ctx.author.id})
    if orderCheck is None:
        embedVar.add_field(name="Order not found.", value="No order found with the given order code.", inline=False)
        await ctx.send(embed=embedVar)
    else:
        if not orderCheck["processed"]:
            embedVar.add_field(name="Order has not been processed. To cancel order, use `$cancel orderCode`",
                               value="To request a refund use `$rrefund`", inline=False)
            await ctx.send(embed=embedVar)
        else:
            servInf = serv.find_one({"searchCode": orderCheck["searchCode"]})
            embedVar = printOrder("Request Refund", "Order Code: " + orderCode,
                                  "React to confirm refund request", orderCheck, servInf)
            message = await ctx.send(embed=embedVar)
            await message.add_reaction('✅')

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '✅'

            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.author.send("Timed out")
            else:
                orders.find_one_and_update({"_id": orderCode, "userID": ctx.author.id ,"searchCode": servInf["searchCode"]},
                                          {"$set": {"refundRequest": True}})
                cancelTime = str(datetime.utcnow())
                embedVar1 = discord.Embed(title="Refund Request sent", description="Order Code: " + orderCode,
                                          color=0xffcccc)
                embedVar1.set_footer(text=cancelTime)
                await ctx.send(embed=embedVar1)

                embedVar.title = "Refund Request"
                embedVar.description = "Order `" + orderCode + "` requested for refund."
                embedVar.set_footer(text=cancelTime)
                embedVar.add_field(name="Details",
                                   value="User: " + user.name + "#" + user.discriminator, inline=False)
                owner = bot.get_user(bot.get_guild(servInf["_id"]).owner_id)
                await owner.send(embed=embedVar)

                
bot.run(os.environ['TOKEN'])
