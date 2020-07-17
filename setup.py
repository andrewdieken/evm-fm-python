from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name = 'evm-fm-python',
    packages = ['evm_fm'],
    version = '0.01.0',
    license='MIT',
    description = 'Environment variable manager for Mac',
    long_description = readme,
    long_description_content_type = "text/markdown",
    author = 'Andrew Dieken',
    author_email = 'andrewrd@live.com',
    url = 'https://github.com/andrewdieken/evm-fm-python',
    download_url = 'https://github.com/andrewdieken/evm-fm-python/archive/v0.01.0.tar.gz',
    keywords = ['aws', 'environment', 'variable', 'manager', 'mac'],
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
    ],
)