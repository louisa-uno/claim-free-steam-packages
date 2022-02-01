import asyncio
import json
import logging
import sys
import time

import requests
from ASF import IPC
from tqdm import tqdm

logging.basicConfig(
    filename="logging.txt",
    filemode='w',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)

log = logging.getLogger('urbanGUI')

try:
	config = json.load(open("config.json"))
	log.debug("Found config file")
except FileNotFoundError:
	log.debug("Couldn't find config file")
	config = {
	    "IPC": {
	        "host": "http://localhost:1242",
	        "password": "your IPC password"
	    },
	    "git_token": "NOT needed if only used to activate packages"
	}
	config["IPC"]["host"] = input("Enter your ArchiSteamFarm host address: ")
	config["IPC"]["host"] = input("Enter your ArchiSteamFarm host password: ")
	log.debug("Saving config file")
	with open("config.json", "w") as f:
		f.write(json.dumps(config))
	log.debug("Saved config file")
except json.JSONDecodeError:
	log.error("Couldn't decode config to json")
	sys.exit()


async def main():
	async with IPC(ipc=config["IPC"]["host"],
	               password=config["IPC"]["password"]) as asf:
		with requests.get(
		    'https://raw.githubusercontent.com/Luois45/claim-free-steam-packages/update-package_list/package_list.txt'
		) as f:
			apps = f.text.split(',')
		for app in tqdm(apps, desc='Activating licenses'):
			try:
				with open('activated_packages.txt', 'r') as f:
					aps = f.read().split(',')
			except FileNotFoundError:
				with open('activated_packages.txt', 'w') as f:
					log.info("Created activated_packages file")
					aps = []
			foundPackage = False
			for ap in aps:
				if app == ap:
					log.debug("\nPackage found in activated_packages")
					foundPackage = True
			if not foundPackage:
				log.debug("\nPackage not found in activated_packages")
				cmd = "!addlicense app/" + app
				activatedPackage = False
				tries = 10
				for i in range(tries):
					resp = await asf.Api.Command.post(body={'Command': cmd})
					if resp.success:
						log.info("\n" + resp.result.replace("\r\n", ""))
						successCodes = ["Items:", "Aktivierte IDs:"]
						if any(x in resp.result for x in successCodes):
							activatedPackage = True
							with open('activated_packages.txt', 'a') as f:
								f.write(app + ",")
							time.sleep(90)
							break
					else:
						log.info(f'\nError: {resp.message}')
					time.sleep(90)
				if not activatedPackage:
					time.sleep(90)


loop = asyncio.get_event_loop()
output = loop.run_until_complete(main())
loop.close()
