from setuptools import setup

# see https://packaging.python.org/tutorials/distributing-packages/

setup(
    name='diva',
    version='0.1.0',
    description='Analytics dashboards made simple',
    long_description='create a simple web analytics dashboard',
    url='https://github.com/mgriley/diva',
    author='Matthew Riley',
    author_email='mgriley97@gmail.com',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # TODO: double-check this
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='dashboard analytics plotting',
    packages=['diva'],
    include_package_data=True,
    # minimal project dependencies here
    # NB: not the same as requirements.txt b/c requirements.txt includes
    # things like wtine, gunicorn, sphinx, etc.
    install_requires=[
        'flask',
        'jsonschema',
        'dateutil',
        'matplotlib',
        'numpy',
        'pandas',
        'bokeh'
    ],
    # copy these files into the build
    # package_data= {
        # 'diva': [
            # 'static/*',
            # 'templates/*'
        # ]
    # },
    # TODO: double-check this
    python_requires='>=3',
    # can create an automatic script, for use on the console,
    # use this! (flask run probably uses this)
    # entry_points={}
)
