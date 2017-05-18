from getpass import getpass
from pprint import pprint
from bitshares import BitShares
from bitshares.asset import Asset


bitshares = BitShares(
    proposer="chainsquad",
    proposal_expiration=60 * 60 * 24 * 3,
    # nobroadcast=True,
    bundle=True,
)
bitshares.wallet.unlock(getpass("Password: "))
hero = Asset("HERO", bitshares_instance=bitshares)

"""
hero.add_markets(
    "whitelist",
    ["BTS", "USD", "HERO"],
    force_enable=True
)
"""

hero.update_feed_producers([
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
])

pprint(
    hero.bitshares.txbuffer.broadcast()
)
