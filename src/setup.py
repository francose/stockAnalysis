from setuptools import setup


setup(
    name='stockAnalysis',
    version='0.1',
    description='',
    url='',
    author='Sadik Erisen',
    license='MIT',
    packages=['stockAnalysis'],
    keywords='stocks, finance, market, S&P500',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business :: Financial'
    ],
    install_requires=[
        'aiohttp == 3.5.4',
        'async-timeout == 3.0.1',
        'attrs == 19.1.0',
        'beautifulsoup4 == 4.7.1',
        'certifi == 2018.11.29',
        'chardet == 3.0.4',
        'cycler == 0.10.0',
        'idna == 2.8',
        'idna-ssl == 1.1.0',
        'kiwisolver == 1.0.1',
        'multidict == 4.5.2',
        'numpy == 1.16.1',
        'pandas == 0.24.1',
        'pyparsing == 2.3.1',
        'python-dateutil == 2.8.0',
       ' pytz == 2018.9',
        'requests == 2.21.0',
        'six == 1.12.0',
        'soupsieve == 1.8',
        'typing-extensions == 3.7.2',
        'urllib3 == 1.24.2',
        'yarl == 1.3.0',
    ],
    include_package_data=True,
    zip_safe=False
)
