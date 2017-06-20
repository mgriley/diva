from setuptools import setup

setup(
    name='sample_name',
    version='1.0.0',
    description='sample python project',
    long_description='longer description',
    url='project homepage, use github link',
    author='Matthew Riley',
    author_email='mgriley97@gmail.com',
    license='MIT',
    # ensure to include these later (see distribution link)
    classifiers=[],
    keywords='sample dashboard analytics plotting',
    packages=['diy_dashboard'],
    include_package_data=True,
    # TODO list minimal project dependencies here
    install_requires=[
        'flask',
    ],
    # copy these files into the build
    package_data= {
        'diy_dashboard': ['static/*', 'templates/*']
    },
    # can create an automatic script, for use on the console,
    # use this! (flask run probably uses this)
    entry_points={
    }
)
