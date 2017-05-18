from getpass import getpass
from pprint import pprint
from bitshares.asset import Asset
from bitshares.price import Price
from bitshares.market import Market
from datetime import date, datetime, timedelta

# Get Settlement price of USD
market = Market("USD:BTS")
price = market.ticker()["quoteSettlement_price"]
price.invert()

# Get HERO price in USD
hero_usd = (1.05 ** ((date.today() - date(1913, 12, 23)).days / 365.2425))
hero = Price(hero_usd, "USD/HERO")

# Calculate HERO price in BTS
hero_bts = price * hero

# Some outputs
print("Price of HERO in USD: {}".format(hero))
print("Price of USD in BTS: {}".format(price))
print("Price of HERO in BTS: {}".format(hero_bts))

# Unlock the wallet
hero.bitshares.wallet.unlock(getpass())

# Publish the price feed
pprint(hero.bitshares.publish_price_feed(
    "HERO",
    hero_bts,
    account="<YOUR FEED PRODUCER ACCOUNT NAME>"
))
