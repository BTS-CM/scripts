from apscheduler.schedulers.blocking import BlockingScheduler
from bitshares.asset import Asset
from bitshares import BitShares
from bitshares.instance import set_shared_bitshares_instance
from bitshares.price import Price
from bitshares.market import Market
from getpass import getpass
from pprint import pprint
import math
import os
import pendulum
from pycoingecko import CoinGeckoAPI

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

def run_hertz_function():
	time_before = pendulum.now()
	# Getting the value of USD in BTS
	market = Market("USD:BTS") # Set reference market to USD:BTS
	price = market.ticker()["quoteSettlement_price"] # Get Settlement price of USD
	price.invert() # Switching from quantity of BTS per USD to USD price of one BTS.

	#Hertz variables:
	#Change only for alternative Algorithm Based Assets.
	hertz_reference_timestamp = "2015-10-13T14:12:24+00:00" # Bitshares 2.0 genesis block timestamp
	hertz_current_timestamp = pendulum.now().timestamp() # Current timestamp for reference within the hertz script
	hertz_amplitude = 0.14 # 14% fluctuating the price feed $+-0.14 (2% per day)
	hertz_period_days = 28 # Aka wavelength, time for one full SIN wave cycle.
	hertz_phase_days = 0.908056 # Time offset from genesis till the first wednesday, to set wednesday as the primary Hz day.
	hertz_reference_asset_value = 1.00 # $1.00 USD, not much point changing as the ratio will be the same.
	hertz_core_exchange_rate = 0.80
	
	# Calculate the current value of Hertz in USD
	hertz_value = get_hertz_feed(hertz_reference_timestamp, hertz_current_timestamp, hertz_period_days, hertz_phase_days, hertz_reference_asset_value, hertz_amplitude)
	hertz = Price(hertz_value, "USD/HERTZ") # Limit the hertz_usd decimal places & convert from float.

        cg = CoinGeckoAPI() # Initialise coingecko
        bts_usd_coingecko = cg.get_price(ids='bitshares', vs_currencies='usd') # Price of BTS in USD from coingecko
        bts_usd_coingecko_value = Price(bts_usd_coingecko["bitshares"]["usd"], "USD/BTS") # Price format

        hertz_bts = bts_usd_coingecko_value.invert() * hertz.as_quote("HERTZ") # Feed price
        hertz_cer = hertz_bts * hertz_core_exchange_rate

        # Some printed outputs
        #print("Price of HERTZ in USD: {}".format(hertz))
        #print("Price of HERTZ in BTS: {}".format(hertz_bts))
        #print("Price of BTS in USD: {}".format(bts_usd_coingecko_value))
        #print("Price of USD in BTS: {}".format(bts_usd_coingecko_value.invert()))

	# Unlock the Bitshares wallet
	hertz.bitshares.wallet.unlock("LOCAL_WALLET_PASSWORD")

	"""
	Publish the price feed to the BTS DEX
	Make sure you change the 'account' before executing.
	Don't change any of the other values.
	"""
	pprint(hertz.bitshares.publish_price_feed(
		"HERTZ",
		hertz_bts,
		cer=hertz_cer, # Setting in line with Wackou's price feed scripts
		mssr=110,
		mcr=200,
		account="REPLACE_WITH_YOUR_USERNAME"
	))

	#time_after = pendulum.now()
	#time_difference = time_after.diff(time_before).in_seconds()
	#print("Time (seconds) taken: {}".format(time_difference))
	#print(".-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.")


if __name__ == "__main__":

	full_node_list = [
	"wss://eu.nodes.bitshares.works", #location: "Central Europe - BitShares Infrastructure Program"
	"wss://us.nodes.bitshares.works", #location: "U.S. West Coast - BitShares Infrastructure Program"
	"wss://sg.nodes.bitshares.works", #location: "Singapore - BitShares Infrastructure Program"
	"wss://bitshares.crypto.fans/ws", #location: "Munich, Germany"
	"wss://bitshares.apasia.tech/ws", #location: "Bangkok, Thailand"
	"wss://japan.bitshares.apasia.tech/ws", #location: "Tokyo, Japan"
	"wss://api.bts.blckchnd.com" #location: "Falkenstein, Germany"
	"wss://dexnode.net/ws", #location: "Dallas, USA"
	"wss://kc-us-dex.xeldal.com/ws", #location: "Kansas City, USA"
	"wss://la.dexnode.net/ws", #location: "Los Angeles, USA"
	]

	bitshares_api_node = BitShares(full_node_list, nobroadcast=False)

	# Set the API node above as the shared Bitshares instance for the rest of the script
	set_shared_bitshares_instance(bitshares_api_node)

	scheduler = BlockingScheduler()
	scheduler.add_job(run_hertz_function, 'interval', seconds=60)

	try:
		scheduler.start()
	except (SystemExit):
		pass
