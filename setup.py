import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
	'pyramid',
	'SQLAlchemy',
	'transaction',
	'pyramid_tm',
	'pyramid_debugtoolbar',
	'zope.sqlalchemy',
	'waitress',
	'pyramid_jinja2',
  'pyramid_beaker',
  'pyramid_persona'
]

setup(name='request_app',
  version='0.0',
  description='request_app',
  long_description=README + '\n\n' + CHANGES,
  classifiers=[
  	"Programming Language :: Python",
  	"Framework :: Pyramid",
  	"Topic :: Internet :: WWW/HTTP",
  	"Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
  ],
  author='',
  author_email='',
  url='',
  keywords='web wsgi bfg pylons pyramid',
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  test_suite='request_app',
  install_requires=requires,
  entry_points="""\
  [paste.app_factory]
  main = request_app:main
  [console_scripts]
  initialize_request_app_db = request_app.scripts.initializedb:main
  """,
)
