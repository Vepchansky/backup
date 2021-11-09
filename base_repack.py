import re, sys

p_name = sys.argv[1]
SETTINGS_PATH = f'/opt/projects/{p_name}/{p_name}/{p_name}/settings'

with open('templates/base_template.template', 'r') as b_temp:
    b_temp = b_temp.read()
    result = re.sub('temp_name_proj', p_name, b_temp)
    result2 = re.sub('temp_name_db', p_name.lower(), result)

with open(SETTINGS_PATH + '/base.py', 'w') as base_py:
    base_py.write(result2)
