try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'Tomography Reconstruction Analysis and Characterization Routines',
	'author': 'Branden Kappes',
	'url': 'https://github.com/csm-adapt/tracr.git',
	'download_url': 'https://github.com/csm-adapt/tracr.git',
	'author_email': 'bkappes@mines.edu',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['tracr'],
	'scripts': ['bin/tracr'],
	'name': 'tracr',
}
setup(**config)	
