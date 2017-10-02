from getpass import getpass
from pprint import pprint
from bitshares.asset import Asset
from bitshares.block import Block
from bitshares.price import Price
from bitshares.market import Market
import pendulum
import math

amplitude = 0.5 # 50% fluctuating the price feed $+-0.50
current_time = pendulum.now().timestamp() # Current timestamp for reference within the hertz script
reference_timestamp = pendulum.parse(Block(1)['timestamp']).timestamp() # Retrieving the Bitshares2.0 genesis block timestamp
period = pendulum.SECONDS_PER_DAY * 30.43 # 30.43 days converted to an UNIX timestamp
reference_asset_value = 1.00 # $1.00 USD
waveform = math.sin(((((current_time - reference_timestamp)/period) % 1) * period) * ((2*math.pi)/period)) # Only change for an alternative HERTZ ABA.

# Get HERTZ price in USD
hertz_usd = reference_asset_value + ((amplitude * reference_asset_value) * waveform)

market = Market("USD:BTS") # Set reference market to USD:BTS
price = market.ticker()["quoteSettlement_price"] # Get Settlement price of USD
price.invert() # Switching from quantity of BTS per USD to USD price of one BTS.
hertz = Price(hertz_usd, "USD/HERTZ") # Limit the hertz_usd decimal places & convert from float.

hertz_bts = hertz / price # Calculate HERTZ price in BTS

# Some printed outputs
print("Price of HERTZ in USD: {}".format(hertz))
print("Price of USD in BTS: {}".format(price))
print("Price of HERTZ in BTS: {}".format(hertz_bts))

# Unlock the Bitshares wallet
hertz.bitshares.wallet.unlock(getpass())

# Publish the price feed to the BTS DEX
# Make sure you change the 'account' before executing.
pprint(hertz.bitshares.publish_price_feed(
    "HERTZ",
    hertz_bts,
    mssr=110,
    mcr=175,
    account="<YOUR FEED PRODUCER ACCOUNT NAME>"
))