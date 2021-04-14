# discord-stock-ticker-bot

a bot to manage the public and premium versions of my [discord stock tickers](https://rssnyder.github.io/discord-stock-ticker/).

join the discord to use: [![Discord Chat](https://img.shields.io/discord/806606291798982678)](https://discord.gg/CQqnCYEtG7)

## user commands

`!ticker stock <stock symbol>`

eg: `!ticker stock pfg`

`!ticker crypto <crypto name>`

eg: `!ticker crypto bitcoin`

## admin commands

add a new empty bot to the db

`!newbot <client_id> <token>`

add a new bot to a premium user's db

`!addprivatebot <client> <client_id> <token> <ticker> <type>`

restart a stack

`!restart <stack name>`
