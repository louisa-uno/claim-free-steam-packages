import asyncio
import time

import requests
from ASF import IPC
from tqdm import tqdm


async def main():
	async with IPC(ipc='http://127.0.0.1:1242',
	               password='YOUR IPC PASSWORD') as asf:
		with open('package_list.txt', 'r') as f:
			apps = f.read().split(',')
		for app in tqdm(apps, desc='Activating licenses'):
			with requests.get(
			    'https://raw.githubusercontent.com/Luois45/claim-free-steam-packages/update-package_list/package_list.txt'
			) as f:
				aps = f.text.split(',')
			foundPackage = False
			for ap in aps:
				if app == ap:
					# print("\nPackage found in activated_packages")
					foundPackage = True
			if not foundPackage:
				# print("\nPackage not found in activated_packages")
				cmd = "!addlicense app/" + app
				activatedPackage = False
				tries = 10
				for i in range(tries):
					resp = await asf.Api.Command.post(body={'Command': cmd})
					if resp.success:
						print("\n" + resp.result.replace("\r\n", ""))
						successCodes = ["Items:", "Aktivierte IDs:"]
						if any(x in resp.result for x in successCodes):
							activatedPackage = True
							with open('activated_packages.txt', 'a') as f:
								f.write(app + ",")
							time.sleep(90)
							break
					else:
						print(f'\nError: {resp.message}')
					time.sleep(90)
				if not activatedPackage:
					time.sleep(90)


loop = asyncio.get_event_loop()
output = loop.run_until_complete(main())
loop.close()
