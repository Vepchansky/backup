import re, sys

p_name = sys.argv[1]
URLS_PATH = f'/opt/projects/{p_name}/{p_name}/{p_name}'

with open(URLS_PATH + '/urls.py', 'r') as urls_r:
    lines = urls_r.read()
    line = re.sub('\'admin/', '\'enter12/', lines)

with open(URLS_PATH + '/urls.py', 'w') as urls_w:
    urls_w.write(line)
