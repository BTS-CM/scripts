from getpass import getpass
from pprint import pprint
from bitshares import BitShares
from bitshares.asset import Asset

bitshares = BitShares(
    proposer="customminer",
    proposal_expiration=60 * 60 * 24 * 3,
    # nobroadcast=True,
    bundle=True,
)

bitshares.wallet.unlock(getpass("Password: "))
hertz = Asset("HERTZ", bitshares_instance=bitshares)

# This needs to be updated with appropriate private feed producers
hertz.update_feed_producers([
    "blckchnd",
    "delegate.ihashfury",
    "rnglab",
    "taconator-witness",
    "verbaltech2",
    "delegate-1.lafona",
    "roelandp",
    "wackou",
    "spartako",
    "sahkan-bitshares",
    "sc-ol"
])

pprint(
    hertz.bitshares.txbuffer.broadcast()
)
