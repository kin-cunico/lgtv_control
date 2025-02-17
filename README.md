# LGTV Remote Controller for PC

I created this project to be able to turn on my LGTV and launch apps. The easiest part was turning on as LGTV can wake-on-LAN. 
The hardest part was making sure that the apps were launched corretly, and for the I tried different libraries, but the one tha worked for me was [aiopylgtv](https://github.com/basnijholt/aiopylgtv).

The GUI was created using [Tkinter](https://docs.python.org/3/library/tkinter.html).

At first I hard coded it to launch YouTube and Crunchyroll, however now we can launch any app that is installed in the Smart TV via getting the system id list. So, it should work for anyone with a Smart LGTV with WebOS on.

## Downloading and Installing

I have plans on shipping this project to Windows and Linux, however that may take some time since I want to change the project to include other commands and for it to have a beautiful finished look.

## Running Locally via CLI

1. You can clone this repository to use it locally: ```git clone https://github.com/kin-cunico/lgtv_control.git```
2. Change to cloned directory: ```cd lgtv_control```
3. before running the project, you will need to change in the ```main.py``` file the ```TV_IP``` and the ```TV_MAC``` to reflect your own tv. Then you will need to create a file for your ```TV key```.
4. Run the pair_tv.py file to get your initial TV key: ```python pair_tv.py```
5. Run the main.py file to use the controller: ```python main.py```

## Licensing

This project is licensed under the Apache 2: [LICENSE](LICENSE).

To check the licensing for Tkinter and aiopylgtv, please check their github repositories. 
