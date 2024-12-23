import discord
from discord.ext import commands
import random
import time

intents = discord.Intents.default()
intents.message_content = True  # Для доступу до вмісту повідомлень
intents.members = True  # Для доступу до інформації про користувачів

bot = commands.Bot(command_prefix="!", intents=intents)

# Словник для зберігання стану поросят (за user_id)
pigs = {}

# Команда для створення поросятка
@bot.command(name='addpig')
async def add_pig(ctx):
    user_id = str(ctx.author.id)
    if user_id in pigs:
        await ctx.send(f"\U0001F437 У вас вже є поросятко, {ctx.author.mention}! Назвіть його за допомогою команди `!rename <ім'я>`. ")
    else:
        pigs[user_id] = {
            'name': 'Поросятко',
            'weight': 20,  # Початкова вага
            'fed': False,  # Стан годування (False - не нагодоване)
        }
        await ctx.send(f"\U0001F416 Поросятко створено, {ctx.author.mention}! Назвіть його за допомогою команди `!rename <ім'я>`. ")

# Команда для перейменування поросятка
@bot.command(name='rename')
async def rename_pig(ctx, *, name: str):
    user_id = str(ctx.author.id)
    if user_id in pigs:
        pigs[user_id]['name'] = name
        await ctx.send(f"Ваше поросятко тепер називається **{name}**, {ctx.author.mention}! ")
    else:
        await ctx.send(f"\U0001F416 У вас немає поросятка, {ctx.author.mention}. Створіть його за допомогою команди `!addpig`. ")

# Команда для видалення поросятка
@bot.command(name='deletepig')
async def delete_pig(ctx):
    user_id = str(ctx.author.id)
    if user_id in pigs:
        del pigs[user_id]
        await ctx.send(f"\U0001F4A5 Ваше поросятко видалено, {ctx.author.mention}. Ви можете створити нове за допомогою команди `!addpig`. ")
    else:
        await ctx.send(f"\U0001F437 У вас немає поросятка, {ctx.author.mention}. ")

# Команда для годування поросятка
@bot.command(name='feed')
async def feed_pig(ctx):
    user_id = str(ctx.author.id)
    if user_id not in pigs:
        await ctx.send(f"\U0001F416 У вас немає поросятка, {ctx.author.mention}. Створіть його за допомогою команди `!addpig`. ")
    else:
        pigs[user_id]['fed'] = True  # Відмічаємо, що поросятко нагодоване
        await ctx.send(f"\U0001F35A Ви нагодували поросятко, {ctx.author.mention}! Тепер ви можете використовувати команду `!grow`. ")

# Команда для росту поросятка
@bot.command(name='grow')
async def grow_pig(ctx):
    user_id = str(ctx.author.id)
    if user_id not in pigs:
        await ctx.send(f"\U0001F416 У вас немає поросятка, {ctx.author.mention}. Створіть його за допомогою команди `!addpig`. ")
    elif not pigs[user_id]['fed']:
        await ctx.send(f"\U0001F35A Ви не нагодували поросятка, {ctx.author.mention}! Спочатку скористайтесь командою `!feed`. ")
    else:
        pig = pigs[user_id]
        weight_change = random.randint(-18, 18)  # Зміна ваги від -18 до 18 кг
        if weight_change < 0:
            weight_change = max(weight_change, -4)  # Мінімальна втрата ваги 4 кг
        elif weight_change > 0:
            weight_change = max(weight_change, 4)  # Мінімальний набір ваги 4 кг

        pig['weight'] += weight_change
        pig['weight'] = max(pig['weight'], 0)  # Щоб вага не стала від'ємною

        # Повідомлення про зміну ваги
        if weight_change > 0:
            await ctx.send(f"\U0001F43D @{ctx.author.mention}, ваше поросятко **{pig['name']}** наростило сальця: **{weight_change} кг**! Тепер вага: **{pig['weight']} кг**. ")
        elif weight_change < 0:
            await ctx.send(f"\U0001F43D @{ctx.author.mention}, ваше поросятко **{pig['name']}** скинуло: **{abs(weight_change)} кг**. Тепер вага: **{pig['weight']} кг**. ")
        else:
            await ctx.send(f"\U0001F437 @{ctx.author.mention}, ваше поросятко **{pig['name']}** не змінило вагу. Поточна вага: **{pig['weight']} кг**. ")

        pigs[user_id]['fed'] = False  # Скидаємо стан годування

# Команда для відображення статусу поросятка
@bot.command(name='stats')
async def stats_pig(ctx):
    user_id = str(ctx.author.id)
    if user_id in pigs:
        pig = pigs[user_id]
        await ctx.send(f"\U0001F416 @{ctx.author.mention}, ваше поросятко **{pig['name']}** важить **{pig['weight']} кг**. ")
    else:
        await ctx.send(f"\U0001F437 У вас немає поросятка, {ctx.author.mention}. Створіть його за допомогою команди `!addpig`. ")

# Запуск бота
bot.run("MTMyMDc2NDcwNzE1NzgzOTkyMw.GJkZON.sGq1SDgTS_z-KtU9st5YGearU_d1sTEH0ybams")