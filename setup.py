from setuptools import find_packages, setup

setup(
    name='daterange.py',
    version='1.0.0',
    description='A cli too that generates a range of dates or timestamps',
    author='Mark Jackson',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['daterange=date_range.daterange:main']
    },
    install_requires=['pendulum==2.0.5'],
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
)
