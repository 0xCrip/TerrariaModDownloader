# TerrariaModDownloader

## Description

A script designed to make downloading scripts on Terraria relatively easy. It come with 3 options.
1. Install files by Name or URL. Note: Name does not always work because names and links are not all linked up on the mod websites, so that is why I added the URL input for a backup for those links. This is not very often this happens.
2. Install files through a friends mod output document. Which I am currently writing and coming soon. The aim of that will be to output the name and URL of all mods installed and then that document can be used with this program.
3. Current Beta feature that allows users to output their currently installed mods to a file.txt --> The goal of this is to then share this txt with a friend and then use it in option 2 to install all the mods your friend has.

## Getting Started
Download the GitHub Zip or Clone the Repository.
### Dependencies
There are none. All the python imports are local.
* Only been tested on Windows 11

### Installing

* In the program you will need to change your 'MODS_PATH' with your own tModLoader mods folder. Usually located at D:\YourUsername\Documents\My Games\Terraria\tModLoader\Mods
* Change the second option for this variable to your own directory. It will likely just be changing the username.
```
MODS_PATH = find_terarria_mods_folder() or 'D:/USERNAME/Documents/My Games/Terraria/tModLoader/Mods'
```

### Executing program

* Just open Command Terminal, navigate to the program folder and use the below command --This may be a little different depending on your python version.
```
python3 main.py
```

## Help
No issues or bugs noticed so far. Let me know if you find any.

## Authors

Contributors names and contact info

Discord -> Criptik_01#6722

## Version History

* 0.1
    * Initial Release

## Acknowledgments
*  None so far, if you do repost this project in any way. Please leave my name on it as I did work on this by myself. Thanks.
