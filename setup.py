from setuptools import setup, find_packages

setup(
    name='gui_script_interface_pkg',
    version='0.1',
    packages=find_packages(),
    description='A GUI script interface with shared memory management',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Cromwell Abiori',
    author_email='cromwell.abiori@hanwha-phasor.com',
    url='https://github.com/cromwellcv/gui_script_interface_pkg',
    install_requires=[
        'pyserial',  # Add any other dependencies your package needs
    ],
)
