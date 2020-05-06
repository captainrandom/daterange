from distutils.core import setup

setup(
    name='daterange',
    version='1.0',
    description='A cli too that generates a range of dates or timestamps',
    author='Mark Jackson',
    requires=['pendulum==2.0.5'],
    test_requires=['pytest']
)
