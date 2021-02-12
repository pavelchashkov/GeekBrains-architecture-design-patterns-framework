import os
from jinja2 import Template

def render(name, folder='templates', **kwargs):
    with open(os.path.join(folder, f'{name}.html'), encoding='utf-8') as f:
        templ = Template(f.read())
    return templ.render(**kwargs)