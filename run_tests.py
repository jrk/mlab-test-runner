#!/usr/bin/python 

import json
import logging
import random
import subprocess
import socket
import time
import urllib2
import sys
from datetime import datetime

hostname = socket.gethostname()
host_ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

clt = 'web100clt'

def test(site):
    global clt
    global hostname, host_ip
    logging.info('Testing %s (%s) to %s at %s', hostname, host_ip, site, str(datetime.now()))
    subprocess.check_call([clt, '--name', site, '-ll'])

def main():
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger().setLevel(logging.INFO)
    global clt
    try:
        subprocess.check_output([clt, '--help'])
    except:
        clt = '/ndt/src/web100clt'
        subprocess.check_output([clt, '--help'])
    
    while True:
        try:
            nearest_data = json.load(
                urllib2.urlopen('https://mlab-ns.appspot.com/ndt'))
            test(nearest_data['fqdn'])

            if False: # skip all-sites
                all_sites = json.load(
                    urllib2.urlopen('https://mlab-ns.appspot.com/ndt?policy=all'))
                us_sites = [site for site in all_sites if site['country'] == 'US']
                us_site = random.choice(us_sites)
                test(us_site['fqdn'])

        except urllib2.URLError as ue:
            logging.error('Failed to access MLabNS: %s', ue.message)

        except subprocess.CalledProcessError as cpe:
            logging.error('Non-zero exit status: %d "%s"', cpe.returncode,
                          cpe.message)

        sleeptime = random.expovariate(1.0/1800.0)
        logging.info('About to sleep for %g seconds', sleeptime)
        time.sleep(sleeptime)

if __name__ == '__main__':
    main()
