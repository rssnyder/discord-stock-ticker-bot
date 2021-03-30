import logging
from os import getenv

import discord
from requests import get

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

        if message.content.startswith('!ticker'):

            opts = message.content.split(' ')
            logging.info(opts)

            if len(opts) < 3:
                await message.reply('usage: !ticker <stock/crypto> <ticker>', mention_author=True)

            security = opts[1]
            ticker = opts[2]

            if security not in TICKER_TYPES:
                await message.reply(f'valid types: {TICKER_TYPES}', mention_author=True)
            
            resp = get(
                f'https://discord-stock-ticker-api.cloud.rileysnyder.org/{security}/{ticker}'
            )
            logging.info(resp.text)

            if resp.json().get('error'):
                await message.reply(resp.json().get('error', 'unknown error'), mention_author=True)
            elif resp.json().get('existing') and resp.json().get('client_id'):
                await message.reply(f'this ticker already exists! {invite_url(resp.json().get("client_id"))}', mention_author=True)
            elif resp.json().get('client_id'):
                await message.reply(f'new ticker created! {invite_url(resp.json().get("client_id"))}', mention_author=True)


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