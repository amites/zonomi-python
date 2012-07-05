from setuptools import setup, find_packages

version = '1.0'

LONG_DESCRIPTION = """
Simple API wrapper for Zonomi DNS service.
"""

setup(
    name='zonomi-python',
    version=version,
    description="Simple API wrapper for Zonomi DNS service.",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ],
    keywords='zonomi,dns',
    author='Alvin Mites',
    author_email='alvin@mitesdesign.com',
    url='https://github.com/amites/zonomi-python',
    license='MIT',
    packages=find_packages(),
    package_data = {
        'general': [
            'fixtures/*'
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
