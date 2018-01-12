from getpass import getpass
from pprint import pprint
from bitshares.asset import Asset
from bitshares import BitShares
#from bitshares.block import Block #Uncomment if using blocknumber as reference timestamp.
from bitshares.instance import set_shared_bitshares_instance
from bitshares.price import Price
from bitshares.market import Market
import pendulum
import math

def get_hertz_feed(reference_timestamp, current_timestamp, period_days, phase_days, reference_asset_value, amplitude):
    """
    Given the reference timestamp, the current timestamp, the period (in days), the phase (in days), the reference asset value (ie 1.00) and the amplitude (> 0 && < 1), output the current hertz value.
    You can use this formula for an alternative HERTZ asset!
    Be aware though that extreme values for amplitude|period will create high volatility which could cause black swan events. BSIP 18 should help, but best tread carefully!
    """
    hz_reference_timestamp = pendulum.parse(reference_timestamp).timestamp() # Retrieving the Bitshares2.0 genesis block timestamp
    hz_period = pendulum.SECONDS_PER_DAY * period_days
    hz_phase = pendulum.SECONDS_PER_DAY * phase_days
    hz_waveform = math.sin(((((current_timestamp - (hz_reference_timestamp + hz_phase))/hz_period) % 1) * hz_period) * ((2*math.pi)/hz_period)) # Only change for an alternative HERTZ ABA.
    hz_value = reference_asset_value + ((amplitude * reference_asset_value) * hz_waveform)
    return hz_value

bitshares_api_node = BitShares(
    # If the connected API node is down, switch to an alternative manually by uncommenting a line & commenting out the broken node.
    #"wss://node.bitshares.eu/ws"
    #"wss://dexnode.net/ws"
    #"wss://bitshares.openledger.info/ws"
    "wss://bitshares.crypto.fans/ws"
    #"wss://openledger.hk/ws"
    )

set_shared_bitshares_instance(bitshares_api_node) # Set the API node TODO: Enable polling multiple nodes & taking avg!

# Unlock the Bitshares wallet
# Perform check prior to calculating HERTZ value, to prevent delay in providing password from publishing an inaccurate (late) Hz price feed.
hertz.bitshares.wallet.unlock(getpass())

#hertz_reference_timestamp = pendulum.parse(Block(1)['timestamp']).timestamp() # Retrieving the Bitshares2.0 genesis block timestamp via the Bitshares library
hertz_reference_timestamp = "2015-10-13T14:12:24+00:00" # Bitshares 2.0 genesis block timestamp
hertz_current_timestamp = pendulum.now().timestamp() # Current timestamp for reference within the hertz script
hertz_amplitude = 0.14 # 14% fluctuating the price feed $+-0.14 (2% per day)
hertz_period_days = 28 # Aka wavelength, time for one full SIN wave cycle.
hertz_phase_days = 0.908056 # Time offset from genesis till the first wednesday, to set wednesday as the primary Hz day.
hertz_reference_asset_value = 1.00 # $1.00 USD, not much point changing as the ratio will be the same.

hertz_value = get_hertz_feed(hertz_reference_timestamp, hertz_current_timestamp, hertz_period_days, hertz_phase_days, hertz_reference_asset_value, hertz_amplitude)

print("Hertz Value: {}".format(hertz_value))

market = Market("USD:BTS") # Set reference market to USD:BTS
price = market.ticker()["quoteSettlement_price"] # Get Settlement price of USD
hertz = Price(hertz_value, "USD/HERTZ") # Limit the hertz_usd decimal places & convert from float.
hertz_bts = hertz / price # Calculate HERTZ price in BTS (THIS IS WHAT YOU PUBLISH!)

# Some printed outputs
print("Price of HERTZ in USD: {}".format(hertz))
print("Price of USD in BTS: {}".format(price))
print("Price of HERTZ in BTS: {}".format(hertz_bts))

"""
Publish the price feed to the BTS DEX
Make sure you change the 'account' before executing.
Don't change any of the other values.
"""
pprint(hertz.bitshares.publish_price_feed(
    "HERTZ",
    hertz_bts,
    mssr=110,
    mcr=200,
    account="<YOUR FEED PRODUCER ACCOUNT NAME>"
))
