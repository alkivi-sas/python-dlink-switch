# Script for DLink Switches

Simple script to deal with dlink switch that only have a web interface. Using request we can so far do the following actions :
- Power POE off & on

## Installation

You need python3 and pipenv, install this tools via your favorite way.

```shell
git clone https://github.com/alkivi-sas/python-dlink-switch
cd python-dlink-switch
pipenv install
pipenv shell
```

## Usage

Once in your pipenv shell

```python
./dlink.py --help
Usage: dlink.py [OPTIONS]

  Script to turn POE Off & On again.

Options:
  --user TEXT      User to log in.
  --password TEXT  Password for user.
  --ip TEXT        IP of the switch.
  --port INTEGER   Port number to reset.
  --help           Show this message and exit.
```
