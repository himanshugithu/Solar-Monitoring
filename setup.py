from setuptools import setup, find_packages
# install_requires=read_requirements(),

def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.read().splitlines()

setup(
    name='solar_monitoring',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "certifi==2024.8.30",
        "charset-normalizer==2.0.12",
        "idna==3.10",
        "pymodbus==2.5.3",
        "pyserial==3.5",
        "requests==2.27.1",
        "schedule==1.2.2",
        "six==1.16.0",
        "urllib3==1.26.20",
        ],
    entry_points={
        'console_scripts': [
            'solar-monitoring=solar_monitoring.main:run',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['config.json'],
    },
    author='Surya Suhaas',
    author_email='mssuhaas@gmail.com',
    description='Solar Modbus Data Reader',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/himanshugithu/Solar-Monitoring',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)