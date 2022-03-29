from pathlib import Path
from setuptools import setup, find_packages
from platform import system
from subprocess import call, check_output, CalledProcessError

# Install PyAudio with pipwin.
if system() == "Windows":
    try:
        check_output(["pip3", "show", "pipwin"])
        has_pipwin = True
    except CalledProcessError:
        has_pipwin = False
    # Install pipwin.
    if not has_pipwin:
        call(["pip3", "install", "pipwin"])
    # Install PyAudio.
    call(["pip3", "install", "pyaudio"])
    # Assume that we don't want pipwin and uninstall it.
    if not has_pipwin:
        call(["pip3", "uninstall", "pipwin"])
# Run the rest of the setup.
setup(
    name='baby_monitor',
    version="1.1.0",
    description='A simple local baby monitor',
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/subalterngames/baby_monitor',
    author_email='subalterngames@gmail.com',
    author='Seth Alter',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords='baby monitor pygame',
    install_requires=["flask", "numpy", "pygame", "requests", "pillow", "netifaces", "pyaudio"],
)
