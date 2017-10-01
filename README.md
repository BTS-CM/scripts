# HERTZ Bitshares price feed scripts

Only pre-approved price feed publishers will be able to publish price feeds against the 'HERTZ' Algorithm Based Asset, however these scripts can (and should) be used to create alternative HERTZ ABAs!

Likewise, only the HERTZ asset creator is able to update the asset using the python script.

## Pre-requisites

If you want to use the spreadsheet calculator you'll need a spreadsheet tool - I used Microsoft Excel 2016, there may be incompatibilities importing it to open source (or web based) spreadsheet tools.

You need to install [pyhton-bitshares](https://github.com/xeroc/python-bitshares/)!

### Documentation

Visit the [pybitshares website](http://docs.pybitshares.com/en/latest/) for in depth documentation on the python-bitshares library.

### Installation

#### Install with pip3:
```
$ sudo apt-get install libffi-dev libssl-dev python-dev python-dev3
$ pip3 install bitshares
```

#### Manual installation:
```
$ git clone https://github.com/xeroc/python-bitshares/
$ cd python-bitshares
$ python3 setup.py install --user
```

#### Upgrade
```
$ pip3 install --user --upgrade
```
