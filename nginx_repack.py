import re, os, sys

p_name = sys.argv[1]

results = []
start_path = []
BASE_PATH = os.getcwd()
NGINX_PATH = '/etc/nginx/sites-enabled'
BACK_PATH = BASE_PATH + f'/backup_temp/opt/domens'

# ResrMsk_domens.txt - перечень доменов
# RestMsk_nginx.conf - конфигурационный файл nginx
# template.txt - шаблон для записи конфигурации в nginx

os.system('systemctl stop nginx.service')

with open(BACK_PATH + f'/{p_name}_domens.txt', 'r') as domens,\
    open(NGINX_PATH + r'/default', 'r') as conf_file:
    domens = domens.readlines()
    finish_row = conf_file.readline()
    while finish_row != '# block_base_conf_finish\n':
        start_path.append(finish_row)
        finish_row = conf_file.readline()
    finish_path = conf_file.readlines()

    with open(BASE_PATH + r'/templates/template.txt', 'r') as nginx_temp:
        nginx_temp = nginx_temp.read()
        for domen in domens:
            domen = domen.strip()
            result = re.sub(r'project_name', sys.argv[1], nginx_temp)
            result2 = re.sub(r'name_host', domen, result)
            results.append(result2 + '\n')

with open(NGINX_PATH + r'/default', 'w') as conf_file:
    conf_file.write(''.join(start_path) + ''.join(results)\
                     + '\n' + finish_row + ''.join(finish_path))

os.system('systemctl start nginx.service')

