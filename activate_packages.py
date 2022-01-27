import asyncio
import time

from ASF import IPC


async def command(asf, cmd):
	return await asf.Api.Command.post(body={'Command': cmd})


async def main():
	# The IPC initialization duration depends on the network
	async with IPC(ipc='http://127.0.0.1:1242',
	               password='YOUR IPC PASSWORD') as asf:
		with open('package_list.txt', 'r') as f:
			apps = f.read().split(',')
		for app in apps:
			try:
				with open('activated_packages.txt', 'r') as f:
					aps = f.read().split(',')
			except FileNotFoundError:
				with open('activated_packages.txt', 'w') as f:
					print("Created activated_packages file")
					aps = []
			foundPackage = False
			for ap in aps:
				if app == ap:
					print("Package found in activated_packages")
					foundPackage = True
			if not foundPackage:
				print("Package not found in activated_packages")
				cmd = "!addlicense app/" + app
				activatedPackage = False
				tries = 10
				for i in range(tries):
					resp = await command(asf, cmd)
					if resp.success:
						print(resp.result)
						successCodes = ["Items:", "Aktivierte IDs:"]
						if any(x in resp.result for x in successCodes):
							activatedPackage = True
							with open('activated_packages.txt', 'a') as f:
								f.write(app + ",")
							time.sleep(20)
							break
					else:
						print(f'Error: {resp.message}')
					time.sleep(20)
				if not activatedPackage:
					time.sleep(20)


loop = asyncio.get_event_loop()
output = loop.run_until_complete(main())
loop.close()
