import re, os, sys

def webset(name_proj):
    PROJ_DIR = f'/opt/projects/{name_proj}/{name_proj}/deployment'
    VASS_DIR = '/etc/uwsgi/vassals'
    with open(os.getcwd() + '/deployment/clear_uwsgi.ini', 'r') as template_uwsgi:
        template_uwsgi = template_uwsgi.read()
        with open(f'{PROJ_DIR}/{name_proj}_uwsgi.ini', 'w') as proj_uwsgi:
            proj_uwsgi.write(re.sub('clear', name_proj, template_uwsgi))
    
    os.system(f'ln -s {PROJ_DIR}/{name_proj}_uwsgi.ini {VASS_DIR}/.')

if __name__ == "__main__":
    webset(sys.argv[1])
