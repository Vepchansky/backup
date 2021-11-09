import re, os, sys

p_name = sys.argv[1]
SETTINGS_PATH = f'/opt/projects/{p_name}/{p_name}/{p_name}/settings'
BASE_PATH = os.getcwd()
BACK_PATH = BASE_PATH + f'/backup_temp/opt/domens'
TEMP1 = 'ALLOWED_HOSTS = [\'*\']'
TEMP2 = 'ALLOWED_HOSTS = ['
TEMP3 = 'ALLOWED_HOSTS = [\'localhost\']'

start_dev = []
start_prod = []
dev_result = []
prod_result = []

with open(BACK_PATH + f'/{p_name}_domens.txt', 'r') as domens_txt:
    domens = domens_txt.readlines()

# СОСТАВЛЕНИЕ ЧАСТЕЙ dev.py + домены

with open(SETTINGS_PATH + '/dev.py', 'r') as dev:
    allow_host_dev = dev.readline()
    while 'ALLOWED_HOSTS' not in allow_host_dev:
        start_dev.append(allow_host_dev)
        allow_host_dev = dev.readline()
    finish__dev = dev.readlines()
    for domen in domens:
        domen = domen.strip()
        dev_result.append('    \'' + domen + '\',')

# СОСТАВЛЕНИЕ ЧАСТЕЙ prod.py + домены

with open(SETTINGS_PATH + '/prod.py', 'r') as prod:
    allow_host_prod = prod.readline()
    while 'ALLOWED_HOSTS' not in allow_host_prod:
        start_prod.append(allow_host_prod)
        allow_host_prod = prod.readline()
    finish_prod = prod.readlines()
    for domen in domens:
        domen = domen.strip()
        prod_result.append('    \'' + domen + '\',')

# Запись измененного DEV.PY

with open(SETTINGS_PATH + '/dev.py', 'w') as dev:
    if allow_host_dev.strip() == TEMP1:
        dev.write(''.join(start_dev) + 'ALLOWED_HOSTS = [\n' + '\n'.join(dev_result)\
              + '\n]\n' + ''.join(finish__dev))
    elif allow_host_dev.strip() == TEMP2:
        dev.write(''.join(start_dev) + 'ALLOWED_HOSTS = [\n' + '\n'.join(dev_result)\
              + '\n' + ''.join(finish__dev))

# Запись измененного PROD.PY

with open(SETTINGS_PATH + '/prod.py', 'w') as prod:
    if allow_host_prod.strip() == TEMP3:
        prod.write(''.join(start_prod) + 'ALLOWED_HOSTS = [\n' + '\n'.join(prod_result)\
              + '\n]\n' + ''.join(finish_prod))
    elif allow_host_prod.strip() == TEMP2:
        prod.write(''.join(start_prod) + 'ALLOWED_HOSTS = [\n' + '\n'.join(prod_result)\
              + '\n' + ''.join(finish_prod))
