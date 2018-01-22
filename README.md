# HERTZ Bitshares price feed scripts

Only pre-approved price feed publishers will be able to publish price feeds against the 'HERTZ' Algorithm Based Asset, however these scripts can (and should) be used to create alternative HERTZ ABAs!

Likewise, only the HERTZ asset creator is able to update the asset using the python script.

## Pre-requisites

If you want to use the spreadsheet calculator you'll need a spreadsheet tool - I used Microsoft Excel 2016, there may be incompatibilities importing it to open source (or web based) spreadsheet tools.

You need to install [pyhton-bitshares](https://github.com/xeroc/python-bitshares/)!

### Documentation

Visit the [pybitshares website](http://docs.pybitshares.com/en/latest/) for in depth documentation on the python-bitshares library.

### Installation

```
pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install --upgrade wheel
pip3 install requests
pip3 install lomond
pip3 install wsaccel
pip3 install hug
pip3 install gunicorn
git clone https://github.com/xeroc/python-bitshares.git -b develop
pip3 install -e python-bitshares/
mv hertz_feed.service /etc/systemd/system/hertz_feed.service
mv hertz_feed.timer /etc/systemd/system/hertz_feed.timer
sudo systemctl enable hertz_feed.service
sudo systemctl enable hertz_feed.timer
sudo systemctl start hertz_feed.timer
sudo systemctl daemon-reload
```

Only implement the systemd service if you've set a static password.
