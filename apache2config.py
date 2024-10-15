#!/usr/bin/env python3

import os
import re

def display_menu():
    print("Menu:")
    print("1. Set Apache2 and php root dir / DocumentRoot location")
    print("2. Set permissions of contents of root dir")
    print("3. Open Apache2.conf")
    print("4. Open php.ini")
    print("5. Restart apache2")
    print("6. Exit")

def main():
    while True:
        display_menu()
        choice = input("Please select an option (1-6): ")
        os.system('cls' if os.name == 'nt' else 'clear')
        # Paths to the configuration files
        apache_conf_path = "/etc/apache2/sites-available/000-default.conf"
        apache2_conf_path = "/etc/apache2/apache2.conf"
        php_ini_path = find_php_ini_path()
        
        if choice == '1':
            os.system('sudo nano ' + apache_conf_path)
            os.system('sudo systemctl restart apache2')
            
        elif choice == '2':
            documentroot = get_apache_document_root()
            #print(documentroot)
            print("Enter the permission code you want for " + documentroot + " and its contents.")
            print("777 - makes everyone able to read/write - Everything for Everyone")
            print("700 - makes only the owner have permissions")
            print("755 - Only owner can write, read and execute for everyone else")
            print("666 - Owner, group and everyone else can read/write, nobody can execute")
            print("Keep in mind, often you will want to be able to modify the contents of this directory from time to time if you're actively developing the files within it, so you may want write permissions.")
            print("Otherwise, you'll be required to use sudo any time you want to make changes here if you don't have write permissions.")
            print("So, what'll it be?")
            permissionlevel = input()
            os.system('sudo chmod -R ' + permissionlevel + ' ' + documentroot)
            os.system('sudo systemctl restart apache2')
            print("Permissions set, apache2 restarted.")
            break
        elif choice == '3':
            print("Opening Apache2 main config...")
            os.system('sudo nano ' + apache2_conf_path)
            
        elif choice == '4':
            print("Opening php.ini...")
            os.system(' sudo nano ' + php_ini_path)
            # Add your code here to open php.ini
        elif choice == '5':
            os.system('sudo systemctl restart apache2')
            #break
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


def get_apache_document_root():
    apache_conf_path = '/etc/apache2/sites-available/000-default.conf'
    
    try:
        with open(apache_conf_path, 'r') as file:
            for line in file:
                # Strip whitespace and check for DocumentRoot directive
                stripped_line = line.strip()
                if stripped_line.startswith("DocumentRoot"):
                    # Split the line and return the directory path
                    return stripped_line.split()[1].strip('"')
                elif stripped_line.startswith("#"):  # Skip comments
                    continue

    except FileNotFoundError:
        print(f"Error: The file {apache_conf_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("DocumentRoot not found in the configuration file.")
    return None

def update_apache_config(apache_conf_path):
    # Read the current configuration
    with open(apache_conf_path, 'r') as file:
        config = file.readlines()

    # Update the DocumentRoot directive
    for i, line in enumerate(config):
        if line.startswith("DocumentRoot"):
            config[i] = f"DocumentRoot \"{rootdir}\"\n"
            break

    # Write the updated configuration back to the file
    with open(apache_conf_path, 'w') as file:
        file.writelines(config)

def update_php_ini(php_ini_path):
    # Read the current php.ini configuration
    with open(php_ini_path, 'r') as file:
        config = file.readlines()

    # Update the upload_tmp_dir directive (or any other relevant directive)
    for i, line in enumerate(config):
        if line.startswith("upload_tmp_dir"):
            config[i] = f"upload_tmp_dir = \"{rootdir}\"\n"
            break

    # Write the updated configuration back to the file
    with open(php_ini_path, 'w') as file:
        file.writelines(config)



def find_php_ini_path():
    php_dir = '/etc/php'
    highest_version = ''
    php_ini_path = ''

    # List all directories in /etc/php
    for version in os.listdir(php_dir):
        # Check if the directory name matches the PHP version pattern
        if re.match(r'^\d+\.\d+$', version):
            # Compare versions to find the highest one
            if version > highest_version:
                highest_version = version

    # Construct the path to php.ini for the highest version found
    if highest_version:
        php_ini_path = os.path.join(php_dir, highest_version, 'apache2', 'php.ini')
        if not os.path.exists(php_ini_path):
            php_ini_path = os.path.join(php_dir, highest_version, 'cli', 'php.ini')

    return php_ini_path

if __name__ == "__main__":
    main()


