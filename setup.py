#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    author='WWU Housing and Viking Union',
    author_email='jabez.kizer@wwu.edu',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    description='LDAP Authorization for Django',
    keywords='django ldap authentication backend',
    license='MIT',
    long_description=""" Authorize users based on LDAP group membership. 
Active Directory oriented, includes support for nested AD groups.
""",
    name='django_ldapauth',
    packages=['ldapauth'],
    url='http://github.com/jabezk/django-ldapauth',
    version='1.5',
)
