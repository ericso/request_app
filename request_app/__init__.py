from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid_beaker import session_factory_from_settings

from .models import (
	DBSession,
	Base,
	)


def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	# Configure SQLAlchemy sessions
	engine = engine_from_config(settings, 'sqlalchemy.')
	DBSession.configure(bind=engine)
	Base.metadata.bind = engine

	# Configure pyramid_persona settings
	# settings = {
	#     'persona.secret': 'itsaseekret',
	#     'persona.audiences': 'http://localhost:6543'
	# }
	settings['persona.secret'] = 'itsaseekret'
	settings['persona.audiences'] = 'http://localhost:6543'

	# Setup configurator
	config = Configurator(settings=settings)

	# Configure Beaker sessions
	session_factory = session_factory_from_settings(settings)
	config.set_session_factory(session_factory)

	# User authentication
	config.include('pyramid_persona')

	# Configure routes
	config.include('pyramid_jinja2') # enable Jinja2 templates
	config.add_jinja2_search_path('request_app:templates') # tells Jinja2 to look for templates in directory
	config.add_static_view('static', 'static', cache_max_age=3600)
	config.add_route('djs', '/')
	# config.add_route('djs', '/djs')
	config.add_route('dj', '/dj/{dj_id}')
	config.add_route('queue', '/queue/{queue_id}')
	config.add_route('results', '/results/{search_text}/{queue_id}')
	config.add_route('songadd', '/songadd/{queue_id}/{song_id}')
	config.add_route('users', '/users')
	config.add_route('user', '/user/{user_id}')
	# config.add_route('results', '/results')
	config.scan()

	return config.make_wsgi_app()
