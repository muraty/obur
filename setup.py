import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


version = '0.0.4'

setup(
    name='obur',
    version=version,
    packages=['obur'],
    install_requires=[
        'librato-metrics==0.4.9',
        'requests==2.12.4',
        'statsd==3.2.1'],
    include_package_data=True,
    license='BSD License',
    description='A minimalistic speed test library.',
    long_description=README,
    keywords='speedtest speed obur',
    url='http://github.com/muraty/obur',
    author='Omer Murat Yildirim',
    author_email='omermuratyildirim@gmail.com',
    entry_points={
        'console_scripts': [
            'obur = obur.cli:main',
        ]
    }
)
