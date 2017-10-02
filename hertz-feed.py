from getpass import getpass
from pprint import pprint
from bitshares.asset import Asset
from bitshares import BitShares
from bitshares.block import Block
from bitshares.instance import set_shared_bitshares_instance
from bitshares.price import Price
from bitshares.market import Market
import pendulum
import math

bitshares_api_node = BitShares(
    # If the connected API node is down, uncomment one of the
    #"wss://node.bitshares.eu/ws"
    #"wss://dexnode.net/ws"
    #"wss://bitshares.openledger.info/ws"
    "wss://bitshares.crypto.fans/ws"
    #"wss://openledger.hk/ws"
    )

set_shared_bitshares_instance(bitshares_api_node) # Set the API node 

reference_timestamp = pendulum.parse(Block(1)['timestamp']).timestamp() # Retrieving the Bitshares2.0 genesis block timestamp
period = pendulum.SECONDS_PER_DAY * 30.43 # 30.43 days converted to an UNIX timestamp
reference_asset_value = 1.00 # $1.00 USD
amplitude = 0.5 # 50% fluctuating the price feed $+-0.50
current_time = pendulum.now().timestamp() # Current timestamp for reference within the hertz script
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
print("Price of BTS in USD: {}".format(price))
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