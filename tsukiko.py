import discord
from discord.ext import commands
from trello import TrelloClient

client = commands.Bot(command_prefix='>')
tclient = TrelloClient(
    api_key='',
    token='')

@client.command()
@commands.has_permissions(manage_channels=True)
async def project(ctx, command, *name: str):
    if command == "create":
        board = tclient.add_board(' '.join(name))
        mainm = await ctx.send('Creating Project Structure for '+' '.join(name))
        cate = await ctx.guild.create_category(" ".join(name))
        info = await ctx.guild.create_text_channel("info", category=cate)
        await info.set_permissions(ctx.guild.default_role, send_messages=False)
        await info.send(f"`Title:` {' '.join(name)}\n`Status:` In Development")
        await ctx.guild.create_text_channel("general-discussion", category=cate)
        await ctx.guild.create_text_channel("artwork", category=cate)
        await ctx.guild.create_text_channel("code", category=cate)
        await ctx.guild.create_text_channel("models", category=cate)
        await ctx.guild.create_voice_channel("Discussion", category=cate)

        await mainm.edit(content=f"Created Project Structure for{' '.join(name)}")

    elif command == "delete":
        cate = None
        for project in ctx.guild.categories:
            if project.name.lower() == ' '.join(name).lower():
                cate = project
        if cate == None or str(project).lower() == "info":
            await ctx.send("Project not found!")
        else:
            mess = await ctx.send(f"Deleting Project Structure of {' '.join(name)}")
            for channel in cate.channels:
                await channel.delete()
            await cate.delete()
            print(f"Deleted Project Structure of {' '.join(name)} in {ctx.guild.name}")
            await mess.edit(content=f"Deleted Project Structure of {' '.join(name)}")

@project.error
async def project_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissions to do that!")

@client.command()
async def status(ctx, prog, *name:str):
    if prog.lower() == "developing":
        cate = None
        for project in ctx.guild.categories:
            if project.name.lower() == ' '.join(name).lower():
                cate = project
        if cate == None or str(project).lower() == "info":
            await ctx.send("Project not found!")
        else:
            chan = None
            for channel in cate.channels:
                if channel.name == "info":
                    chan = channel
            messages = await chan.history(limit=50).flatten()
            messages.reverse()
            await messages[0].edit(content=f"Title: {' '.join(name)}\nStatus: In Development")
            await ctx.send(f"Project {cate.name} Status Updated to 'In Development'")

    elif prog.lower() == "hold":
        cate = None
        for project in ctx.guild.categories:
            if project.name.lower() == ' '.join(name).lower():
                cate = project
                print(project.name)
        if cate == None or str(project).lower() == "info":
            await ctx.send("Project not found!")
        else:
            chan = None
            for channel in cate.channels:
                if channel.name == "info":
                    chan = channel
            messages = await chan.history(limit=50).flatten()
            messages.reverse()
            await messages[0].edit(content=f"Title: {' '.join(name)}\nStatus: On Hold")
            await ctx.send(f"Project {cate.name} Status Updated to 'On Hold'")

    elif prog.lower() == "completed":
        cate = None
        for project in ctx.guild.categories:
            if project.name.lower() == ' '.join(name).lower():
                cate = project
        if cate == None or str(project).lower() == "info":
            await ctx.send("Project not found!")
        else:
            chan = None
            for channel in cate.channels:
                if channel.name == "info":
                    chan = channel
            messages = await chan.history(limit=50).flatten()
            messages.reverse()
            await messages[0].edit(content=f"Title: {' '.join(name)}\nStatus: Completed")
            await ctx.send(f"Project {cate.name} Status Updated to 'Completed'")

@client.command()
async def ping(ctx):
    await ctx.send('Pong! '+str(round(client.latency * 1000))+'ms, '+ctx.message.author.mention)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("OwO | >help"))
    print("Logged in as " + client.user.name)
    print("Running in:")
    for server in client.guilds:
        print(server)
    print()

client.run('')
