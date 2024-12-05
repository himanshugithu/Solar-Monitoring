from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.read().splitlines()

setup(
    name='solar_modbus',
    version='0.1.0',
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'solar_modbus=solar_modbus.main:run',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['config.json'],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='Solar Modbus Data Reader',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your-repo/solar-modbus',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)