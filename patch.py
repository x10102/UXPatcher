import hashlib
from shutil import copy, move
from os import getenv
from os.path import join

UXINIT_PATH = join(getenv('SystemDrive')+'\\', 'Windows', 'System32', 'uxinit.dll')
THEMEUI_PATH = join(getenv('SystemDrive')+'\\', 'Windows', 'System32', 'themeui.dll')

def green(text):
    return f'\033[0;32m{text}\033[0m'

def red(text):
    return f'\033[0;31m{text}\033[0m'

def yellow(text):
    return f'\033[0;33m{text}\033[0m'

logo = f"""
╔══════════════════════════════════════════════════════════════════╗
║  ██████ ██████   █████   ██████ ██   ██ ████████ ███████ ██   ██ ║
║ ██      ██   ██ ██   ██ ██      ██  ██     ██    ██      ██  ██  ║
║ ██      ██████  ███████ ██      █████      ██    █████   █████   ║
║ ██      ██   ██ ██   ██ ██      ██  ██     ██    ██      ██  ██  ║
║  ██████ ██   ██ ██   ██  ██████ ██   ██    ██    ███████ ██   ██ ║
╠══════════════════════════════════════════════════════════════════╣
║ => https://github.com/x10102/UXPatcher                           ║
║ => {yellow("USE AT YOUR OWN RISK!")}                                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

themeui = {
    '0ddecc3fa8292afad5cfc615b34e0b2ce6b72f87': {
        'output': '7eb3a56a6b172a259f05d12ccb3ba6f94bbcab44',
        'patches': [
            {
                "offset": 0x0005A5A2,
                "length": 2,
                "data": b'\x90\x90'
            },
            {
                "offset": 0x0005A5D6,
                "length": 2,
                "data": b'\x90\x90'
            }
        ],
        'version': "Windows 10 Home 22H2 build 19045.4529"
    },
}

uxinit = {
    '1f56fbf493c393d0d9e4e1beb48589cfb6e27cbc': {
        'output': 'b306014be22e4017bfc0ba258b971ba9aef37dfb',
        'patches': [
            {
                "offset": 0x00014d4e,
                "length": 2,
                "data": b'\x90\x90'
            },
            {
                "offset": 0x00014d82,
                "length": 2,
                "data": b'\x90\x90'
            }
        ],
        'version': "Windows 10 Home 22H2 build 19045.4529"
    },
}

def patch_file(filename, output_name, patch_info):
    print(f'=> Reading {filename}')

    try:
        with open(filename, 'r+b') as dll:
            dll.seek(0)
            data = bytearray(dll.read())
    except FileNotFoundError:
        print(red('=> File not found'))
        exit(0)
    except Exception:
        print(red('=> I/O Error, check permissions'))

    print('=> Checking hashes')
    file_hash = hashlib.sha1(data).hexdigest()
    if file_hash not in patch_info:
        print(red('=> ERROR: Hash mismatch. File was probably updated or patched before, submit an issue on github.'))
        exit(0)
    else:
        current_ver = patch_info[file_hash]
        print(f'=> Hash OK, detected version: {current_ver["version"]}')

    for patch_idx, patch in enumerate(current_ver['patches']):
        print(yellow(f'=> Patching {patch_idx+1} of {len(current_ver["patches"])}'))
        for i in range(patch['length']):
            data[patch['offset']+i] = patch['data'][i]

    print('=> Writing output')
    with open(output_name, 'wb') as newfile:
        newfile.write(data)

    with open(output_name, 'rb') as newfile:
        print('=> Checking hashes')
        if(hashlib.sha1(newfile.read()).hexdigest() != current_ver['output']):
            print(red('=> ERROR: Hash mismatch. Unknown error. DO NOT USE THE GENERATED FILE.'))
            exit(0)
        else:
            print(green(f'=> Patched {filename}'))

def copy_files():
    print('=> Copying files')
    try:
        copy(UXINIT_PATH, '.')
        copy(THEMEUI_PATH, '.')
    except Exception:
        print(red('=> Unable to copy files, check permissions'))

def cleanup():
    print('=> Cleaning up')
    try:
        move('uxinit.dll', 'uxinit.dll.backup')
        move('themeui.dll', 'themeui.dll.backup')
        move('uxinit.patched.dll', 'uxinit.dll')
        move('themeui.patched.dll', 'themeui.dll')
    except Exception:
        print(red('=> Error renaming files, check permissions'))

if __name__ == '__main__':
    print(logo)
    copy_files()
    patch_file('themeui.dll', 'themeui.patched.dll', themeui)
    patch_file('uxinit.dll', 'uxinit.patched.dll', uxinit)
    cleanup()
    print(green('=> Patcher done'))
    print(yellow('=> Now boot into safe mode / installer and replace files'))