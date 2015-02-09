"""
Flask-routes
-------------

Alternative routing for Flask
"""

import setuptools

setuptools.setup(
    name='Flask-Routing',
    version='0.0.21',
    url='',
    license='BSD',
    author='Hackerlist',
    author_email='support@hackerlist.net',
    description='Alternative web.py style routing for Flask',
    long_description=__doc__,
    packages=setuptools.find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
