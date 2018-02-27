# HERTZ Bitshares price feed scripts

This repository contains reference Hertz price feed scripts and tools.

Hertz is an Algorithm Based Asset (ABA) which is a Market Pegged Asset (MPA) that's pegged to the USD and modified using a sine wave algorithm to predictably oscillate using an amplitude of 14% and a period of 28 days.

Given that this repo (and all other hertz price feed repos) are MIT licensed, everyone is free to copy/modify the concept behind Hertz with alternative static variables (different amplitudes, periods, reference timestamp, reference asset, algorithm, etc).

Before you can publish price feeds for Hertz you'll need to be added to the 'approved list of price feed publishers' within Hertz smartcoin settings.

### hertz_feed.py Installation & Usage

The reference hertz price feed Python3 script is implemented using the python-bitshares library, it was designed and tested with Ubuntu in mind so the following instructions may not work for alternative operating systems.

#### Setup Ubuntu software dependencies

`sudo apt-get install virtualenv git libffi-dev libssl-dev python-dev python3-dev python3-pip`

#### Create a virtual environment

Used to keep your Python environment isolated from one another.

```
mkdir Hertz
virtualenv -p python3 Hertz
echo "source ./Hertz/bin/activate" > access_hertz_environment.sh
chmod +x access_hertz_environment.sh
source access_hertz_environment.sh # To activate the environment
```

#### Install Python packages

The following python packages are required for publishing Hertz price feeds.

Note that in order to properly install the python packages, you must be within the Hertz python virtual environment we created in the previous step. You can do this via `source access_hertz_environment.sh`, if successful your terminal prompt will show `(Hertz) username@computer_name:~$`.

We need to use the development branch of the `python-bitshares` repo as the master branch has dependency issues regarding `pycrypto`.

```
pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install --upgrade wheel
pip3 install requests
pip3 install pendulum
pip3 install bitshares
```

If any of the above commands fail, pip3 will inform you of any missing dependencies you need to install. Please post an issue to this repo for improving docs if this occurs, thanks.

#### Download, configure & test the Hertz price feed scripts

From within your user's home directory run the following command:

```
git clone https://github.com/BTS-CM/scripts.git hertz_pricefeed
cd hertz_pricefeed/
```



Within the `hertz_pricefeed` folder, you need to configure:
* The `create_wallet.py` file, providing a `LOCAL_WALLET_PASSWORD` (doesn't need to be your Bitshares password) and the `PRICE_FEED_PUBLISHER_ACTIVE_KEY` (Extracted from the wallet).
* The `hertz-feed.py` file, specifically the 'LOCAL_WALLET_PASSWORD' (line 86 - created in the previous step) and 'account_name' (line 99 - your Bitshares account name).

Once configured, run the 'create_wallet.py' script via `python3 create_wallet.py` only once, then try `python3 hertz-feed.py` to publish a Hertz price feed. If you want to test the script without publishing a price feed then comment out lines 86-101 of `hertz-feed.py`.

#### Install the Systemd service & timer

In order to regularly publish Hertz price feeds, copy the hertz_feed service and timer to the appropriate systemd linux folder & launch the service.

Alter the contents of the timer file to change the frequency of publishing price feeds, the current default is set to 1 minute. After any changes run the command `sudo systemctl daemon-reload`.

You'll also need to change the `username` field in the `hertz_feed.service` file to the username you plan to run the script under.

```
mv hertz_feed.service /etc/systemd/system/hertz_feed.service
mv hertz_feed.timer /etc/systemd/system/hertz_feed.timer
sudo systemctl enable hertz_feed.service
sudo systemctl enable hertz_feed.timer
sudo systemctl daemon-reload
sudo systemctl start hertz_feed.timer
sudo systemctl start hertz_feed.service
```
