# Claim free Steam  packages script

![claim-free-steam-packages Actions](https://api.meercode.io/badge/Luois45/claim-free-steam-packages?type=ci-score&lastDay=14)
[![Build executable with PyInstaller](https://github.com/Luois45/claim-free-steam-packages/actions/workflows/build.yml/badge.svg)](https://github.com/Luois45/claim-free-steam-packages/actions/workflows/build.yml)
[![Update the package_list.txt file](https://github.com/Luois45/claim-free-steam-packages/actions/workflows/update_package_list.yml/badge.svg)](https://github.com/Luois45/claim-free-steam-packages/actions/workflows/update_package_list.yml)
[![Last package list update](https://img.shields.io/github/last-commit/Luois45/claim-free-steam-packages/auto-update?label=Last%20package%20list%20update)](https://github.com/Luois45/claim-free-steam-packages/actions/workflows/update_package_list.yml)

[![DeepSource](https://deepsource.io/gh/Luois45/claim-free-steam-packages.svg/?label=active+issues&show_trend=true&token=eIo_r1Hx850IQIJEoUj3FaC5)](https://deepsource.io/gh/Luois45/claim-free-steam-packages/?ref=repository-badge)
[![Github All Releases](https://img.shields.io/github/downloads/Luois45/claim-free-steam-packages/total.svg)](https://tooomm.github.io/github-release-stats/?username=Luois45&repository=claim-free-steam-packages)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![built with: Python3](https://camo.githubusercontent.com/0d9fbff04202da688cc79c5ffe984bd171edf453b2e41e5e56e55202dd5bdbb2/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275696c74253230776974682d507974686f6e332d7265642e737667)](https://www.python.org/)

This script does automate the activation of free packages (games, movies, DLC, etc.) on Steam. It does register as much as possible free packages to you Steam account.
The regularly updated database contains more than 15,000 packages that will be added and available in the library forever after activation.

## Instruction of usage

1. Download the latest [ArchiSteamFarm](https://github.com/JustArchiNET/ArchiSteamFarm/releases/latest) release
2. Set up [ArchiSteamFarm](https://github.com/JustArchiNET/ArchiSteamFarm/wiki/Setting-up)
3. Download the [Windows executable](https://github.com/Luois45/claim-free-steam-packages/releases/latest) or just clone this repository
4. Execute the activate_packages script or executable
5. The script will create a activated_packages.txt and config.json file after execution. Don't edit or delete it unless you know what you're doing.
6. Have a look at the remaining time and wait for it to finish, it may take a while
7. Enjoy

## FAQ
**Why it take so long to complete the script?**

The Steam API is limited to 50 package activations per hour.

Have a look into these [instructions](docs/instructions-for-users-with-many-packages.md) if you do already own many steam packages.
 
**Why not all available packages will be registered to you account?**

Some of packages like DLC, require to activate first base game first. Some can be not available on you region, or have other restrict.

**Can i be banned for use this script?**

No, this is Steam built-in feature. This script does not violate service terms of usage. Use this at your own risk, the author assumes no responsibility.

**What's the point of this?**

If some of this free packages will be removed or will be paid at future, you still be able to play them for free. A few games when installed give you +1 Games on your profile.

**How often does the package list get updated?**

The package list gets updated every hour via GitHub Actions. This does have the disadvantage that it costs me something (Proxy & Server provider) but I'll try to keep it up.

**How do I choose the steam accounts the script should use?**

The script will use on default all steam account which are connected to your ASF installation. It is possible to configure it in the `config.json` by changing the IPC → account to the name of your accounts inside of ASF.

Default: `"accounts": ["ASF"]`

Example for configuration: `"accounts": ["Louis45", "Louis_45"]`

## Support & Contributing
Anyone is welcome to contribute. If you decide to get involved, please take a moment and check out the following:

* [Bug reports](.github/ISSUE_TEMPLATE/bug_report.md)
* [Feature requests](.github/ISSUE_TEMPLATE/feature_request.md)

If you want to support this project, you can help financing the Proxies and the Server for the GitHub Actions runner.

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/louis45)

## License

The code is under the [GPL-3.0 License](https://choosealicense.com/licenses/gpl-3.0/).
