from getpass import getpass
from pprint import pprint
from bitshares.asset import Asset
from bitshares.price import Price
from bitshares.market import Market
from datetime import date, datetime, timedelta
import time
import math

# Get Settlement price of USD
market = Market("USD:BTS")
price = market.ticker()["quoteSettlement_price"]
price.invert()

# Get HERTZ price in USD
hertz_usd = 1.00 + (0.5 * math.sin(((((time.time() - 1444745544)/2629746) % 1) * 2629746) * ((2*math.pi)/2629746)))


hertz = Price(hertz_usd, "USD/HERTZ")

# Calculate HERTZ price in BTS
hertz_bts = price * hertz

# Some outputs
print("Price of HERTZ in USD: {}".format(hertz))
print("Price of USD in BTS: {}".format(price))
print("Price of HERTZ in BTS: {}".format(hertz_bts))

# Unlock the wallet
hertz.bitshares.wallet.unlock(getpass())

# Publish the price feed
pprint(hertz.bitshares.publish_price_feed(
    "HERTZ",
    hertz_bts,
    mssr=110,
    mcr=175,
    account="<YOUR FEED PRODUCER ACCOUNT NAME>"
))