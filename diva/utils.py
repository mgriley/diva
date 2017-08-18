from jinja2 import Environment, PackageLoader

# Allow Jinja use without Flask
env = Environment(loader=PackageLoader('diva', 'templates'))

def render_template(filename, **variables):
    return env.get_template(filename).render(variables)


