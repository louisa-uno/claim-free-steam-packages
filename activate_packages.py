import asyncio
import json
import logging
import random
import re
import sys
import time

import requests
from ASF import IPC
from tqdm import tqdm

ASF_SEPARATOR = ','
INPUT_SEPARATOR = ','
OUTPUT_SEPARATOR = ','

logging.basicConfig(
    filename="logging.txt",
    filemode='w',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.WARNING)

log = logging.getLogger('urbanGUI')


def loadConfig():
	try:
		with open('config.json', 'r') as f:
			config = json.load(f)
			return config
	except FileNotFoundError:
		return createConfig()
	except json.decoder.JSONDecodeError:
		print(
		    "Config file is not valid JSON. Please delete the config file and run the script again."
		)
		sys.exit(0)


def createConfig():
	config = {
	    "IPC": {
	        "host": "http://localhost:1242",
	        "password": "your IPC password",
	        "accounts": ["ASF"]
	    },
	    "STEAM": {
	        "id": "your STEAM id",
			"apikey": "your STEAM apikey"
	    },
	    "repeat_hour_delay": "2"
	}
	config["IPC"]["host"] = input("Enter your ArchiSteamFarm host address (Example: http://192.168.1.188:21242): ")
	config["IPC"]["password"] = input(
	    "Enter your ArchiSteamFarm host password: ")
	config["IPC"]["accounts"][0] = input("Enter the name of your bot name in ASF: ")
	config["STEAM"]["id"] = input(
	    "Entering your steam ID will download the IDs of the Steam games you own to skip them when activating packages.\nIf you don't want to enter your ID just leave it empty and press enter.\nYou can find it out here. https://www.steamidfinder.com/ You need the steamID64 in Dec\nexample: https://steamcommunity.com/id/Louis_45/ → 76561198841548760 is the ID\nYour Steam ID: "
	)
	config["STEAM"]["apikey"] = input("Entering your steam apikey is necessary for checking the already activated packages. You can find it out/register it here. https://steamcommunity.com/dev/apikey\nYour Steam apikey: ")
	log.debug("Saving config file")
	with open("config.json", "w") as f:
		f.write(json.dumps(config))
	log.debug("Saved config file")
	return config


config = loadConfig()


async def activatePackages(asf, tries):
	with requests.get(
	    'https://raw.githubusercontent.com/Luois45/claim-free-steam-packages/auto-update/package_list.txt'
	) as f:
		package_list = f.text.split(INPUT_SEPARATOR)
		print("Downloaded repo package list with {} free packages.".format(
		    len(package_list)))

	activatedPackage = False
	try:
		with open('activated_packages.txt', 'r') as f:
			activated_packages = f.read().split(OUTPUT_SEPARATOR)
	except FileNotFoundError:
		with open('activated_packages.txt', 'w') as f:
			log.info("Created activated_packages file")
			steamId = config["STEAM"]["id"]
			steamApikey = config["STEAM"]["apikey"]
			if steamId != "" and steamId != "your STEAM id" and steamApikey != "" and steamApikey != "your STEAM apikey":
				with requests.get(
				    f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steamApikey}&steamid={steamId}&format=json"
				) as r:
					html = r.text
					regex = re.compile('"appid":(\d+),')
					resultsList = regex.findall(html)
					log.info(
					    f"Fetched {len(resultsList)} packages to activated_packages.txt using Steam Username"
					)
					results = ""
					for result in resultsList:
						results += result + OUTPUT_SEPARATOR
					f.write(results)
					del results
					del resultsList
		with open('activated_packages.txt', 'r') as f:
			activated_packages = f.read().split(OUTPUT_SEPARATOR)

	apps = []
	for app in package_list:
		if app not in activated_packages:
			apps.append(app)
	random.shuffle(apps)

	if len(apps) > 0:
		print(
		    "Out of {} known free packages, {} are not already activated in your account. Beginning activation."
		    .format(len(package_list), len(apps)))

		for app in tqdm(apps, desc=f'{tries} attempt: Activating licenses'):

			cmd = "!addlicense " + ASF_SEPARATOR.join(
			    config["IPC"]["accounts"]) + " app/" + app
			resp = await asf.Api.Command.post(body={'Command': cmd})

			if resp.success:
				log.info(resp.result.replace("\r\n", ""))
				successCodes = ["Items:", "Aktivierte IDs:"]

				if any(x in resp.result for x in successCodes):
					activatedPackage = True
					with open('activated_packages.txt', 'a') as f:
						f.write(app + OUTPUT_SEPARATOR)
			else:
				log.info(f'Error: {resp.message}')
			time.sleep(74)
	else:
		print(
		    "Out of {} known free packages, all are already activated. Skipping activation phase."
		    .format(len(package_list)))
	del activated_packages
	del package_list
	delay = int(config["repeat_hour_delay"]) * 3600
	print('Waiting {} hours to check for new free packages.'.format(
	    config["repeat_hour_delay"]))
	for _ in tqdm(range(delay), desc="waiting..."):
		time.sleep(1)
	return activatedPackage


async def main():
	async with IPC(ipc=config["IPC"]["host"],
	               password=config["IPC"]["password"]) as asf:
		tries = 0
		while True:
			tries += 1
			activatedPackage = await activatePackages(asf, tries)
			if activatedPackage:
				break


loop = asyncio.get_event_loop()
output = loop.run_until_complete(main())
loop.close()
