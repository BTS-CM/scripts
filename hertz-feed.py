from getpass import getpass
from pprint import pprint
from bitshares.asset import Asset
from bitshares.price import Price
from bitshares.market import Market
from datetime import date, datetime, timedelta
import time
import math

reference_timestamp = 1444745544 # Bitshares 2.0 genesis UNIX timestamp
period = 2629746 # 30.43 days converted to an UNIX timestamp
reference_asset_value = 1.00 # $1.00 USD
amplitude = 0.5 * reference_asset_value # 50% fluctuating the price feed $+-0.50
current_time = time.time()

# Get HERTZ price in USD
hertz_usd = reference_asset_value + (amplitude * math.sin(((((current_time - reference_timestamp)/period) % 1) * period) * ((2*math.pi)/period)))

market = Market("USD:BTS") # Set reference market to USD:BTS
price = market.ticker()["quoteSettlement_price"] # Get Settlement price of USD
price.invert() # Switching from USD/BTS to BTs/USD?
hertz = Price(hertz_usd, "USD/HERTZ") # Limit the hertz_usd decimal places?

hertz_bts = hertz / price # Calculate HERTZ price in BTS

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