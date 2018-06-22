#!/usr/bin/env python
import requests
import hashlib
import click
import logging
import re

from time import sleep
from alkivi.logger import Logger

# Define the global logger
logger = Logger(min_log_level_to_mail=None,
                min_log_level_to_save=None,
                min_log_level_to_print=logging.DEBUG)

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


@click.command()
@click.option('--user', default='admin', help='User to log in.')
@click.option('--password', prompt='Password', help='Password for user.')
@click.option('--ip', prompt='Switch IP', help='IP of the switch.')
@click.option('--port', prompt='Port to reset', help='Port number to reset.', type=int)
def dlink(user, password, ip, port):
    """Script to turn POE Off & On again."""
    print('Going to reset port {0} of switch {1}'.format(port, ip))

    pinkpanther = hashlib.md5()
    pinkpanther.update(password.encode('utf-8'))

    data = {
        'pinkpanther': pinkpanther.hexdigest(),
        'pelican': user,
        'BrowsingPage': 'index_dlink.htm',
        'currlang': 0,
        'changlang': 0,
    }

    # Global session
    s = requests.Session()

    # Auth
    auth_url = 'http://{0}/homepage.htm'.format(ip)
    auth_response = s.post(auth_url, data=data)

    # Now fetch gambit
    m = re.search('Gambit=([A-Z0-9]*)"', auth_response.text)
    if m:
        gambit = m.groups()
    else:
        logger.warning('Unable to get gambit from auth_response, quitting', auth_response.text)
        exit(0)

    # Now post port POE
    data = {
        'Gambit': gambit,
        'FormName': 'portset',
        'port_f': '{0:02d}'.format(port - 1),
        'port_t': '{0:02d}'.format(port - 1),
        'PoE_Enable': 0,
        'TimeRangeID': 0,
        'Priority': 2,
        'PDDetect': 2,
        'legacyPD': 1,
        'post_url': 'cgi_port.'
    }
    poe_url = 'http://{0}/iss/specific/PoEPortSetting.js'.format(ip)
    poe_response = s.post(poe_url, data)
    logger.debug('poe', poe_response.status_code, poe_response.headers, poe_response.text)

    sleep(1)
    data = {
        'Gambit': gambit,
        'FormName': 'portset',
        'port_f': '{0:02d}'.format(port - 1),
        'port_t': '{0:02d}'.format(port - 1),
        'PoE_Enable': 1,
        'TimeRangeID': 0,
        'Priority': 2,
        'PDDetect': 2,
        'PowerLimit': 1,
        'legacyPD': 1,
        'post_url': 'cgi_port.'
    }
    poe_url = 'http://{0}/iss/specific/PoEPortSetting.js'.format(ip)
    poe_response = s.post(poe_url, data)
    logger.debug('poe', poe_response.status_code, poe_response.headers, poe_response.text)


if __name__ == '__main__':
    dlink()
