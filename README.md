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

If you've never used python-bitshares before and haven't created a local wallet then configure the `create_wallet.py` file, providing a `LOCAL_WALLET_PASSWORD` (doesn't need to be your Bitshares password) and the `PRICE_FEED_PUBLISHER_ACTIVE_KEY` (Extracted from the wallet), then run the 'create_wallet.py' script via `python3 create_wallet.py` once.

If you already have created a local python-bitshares wallet, proceed to the next step.

The `hertz-feed.py` file requires minor configuration, specifically the 'LOCAL_WALLET_PASSWORD' (line 86 - created in the previous step) and 'account_name' (line 99 - your Bitshares account name). Once configured, run the command `python3 hertz-feed.py` to publish a Hertz price feed.

If you want to test the script without publishing a price feed then comment out lines 86-101 of `hertz-feed.py`.

#### Install the Systemd service & timer

Once you've successfully tested the Hertz price feed script you should consider configuring a SystemD service and timer in order to regularly publish Hertz price feeds. The first step is alter the contents of the service file to provide the `username` you're running the script under. The second optional step is to configure the timer file by changing the trigger frequency; the current default is set to 60 seconds.

Once you've configured the service (and optionally the timer) files, copy the hertz_feed service and timer to the appropriate systemd linux folder using the following commands:

```
cp hertz_feed.service /etc/systemd/system/hertz_feed.service
cp hertz_feed.timer /etc/systemd/system/hertz_feed.timer
```

Once you've copied the files to the appropriate folder, run the following commands:

```
sudo systemctl daemon-reload
sudo systemctl enable hertz_feed.service
sudo systemctl enable hertz_feed.timer
sudo systemctl start hertz_feed.timer
sudo systemctl start hertz_feed.service
```
