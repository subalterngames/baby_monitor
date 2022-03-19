from subprocess import call
from platform import system
from setuptools import setup, find_packages


if system() == "Windows":
    call(["pip3", "install", "pipwin"])
    call(["pipwin", "install", "pyaudio"])


setup(
    name='baby_monitor',
    version="0.0.1",
    description='A simple local baby monitor',
    long_description='TODO',
    long_description_content_type='text/markdown',
    url='https://github.com/subalterngames/baby_monitor',
    author_email='subalterngames@gmail.com',
    author='Seth Alter',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords='baby monitor pygame pyaudio',
    install_requires=["pyaudio", "numpy", "pygame", "requests", "pillow"],
)
