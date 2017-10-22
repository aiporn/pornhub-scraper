"""
Project meta-data.
"""

from setuptools import setup, find_packages

setup(
    name='pornhub-scraper',
    version='0.0.1',
    description='Scrape meta-data from Pornhub.',
    long_description='Scrape meta-data from Pornhub.',
    url='https://github.com/aiporn/pornhub-scraper',
    author='Porn AI',
    author_email='openpornai@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='porn ai scraping html',
    packages=find_packages(),
    install_requires=['beautifulsoup4'],
)
