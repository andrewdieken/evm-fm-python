from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name = 'evm-fm-python',
    version = '0.01.6',
    license='MIT',
    description = 'Environment variable manager for Mac',
    long_description = readme,
    long_description_content_type = "text/markdown",
    author = 'Andrew Dieken',
    author_email = 'andrewrd@live.com',
    url = 'https://github.com/andrewdieken/evm-fm-python',
    keywords = ['aws', 'environment', 'variable', 'manager', 'mac'],
    packages = ['evm_fm'],
    package_data = {'evm_fm': [
        'templates/*.plist'
    ]},
    install_requires=[
        'toml>=0.10.1',
        'ssm-parameter-store==19.11.0',
    ],
    entry_points={
        'console_scripts': [
            'evm_fm = evm_fm.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)