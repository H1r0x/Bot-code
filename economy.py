@bot.command(aliases=['bal'])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f'{ctx.author.name} Balance',color = discord.Color.red()) 
    em.add_field(name="Wallet :moneybag:", value=wallet_amt)
    em.add_field(name='Bank :money_with_wings:', value=bank_amt, inline=False)
    await ctx.send(embed= em)

@bot.command()
async def beg(ctx):

    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(2000)

    if earnings == 0:
        await ctx.send(f"{ctx.author.mention}How unlucky... You didn't get anything...")

    elif earnings > 50:
        await ctx.send(f"{ctx.author.mention} Nice you got ⏣{earnings} from a cool dude")

    elif earnings > 100:
        await ctx.send(f"{ctx.author.mention} Someone felt nice and gave you ⏣{earnings}")

    elif earnings > 500:
        await ctx.send(f"{ctx.author.mention} You seem to have a way with people! Someone gave you ⏣{earnings}")

    elif earnings > 800:
        await ctx.send(f"{ctx.author.mention} What a lucky day!! Someone gave you ⏣{earnings}")

    elif earnings > 1500:
        await ctx.send(f"{ctx.author.mention} A rich man passed by you and felt bad. So ha gave you ⏣{earnings}")

    elif earnings > 2000:
        await ctx.send(f"{ctx.author.mention} A shady man walked up to you and said 'I know how tough it can be out here' before giving you ⏣{earnings}")


    users[srt(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        users = json.load(f)

@bot.command()
async def work(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(10000)

    await ctx.send(f'{ctx.author.mention} You worked and earned {earnings}✪ coins!!')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)


@bot.command(aliases=['with'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,'bank')
    await ctx.send(f'{ctx.author.mention} You withdrew {amount} coins')


@bot.command(aliases=['dep'])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You deposited {amount} coins')


@bot.command(aliases=['sm'])
async def send(ctx,member : discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount,'bank')
    await update_bank(member,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')
