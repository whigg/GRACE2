import os
import sys
from setuptools import setup, find_packages
from tethys_apps.app_installation import custom_develop_command, custom_install_command

### Apps Definition ###
app_package = 'grace2'
release_package = 'tethysapp-' + app_package
app_class = 'grace2.app:Grace2'
app_package_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tethysapp', app_package)

### Python Dependencies ###
dependencies = []

setup(
    name=release_package,
    version='2.0.1',
    tags='&quot;Hydrology&quot;, &quot;Groundwater&quot;',
    description='The GRACE application is a visualization tool for GRACE global satellite data. It also provides visualization for global surface water, soil moisture, and groundwater data.',
    long_description='',
    keywords='',
    author='Travis McStraw',
    author_email='travis.mcstraw@gmail.com',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['tethysapp', 'tethysapp.' + app_package],
    include_package_data=True,
    zip_safe=False,
    install_requires=dependencies,
    cmdclass={
        'install': custom_install_command(app_package, app_package_dir, dependencies),
        'develop': custom_develop_command(app_package, app_package_dir, dependencies)
    }
)
