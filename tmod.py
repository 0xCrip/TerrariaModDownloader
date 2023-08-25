import requests
import os
import sys
from termcolor import colored

# Base URL for mod downloads and path to store mods
BASE_URL = 'https://mirror.sgkoi.dev/tModLoader/download.php?Down=mods/'
MODS_PATH = 'D:/dfaul/Documents/My Games/Terraria/tModLoader/Mods/'


# Function to print a separator line
def s_line():
    print('===========================================================================================================')


# Function to print a colored separator line
def s_line_color(color):
    line = colored(
        '===========================================================================================================',
        color)
    print(line)


# Function to clear the terminal
def clear_terminal():
    input('Press Enter to continue...')
    os.system('cls' if os.name == 'nt' else 'clear')


# Function to check if a string has only one word
def one_word(user_mod):
    words = user_mod.split()
    return len(words) == 1


# Function to download and install a mod
def download_mod(mod_name):
    mod_url = f'{BASE_URL}{mod_name}.tmod'
    response = requests.get(mod_url)
    if response.status_code == 200:
        if os.path.exists(f'{MODS_PATH}{mod_name}.tmod'):
            print(f'{mod_name} already installed. Skipping...')
        else:
            with open('modhistory.txt', 'a+') as history_file:
                lines = history_file.readlines()
                if any(mod_name in line for line in lines):
                    print(f'Mod "{mod_name}" already in history.')
                else:
                    history_file.write(f'{mod_name} {mod_url}\n')

                with open(os.path.join(MODS_PATH, f'{mod_name}.tmod'), 'wb') as file:
                    print(f'Downloading...')
                    file.write(response.content)

            print(f'Mod "{mod_name}" downloaded successfully.')
            extra = input('Do you want to install more mods? [Y/N]: ')
            if extra.lower() == 'n':
                sys.exit()
            elif extra == 'quit':
                clear_terminal()
                sys.exit()
    else:
        s_line_color('red')
        print(f'Failed to find mod: "{mod_name}"')
        print('Remember: Sometimes mod names are different from the title of the mod.')
        print('Example -> Title = AutoReforge | [[Mod Name]] = AutoReroll')
        print('Be as case-sensitive as you can.')
        s_line_color('red')

        # Ask the user to provide the mod URL
        print('Press enter to quit the program or')
        mod_url = input(f'Enter the URL for the "{mod_name}" mod: ')
        if mod_url == "":
            clear_terminal()
            quit()
        else:
            download_mod_with_url(mod_name, mod_url)


# Function to download mod with provided URL
def download_mod_with_url(mod_name, mod_url):
    mod_path = f'{MODS_PATH}{mod_name}.tmod'
    response = requests.get(mod_url)
    if response.status_code == 200:
        with open(mod_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f'The {mod_name}:URL is not working. Are you sure it is valid?')


# Function to install mods from a file
def install_from_file():  # Option 2
    print(colored('Terraria File Installer', 'red', attrs=['bold', 'blink']))
    print(
        'This program requires an existing wordlist, likely from a friend to be passed into the program. It will then '
        'download all mods your friend has installed.')
    print(colored('Note: ',
                  'red') + 'Make sure the files are formatted like this with a single line for each mod,\nwith a '
                           'space between the Mod name and URL.')
    print('Mod_Name Link_To_Mod_Download')
    print('Mod_Name Link_To_Mod_Download')
    print('etc')
    s_line_color('green')

    input_file = input(
        'Enter the text file name stored in the program\'s directory: ')
    if input_file == 'quit':
        clear_terminal()
        sys.exit()

    input_file = input_file.replace('.txt', '')
    install_file = input_file + '.txt'
    print('old file: ' + input_file)
    print('new file: ' + install_file)

    try:
        with open(install_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(" ")
                if len(parts) == 2:
                    name, url = parts
                    download_mod(name)
                else:
                    print("Invalid Line Format:", line)
    except FileNotFoundError:
        print(f'File {install_file} not found.')
    except Exception as e:
        print(f'An error occurred: {e}')

    print('Program complete: Please re-run to install more mods.')
    sys.exit()


# Function to install mods from the terminal
def install_from_terminal():  # Option 1
    print(colored('Terraria Single File Installer',
          'red', attrs=['bold', 'blink']))
    print('This section of the program installs Terraria files from a mod website.\nThis is done one at a time.')
    print('Note: Sometimes mod names are different from the title of the mod.')
    print('Example -> Title = AutoReforge | [[Mod Name]] = AutoReroll')
    print('Example -> Title = Elemental Unleash | [[Mod Name]] = Bluemagic')
    print('Not all mods are like this, just some.')
    print('Also be as case-sensitive as you can.')
    s_line_color('green')

    user_mod = input('Enter the name of the Terraria Mod: ')

    if user_mod == 'quit':
        clear_terminal()
        sys.exit()

    mod_name = user_mod.strip()
    if not one_word(mod_name):
        mod_name = mod_name.title()

    mod_name = mod_name.replace(" ", "")

    destination_path = os.path.join(MODS_PATH, f'{mod_name}.tmod')
    print(f'Searching for: {user_mod}, please wait...')

    if os.path.exists(destination_path):
        print(f'The file {mod_name}.tmod already exists.')
        s_line_color('green')
        extra = input('Do you want to install more mods? [Y/N]: ')
        if extra.lower() == 'n':
            sys.exit()
    else:
        download_mod(mod_name)

# def outputmods():


# Main Call
if __name__ == "__main__":
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colored('Terraria Mod Installer',
              'red', attrs=['bold', 'blink']))
        print('The main aim of this program is to make it easy to install Terraria mods.')
        print('Either through the Mod name or through a friend\'s formatted mod list.')
        print('Select an option for more information.')
        s_line_color('green')

        option = input(
            colored('(1)', 'green') + ' => Terminal \n' + colored('(2)', 'green') + ' => Install mods through a formatted file \n' + colored('(3)', 'green') + ' => Beta Feature for outputting installed mods to a file.' + '\nPlease choose an option: ')

        if option == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            install_from_terminal()
        elif option == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            install_from_file()
        elif option == 'quit':
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit()
