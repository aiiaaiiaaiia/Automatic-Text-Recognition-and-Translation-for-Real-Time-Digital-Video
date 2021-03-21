from setuptools import find_packages, setup
setup(
    name='rt_atrt_lib',
    packages=find_packages(include=['rt_atrt_lib']),
    version='0.1.2',
    description='My first Python library',
    author='Me',
    license='MIT',
    package_data={'rt_atrt_lib': ['resources/*.ttf']},
    include_package_data=True
)