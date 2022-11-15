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

logging.basicConfig(
    filename="logging.txt",
    filemode="w",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.WARNING,
)

log = logging.getLogger("urbanGUI")


def load_config():
    try:
        with open("config.json", encoding="utf8") as file:
            loaded_config = json.load(file)
            return loaded_config
    except FileNotFoundError:
        return create_config()
    except json.decoder.JSONDecodeError:
        print(
            "Config file is not valid JSON. Please delete the config file and run the script again.",
        )
        sys.exit(0)


def get_username_input_sentence():
    sentence = "Enter your steam username to download IDs of owned games to skip them when activating packages."
    sentence += "\nIf you don't want to enter your username just leave it empty and press enter."
    sentence += "\nThe steam username is the username in the url when opening your steam profile."
    sentence += "\nexample: https://steamcommunity.com/id/Louis_45/ → Louis_45 is the steam username"
    sentence += "\nYour Steam username:"
    return sentence


def create_config():
    my_config = {
        "IPC": {
            "host": "http://localhost:1242",
            "password": "your IPC password",
            "accounts": ["ASF"],
        },
        "STEAM": {"username": "your STEAM username"},
        "repeat_hour_delay": "2",
    }
    my_config["IPC"]["host"] = input("Enter your ArchiSteamFarm host address: ")
    my_config["IPC"]["password"] = input("Enter your ArchiSteamFarm host password: ")
    my_config["STEAM"]["username"] = input(get_username_input_sentence())
    log.debug("Saving config file")
    with open("config.json", "w", encoding="utf8") as file:
        file.write(json.dumps(my_config))
    log.debug("Saved config file")
    return my_config


config = load_config()


async def activate_packages(asf, tries):
    url = "https://raw.githubusercontent.com/Luois45/claim-free-steam-packages/auto-update/package_list.txt"
    with requests.get(url) as file:
        package_list = file.text.split(",")
        print(f"Downloaded repo package list with {len(package_list)} free packages.")

    activated_package = False
    try:
        with open("activated_packages.txt", encoding="utf8") as file:
            activated_packages = file.read().split(",")
    except FileNotFoundError:
        with open("activated_packages.txt", "w", encoding="utf8") as file:
            log.info("Created activated_packages file")
            steam_username = config["STEAM"]["username"]
            if steam_username not in {"", "your STEAM username"}:
                with requests.get(
                    f"https://steamcommunity.com/id/{steam_username}/games/?tab=all",
                ) as response:
                    html = response.text
                    regex = re.compile(r'"appid":(\d+),')
                    results_list = regex.findall(html)
                    log.info(
                        "Fetched %s packages to activated_packages.txt using Steam Username",
                        len(results_list),
                    )
                    results = ""
                    for result in results_list:
                        results += result + ","
                    file.write(results)
                    del results
                    del results_list
        with open("activated_packages.txt", encoding="utf8") as file:
            activated_packages = file.read().split(",")

    apps = []
    for app in package_list:
        if app not in activated_packages:
            apps.append(app)
    random.shuffle(apps)

    if len(apps) > 0:
        print(
            f"Out of {len(package_list)} known free packages, {len(apps)} are not owned. Beginning activation.",
        )

        for app in tqdm(apps, desc=f"{tries} attempt: Activating licenses"):

            cmd = "!addlicense " + ",".join(config["IPC"]["accounts"]) + " app/" + app
            resp = await asf.Api.Command.post(body={"Command": cmd})

            if resp.success:
                log.info(resp.result.replace("\r\n", ""))
                success_codes = ["Items:", "Aktivierte IDs:"]

                if any(x in resp.result for x in success_codes):
                    activated_package = True
                    with open("activated_packages.txt", "a", encoding="utf8") as file:
                        file.write(app + ",")
            else:
                log.info("Error: %s", resp.message)
            time.sleep(74)
    else:
        print(
            f"Out of {len(package_list)} known free packages, all are already activated. Skipping activation phase.",
        )
    del activated_packages
    del package_list
    delay = int(config["repeat_hour_delay"]) * 3600
    print(
        f"Waiting {config['repeat_hour_delay']} hours to check for new free packages.",
    )
    for _ in tqdm(range(delay), desc="waiting..."):
        time.sleep(1)
    return activated_package


async def main():
    async with IPC(
        ipc=config["IPC"]["host"],
        password=config["IPC"]["password"],
    ) as asf:
        tries = 0
        while True:
            tries += 1
            activated_package = await activate_packages(asf, tries)
            if activated_package:
                break


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
