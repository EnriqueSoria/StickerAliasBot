# @StickerAliasBot
## Try it
It can be online or not, I don't have it hosted anywhere. 

 - Send to @StickerAliasBot: `/start`
 - Send to @StickerAliasBot a (non-animated) sticker
 - Send to @StickerAliasBot tome keywords space-separated



 - Go to another chat and use it on inline mode and search stickers by your tags

## Run
```bash
git clone https://github.com/EnriqueSoria/StickerAliasBot.git
pipenv sync
touch .secret
```
 - Generate a token with @BotFather
 - Paste it into `.secret`
```bash
pipenv shell
python bot.py
```