import logging
from os import getenv
from time import sleep

import discord
from requests import get

from util import stock, crypto, crypto_search, add_bot, add_private_bot, change_ticker_photo

TICKER_TYPES = [
    'stock',
    'crypto'
]

def invite_url(client_id: str):

    return f'https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=0&scope=bot'

class DiscordStockTickerBot(discord.Client):

    async def on_ready(self):
        logging.info('Logged in')

    async def on_message(self, message):

        if message.author.id == self.user.id:
            return

        if message.author.id == int(getenv('ADMIN_ID')):
            
            if message.content.startswith('!addbot'):

                opts = message.content.split(' ')
                logging.info(opts)

                if len(opts) < 3:
                    await message.reply('usage: !addbot <client_id> <token>', mention_author=True)
                    return
                
                if add_bot(opts[1], opts[2]):
                    await message.reply('Bot added!', mention_author=True)
                    return
                else:
                    await message.reply('Unable to add new bot.', mention_author=True)
                    return
            
        if message.content.startswith('!ticker'):

            opts = message.content.split(' ')
            logging.info(opts)

            if len(opts) < 3:
                await message.reply('usage: !ticker <stock/crypto> <ticker>', mention_author=True)
                return

            security = opts[1]
            ticker = opts[2]

            if security not in TICKER_TYPES:
                await message.reply(f'valid types: {TICKER_TYPES}', mention_author=True)
                return
            
            if security == 'stock':
                resp = stock(ticker)
            elif security == 'crypto':
                resp = crypto(ticker)

            if resp.get('error'):
                await message.reply(resp.get('error', 'unknown error'), mention_author=True)
                return
            elif resp.get('existing') and resp.get('client_id'):
                await message.reply(f'this ticker already exists! <{invite_url(resp.get("client_id"))}>', mention_author=True)
                return
            elif resp.get('client_id'):
                await message.reply(f'new ticker created!: <{invite_url(resp.get("client_id"))}>', mention_author=True)
                return
        
        if message.content.startswith('!search'):

            opts = message.content.split(' ')
            logging.info(opts)

            if len(opts) < 2:
                await message.reply('usage: !search <crypto>', mention_author=True)
                return

            cryptos = opts[1]

            results = crypto_search(cryptos)

            await message.reply(f'possible coins: {", ".join(results)}', mention_author=True)
            return


        if message.content.startswith('!image'):
            
            opts = message.content.split(' ')
            logging.info(opts)

            if len(opts) < 3:
                await message.reply('usage: !image <stock/crypto> <image url>')
                return

            ticker = opts[1]
            url = opts[2]

            result = change_ticker_photo(ticker.lower(), url)

            if result:
                await message.add_reaction('\U00002705')
                return
            else:
                await message.add_reaction('\U0000274E')
                return


if __name__ == "__main__":

    logging.basicConfig(
        filename=getenv('LOG_FILE'),
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s %(levelname)-8s %(message)s',
    )

    token = getenv('DISCORD_BOT_TOKEN')
    if not token:
        print('DISCORD_BOT_TOKEN not set!')

    client = DiscordStockTickerBot()
    client.run(token)
