from setuptools import setup

setup(
    name='diva',
    version='0.1.0',
    description='dashboards made simple',
    long_description='create a dashboard of data retrieved from your server',
    url='https://github.com/mgriley/diva',
    author='Matthew Riley',
    author_email='mgriley97@gmail.com',
    license='MIT',
    # ensure to include these later (see distribution link)
    classifiers=[],
    keywords='sample dashboard analytics plotting',
    packages=['diva'],
    include_package_data=True,
    # TODO list minimal project dependencies here
    install_requires=[
        'flask',
    ],
    # copy these files into the build
    package_data= {
        'diva': ['static/*', 'templates/*']
    },
    # can create an automatic script, for use on the console,
    # use this! (flask run probably uses this)
    entry_points={
    }
)
