import discord
from discord.ext import commands

BOT_TOKEN = 'YOUR BOT TOKEN'

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
id =647315961032212480
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello there! New moderation bot here ")

@bot.command()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def ban(ctx, user:discord.Member, *,reason=None):

    if reason is None:
        reason = "No reason provided"

    await user.ban(reason=reason)
    await ctx.send(f'{user.mention} has been banned for: {reason}')


@bot.command()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def kick(ctx, user:discord.Member, *,reason=None):
    if reason is None:
        reason = 'No reason provided'
    await user.kick(reason=reason)
    await ctx.send(f'{user.mention} has been kicked for : {reason }')



@bot.command()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    guild = ctx.guild
    user = await bot.fetch_user(user_id)
    await guild.unban(user)
    await ctx.send(f'{user.mention} has been unbanned')


@bot.command()
@commands.has_permissions(manage_roles=True)
@commands.bot_has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    try:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not muted_role:
            # If the Muted role doesn't exist, create it
            muted_role = await ctx.guild.create_role(name="Muted")

            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True,
                                              read_messages=False)

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(
            f'{member.mention} has been muted for: {reason}' if reason else f'{member.mention} has been muted.')
    except discord.Forbidden:
        await ctx.send("I do not have permission to mute this member.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")

@bot.command()
@commands.has_permissions(manage_roles=True)
@commands.bot_has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    try:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(muted_role)
        await ctx.send(f'{member.mention} has been unmuted')
    except discord.Forbidden:
        await ctx.send("I do not have permission to mute this member.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")




@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to ban members.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have permission to ban members.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Member not found. Please mention a valid member.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a member to ban.")
    else:
        await ctx.send("An error occurred.")


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to unban members.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have permission to unban members.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid user ID provided.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a user ID to unban.")
    else:
        await ctx.send("An error occurred.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to ban members.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have permission to ban members.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Member not found. Please mention a valid member.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a member to ban.")
    else:
        await ctx.send("An error occurred.")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to mute members.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have permission to manage roles.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Member not found. Please mention a valid member.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a member to mute.")
    else:
        await ctx.send("An error occurred.")


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    avatar_url = member.display_avatar.url
    embed = discord.Embed(title=f"{member.display_name}'s avatar")
    embed.set_image(url=avatar_url)

    await ctx.send(embed=embed)


@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Member not found. Please mention a valid member.")
    else:
        await ctx.send(f"An error occurred: {error}")


bot.run(BOT_TOKEN)

