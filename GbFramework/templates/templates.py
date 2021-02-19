from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment


def render(name, folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    tmpl = env.get_template(f'{name}.html')
    return tmpl.render(**kwargs)
