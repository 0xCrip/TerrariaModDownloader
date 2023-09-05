import requests
import os
import sys
import urllib3
from tqdm import tqdm
from termcolor import colored
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)
# Base URL for mod downloads and path to store mods
BASE_URL = 'https://mirror.sgkoi.dev/tModLoader/download.php?Down=mods/'  # Base of the website

debug = False  # Enables/Disables debug features


def find_terarria_mods_folder():
    possible_paths = [
        os.path.expanduser("~/Documents/My Games/Terraria/tModLoader/Mods"),
        os.path.expanduser("~/My Documents/My Games/Terraria/tModLoader/Mods"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


MODS_PATH = find_terarria_mods_folder() or 'D:/dfaul/Documents/My Games/Terraria/tModLoader/Mods'


def s_line():
    print('===========================================================================================================')


def s_line_color(color):
    line = colored(
        '===========================================================================================================',
        color)
    print(line)


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def confirm_exit():
    input('Press Enter to continue...')

def one_word(user_mod):
    words = user_mod.split()
    return len(words) == 1


def output_mods():
    print(colored('Terraria Mod Output', 'red', attrs=['bold', 'blink']))
    print('This program takes all the mods you have installed in your mod directory and then outputs them to a '
          'formatted file. \nThis can then be downloaded by someone else.')
    print(colored('Note: ',
                  'red') + 'Do not add file extensions to your file name. And the output links are not verified, '
                           'just a potential link.')
    print('Output will look like this: mod_name mod_url')
    s_line_color('green')
    output_file = input('What do you want to call the file?: ')
    if output_file == 'quit' or output_file == 'Quit':
        confirm_exit()
        clear_terminal()
    if '.txt' in output_file:
        output_file = output_file[:-4]
    installed_mods = [mod_file for mod_file in os.listdir(MODS_PATH) if
                      os.path.isfile(os.path.join(MODS_PATH, mod_file))]
    for mod_name in installed_mods:
        if '.tmod' in mod_name:
            url_check = f'{BASE_URL}{mod_name}'
            with open(f'{output_file}.txt', 'a') as file:
                file.write(f'{mod_name[:-5]} {url_check}\n')
                print(f'{mod_name} has been written to the file.')

def download_mod(mod_name):
    mod_url = f'{BASE_URL}{mod_name}.tmod'
    response = requests.get(mod_url, stream=True)

    if response.status_code == 200:
        if os.path.exists(f'{MODS_PATH}{mod_name}.tmod'):
            print(f'{mod_name} already installed. Skipping...')
        else:
            with open('InstallHistory.txt', 'a+') as history_file:
                lines = history_file.readlines()
                if any(mod_name in line for line in lines):
                    print(f'Mod "{mod_name}" already in history.')
                else:
                    history_file.write(f'{mod_name} {mod_url}\n')

                mod_path = os.path.join(MODS_PATH, f'{mod_name}.tmod')
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024  # 1 KB

                max_desc_width = 50  # Set a maximum width for the description
                truncated_mod_name = mod_name[:max_desc_width - 3] + "..." if len(
                    mod_name) > max_desc_width else mod_name

                with open(mod_path, 'wb') as file, tqdm(
                        desc=truncated_mod_name,  # Use the truncated name for description
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024,
                        ncols=80
                ) as bar:
                    for data in response.iter_content(block_size):
                        bar.update(len(data))
                        file.write(data)

            print(f'Mod "{mod_name}" downloaded ', colored('successfully', 'green'))

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
        if mod_url == "" or mod_url == "quit" or mod_url == "Quit":
            confirm_exit()
            clear_terminal()
        else:
            download_mod_with_url(mod_name, mod_url)


def download_mod_with_url(mod_name, mod_url):
    mod_path = f'{MODS_PATH}{mod_name}.tmod'
    response = requests.get(mod_url)
    if response.status_code == 200:
        with open(mod_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f'The {mod_name}:URL is not working. Are you sure it is valid?')

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
        confirm_exit()
        clear_terminal()
        sys.exit()

    input_file = input_file.replace('.txt', '')
    install_file = input_file + '.txt'
    if debug:
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
                    print("Invalid Line Format: ", line)
    except FileNotFoundError:
        print(f'No file by {install_file} has been found.')
    except Exception as e:
        print(f'An error occurred: {e}')

    print('Program complete: Please re-run to install more mods.')
    confirm_exit()
    clear_terminal()
    sys.exit()


def install_from_terminal():  # Option 1
    print(colored('Terraria Single File Installer',
                  'red', attrs=['bold', 'blink']))
    print('This section of the program installs Terraria mods from a mod website.')
    print('Note: Sometimes mod names are different from the title of the mod.')
    print('Example -> Title = AutoReforge | [[Mod Name]] = AutoReroll')
    print('Example -> Title = Elemental Unleash | [[Mod Name]] = Bluemagic')
    print('Not all mods are like this, just some.')
    print(
        'Also if the mod you want to install is something like "Calamity Mod (No Calamity Music)" anything in '
        'brackets should be ignored. \nTry to be as case sensitive as you can.')
    s_line_color('green')

    user_mod = input('Enter the name of the Terraria Mod: ')

    if user_mod == 'quit':
        confirm_exit()
        clear_terminal()
        sys.exit()

    mod_name = user_mod.strip()
    if not one_word(mod_name):
        mod_name = mod_name.title()

    mod_name = mod_name.replace(" ", "")

    destination_path = os.path.join(MODS_PATH, f'{mod_name}.tmod')
    print(f'Searching for: {user_mod}, please wait...')

    if os.path.exists(destination_path):
        print(f'The mod {mod_name} already exists.')
        s_line_color('green')
        extra = input('Do you want to install more mods? [Y/N]: ')
        if extra.lower() == 'n':
            sys.exit()
    else:
        download_mod(mod_name)


if __name__ == "__main__":
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colored('Terraria Mod Installer', 'red', attrs=['bold', 'blink']))
        print('The main aim of this program is to make it easy to install Terraria mods.')
        print('Either through the Mod name or through a friend\'s formatted mod list.')
        print('Select an option for more information.')
        s_line_color('green')

        option = input(
            colored('(1)', 'green') + '    => Install through the Terminal \n' +
            colored('(2)', 'green') + '    => Install mods through a formatted file \n' +
            colored('(3)', 'green') + '    => Output installed mods to a file \n' +
            colored('(Quit)', 'red') + ' => Quit the program\nChoose an option: ')

        if option == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            install_from_terminal()
        elif option == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            install_from_file()
        elif option == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            output_mods()
        elif option == 'quit':
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit()
        else:
            print("That is not an option, try again.")
