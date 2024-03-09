import os
import json
from PyInstaller.__main__ import run as pyinstaller_run
import ctypes
from ctypes import wintypes
import pythoncom
from win32com.client import Dispatch, constants


CONFIG_FILE = "easyexe-config.json"
welcome_art = r"""

███████  █████  ███████ ██    ██ ███████ ██   ██ ███████ 
██      ██   ██ ██       ██  ██  ██       ██ ██  ██      
█████   ███████ ███████   ████   █████     ███   █████   
██      ██   ██      ██    ██    ██       ██ ██  ██      
███████ ██   ██ ███████    ██    ███████ ██   ██ ███████ 
                                                         
                                                         
    """


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def save_config(config):
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file, indent=4)


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as config_file:
            return json.load(config_file)
    return {}


def set_file_properties(file_path, properties):
    pythoncom.CoInitialize()
    try:
        # Load the DLL
        ctypes.windll.kernel32.SetFileAttributesW(file_path, 0)
        # Open the file to set properties
        handle = ctypes.windll.kernel32.CreateFileW(file_path, ctypes.c_uint32(0x10000000), ctypes.c_uint32(0), None,
                                                    ctypes.c_uint32(3), ctypes.c_uint32(0x80), None)
        # Set properties
        for key, value in properties.items():
            prop_key = key.encode('utf-16le')
            prop_value = value.encode('utf-16le')
            # Use wintypes.LPWSTR for Unicode strings
            ctypes.windll.kernel32.SetFileInformationByHandle(handle, 22, wintypes.LPWSTR(prop_key), len(prop_key))
            ctypes.windll.kernel32.SetFileInformationByHandle(handle, 23, wintypes.LPWSTR(prop_value), len(prop_value))
        # Close the file handle
        ctypes.windll.kernel32.CloseHandle(handle)
    finally:
        pythoncom.CoUninitialize()


def convert_py_to_exe(script_path, create_onefile=False, create_windowed=False, custom_name=None, custom_distpath=None,
                      custom_icon=None, file_properties=None):
    if not os.path.exists(script_path):
        clear_console()
        print(welcome_art)
        print(f"The specified script does not exist: {script_path}")
        return
    try:
        # Build options based on user input
        options = [script_path]
        if create_onefile:
            options.append('--onefile')
        if create_windowed:
            options.append('--windowed')
        if custom_name:
            options.extend(['--name', custom_name])
        if custom_distpath:
            options.extend(['--distpath', custom_distpath])
        if custom_icon:
            options.extend(['--icon', custom_icon])
        # Run PyInstaller with the specified options
        pyinstaller_run(options)
        clear_console()
        print(welcome_art)
        print(f"Successfully converted {script_path} to an executable.")
        # Set file properties
        if file_properties:
            set_file_properties(os.path.join(custom_distpath, f"{custom_name}.exe"), file_properties)
        # Save configuration to the cache file
        config = {
            'script_path': script_path,
            'create_onefile': create_onefile,
            'create_windowed': create_windowed,
            'custom_name': custom_name,
            'custom_distpath': custom_distpath,
            'custom_icon': custom_icon,
            'file_properties': file_properties
        }
        save_config(config)
    except Exception as e:
        clear_console()
        print(welcome_art)
        print(f"An unexpected error occurred: {e}")


def get_user_input():
    # Load configuration from the cache file
    config = load_config()
    clear_console()
    print(welcome_art)
    script_path_input = input(f"Enter the path to your Python script [{config.get('script_path', '')}]: ").strip(
        '"') or config.get('script_path', '')
    use_json_details = input("Do you want to use file details from the JSON file? (y/n) [y]: ").lower() != 'n'
    if use_json_details:
        file_properties = config.get('file_properties', {})
    else:
        file_properties = {}
        print("\nEnter file properties (press Enter to skip):")
        file_properties['FileDescription'] = input(
            f"File Description [{config.get('file_properties', {}).get('FileDescription', '')}]: ").strip() or config.get(
            'file_properties', {}).get('FileDescription', '')
        file_properties['FileVersion'] = input(
            f"File Version [{config.get('file_properties', {}).get('FileVersion', '')}]: ").strip() or config.get(
            'file_properties', {}).get('FileVersion', '')
        file_properties['ProductName'] = input(
            f"Product Name [{config.get('file_properties', {}).get('ProductName', '')}]: ").strip() or config.get(
            'file_properties', {}).get('ProductName', '')
        file_properties['ProductVersion'] = input(
            f"Product Version [{config.get('file_properties', {}).get('ProductVersion', '')}]: ").strip() or config.get(
            'file_properties', {}).get('ProductVersion', '')
        file_properties['LegalCopyright'] = input(
            f"Copyright [{config.get('file_properties', {}).get('LegalCopyright', '')}]: ").strip() or config.get(
            'file_properties', {}).get('LegalCopyright', '')
        file_properties['Language'] = input(
            f"Language [{config.get('file_properties', {}).get('Language', '')}]: ").strip() or config.get(
            'file_properties', {}).get('Language', '')
    # Other user choices
    clear_console()
    print(welcome_art)
    print("\nEnter options (press Enter to skip):")
    create_onefile = input("Create a single executable file (--onefile)? (y/n) [n]: ").lower() == 'y'
    create_windowed = input("Create a windowed (GUI) executable (--windowed)? (y/n) [n]: ").lower() == 'y'
    custom_name_input = input(
        f"Enter a custom name for the executable (press Enter to skip) [{config.get('custom_name', '')}]: ").strip() or config.get(
        'custom_name', '')
    custom_distpath_input = input(
        f"Enter a custom output directory for the executable (press Enter to skip) [{config.get('custom_distpath', '')}]: ").strip() or config.get(
        'custom_distpath', '')
    custom_icon_input = input(
        f"Enter the path to a custom icon for the executable (press Enter to skip) [{config.get('custom_icon', '')}]: ").strip() or config.get(
        'custom_icon', '')
    # Save user choices to configuration
    config.update({
        'custom_name': custom_name_input,
        'custom_distpath': custom_distpath_input,
        'custom_icon': custom_icon_input,
        'file_properties': file_properties
    })
    save_config(config)

    return script_path_input, create_onefile, create_windowed, custom_name_input, custom_distpath_input, custom_icon_input, file_properties


if __name__ == "__main__":
    script_path, create_onefile, create_windowed, custom_name, custom_distpath, custom_icon, file_properties = get_user_input()
    convert_py_to_exe(
        script_path=script_path,
        create_onefile=create_onefile,
        create_windowed=create_windowed,
        custom_name=custom_name,
        custom_distpath=custom_distpath,
        custom_icon=custom_icon,
        file_properties=file_properties
    )
