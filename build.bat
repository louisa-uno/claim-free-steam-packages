del dist\activate_packages.exe
del dist\activate_packages-headless.exe
pyinstaller activate_packages.py -F -n activate_packages
pyinstaller activate_packages.py -F -n activate_packages-headless -w
