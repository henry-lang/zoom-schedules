import os

def install_modules(modules):
    print('Installing needed modules...')
    for module in modules:
        print(f'Installing {module}...')
        os.system(f'python3 -m pip install {module} -q')