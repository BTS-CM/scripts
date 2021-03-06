from getpass import getpass
from pprint import pprint
from bitshares.asset import Asset
from bitshares import BitShares
from bitshares.instance import set_shared_bitshares_instance
from bitshares.price import Price
from bitshares.market import Market
import pendulum
import math

def get_hertz_feed(reference_timestamp, current_timestamp, period_days, phase_days, reference_asset_value, amplitude):
	"""
	Given the reference timestamp, the current timestamp, the period (in days), the phase (in days), the reference asset value (ie 1.00) and the amplitude (> 0 && < 1), output the current hertz value.
	You can use this for an alternative HERTZ asset!
	"""
	hz_reference_timestamp = pendulum.parse(reference_timestamp).timestamp() # Retrieving the Bitshares2.0 genesis block timestamp
	hz_period = pendulum.SECONDS_PER_DAY * period_days
	hz_phase = pendulum.SECONDS_PER_DAY * phase_days
	hz_waveform = math.sin(((((current_timestamp - (hz_reference_timestamp + hz_phase))/hz_period) % 1) * hz_period) * ((2*math.pi)/hz_period)) # Only change for an alternative HERTZ ABA.
	hz_value = reference_asset_value + ((amplitude * reference_asset_value) * hz_waveform)
	return hz_value

def phase_verification(date_from, date_to):
	"""
	Given a date range, output a list of days (at T12:00:00+00:00) and their respective HERTZ oscillation value.
	Use this function to verify that you have applied a correct phase to your ABA.
	The get_hertz_feed function references the global hertz variables.
	"""
	date_list = pendulum.period(pendulum.parse(date_from), pendulum.parse(date_to))

	for date in date_list.range('days'):
		hertz_test_timestamp = date.timestamp()
		hertz_value_list = get_hertz_feed(hertz_reference_timestamp, hertz_test_timestamp, hertz_period_days, hertz_phase_days, hertz_reference_asset_value, hertz_amplitude)
		print(date.to_date_string(), date.format('%A'), "{0:.2f}".format(hertz_value_list))

if __name__ == "__main__":
	full_node_list = [
		"wss://eu.nodes.bitshares.works", #location: "Central Europe - BitShares Infrastructure Program"
		"wss://us.nodes.bitshares.works", #location: "U.S. West Coast - BitShares Infrastructure Program"
		"wss://sg.nodes.bitshares.works", #location: "Singapore - BitShares Infrastructure Program"
		"wss://bitshares.crypto.fans/ws", #location: "Munich, Germany"
		"wss://bit.btsabc.org/ws", #location: "Hong Kong"
		"wss://bitshares.apasia.tech/ws", #location: "Bangkok, Thailand"
		"wss://japan.bitshares.apasia.tech/ws", #location: "Tokyo, Japan"
		"wss://api.bts.blckchnd.com" #location: "Falkenstein, Germany"
		"wss://openledger.hk/ws", #location: "Hong Kong"
		"wss://bitshares.dacplay.org/ws", #location:  "Hangzhou, China"
		"wss://bitshares-api.wancloud.io/ws", #location:  "China"
		"wss://ws.gdex.top", #location: "China"
		"wss://dex.rnglab.org", #location: "Netherlands"
		"wss://dexnode.net/ws", #location: "Dallas, USA"
		"wss://kc-us-dex.xeldal.com/ws", #location: "Kansas City, USA"
		"wss://la.dexnode.net/ws", #location: "Los Angeles, USA"
		"wss://btsza.co.za:8091/ws" #location: "Cape Town, South Africa"
	]

	bitshares_api_node = BitShares(full_node_list)
	set_shared_bitshares_instance(bitshares_api_node) # Set the API node TODO: Enable polling multiple nodes & taking avg!

	hertz_reference_timestamp = "2015-10-13T14:12:24+00:00" # Bitshares 2.0 genesis block timestamp
	hertz_current_timestamp = pendulum.now().timestamp() # Current timestamp for reference within the hertz script
	hertz_amplitude = 0.14 # 14% fluctuating the price feed $+-0.14
	hertz_period_days = 28 # Aka wavelength, time for one full SIN wave cycle.
	hertz_phase_days = 0.908056 # Time offset from genesis till the first wednesday, to set wednesday as the primary Hz day.
	hertz_reference_asset_value = 1.00 # $1.00 USD, not much point changing as the ratio will be the same.

	# Verify phase
	print(phase_verification("2018-01-01","2019-01-31"))
