#from pyramid.response import Response
#from pyramid.renderers import get_renderer
#from sqlalchemy.exc import DBAPIError

#import docutils.core import publish_parts

from pyramid.security import authenticated_userid
from pyramid.exceptions import Forbidden
from pyramid.view import view_config

# Database object models
from .models import (
	DBSession,
	DJ,
	Song,
	Queue,
	User
)

# For Jinja2 Templates
from jinja2 import Template, Environment, PackageLoader

from collections import OrderedDict

# @view_config(route_name='login', renderer='login.jinja2')
# def login_view(request):
# 	# Grab request variables
# 	email = request.matchdict['email']
# 	password = request.matchdict['password']

# 	# Create a session
# 	session = request.session

# 	# Check if user is already logged in
	

# 	if 'email' in session:
# 		# User is already logged in
# 		return {
# 			'app_name': 'ReQuest'
# 		}
# 	else:
# 		# Pull user with email from database
# 		user = DBSession.query(User).filter_by(email=email).first()

# 		# Authenticate user
# 		if user.password == password:
# 			# Set session 
# 			session['email'] = email

# 	return {
# 		'app_name': 'ReQuest',
# 		'email': session['email'],
# 	}

@view_config(route_name='djs', renderer='djs.jinja2')
def djs_view(request):
	# Check if a user is logged in
	userid = authenticated_userid(request)
	if userid is None:
		raise Forbidden()

	# Pull DJs from database
	# djs = DBSession.query(DJ)
	records = DBSession.query(DJ, Queue).join(Queue).filter(DJ.id==Queue.dj_id).all()

	return {
		'app_name': 'ReQuest',
		'userid': userid,
		'records': records
	}

@view_config(route_name='dj', renderer='dj.jinja2')
def dj_view(request):
	# Check if a user is logged in
	userid = authenticated_userid(request)
	if userid is None:
		raise Forbidden()

	dj_id = request.matchdict['dj_id']

	# Pull dj with dj_id from database
	dj = DBSession.query(DJ).filter_by(id=dj_id).first()

	return {
		'app_name': 'ReQuest',
		'userid': userid,
		'dj': dj
	}

@view_config(route_name='queue', renderer='queue.jinja2')
def queue_view(request):
	# Check if a user is logged in
	userid = authenticated_userid(request)
	if userid is None:
		raise Forbidden()

	queue_id = request.matchdict['queue_id']

	# Grab the songs for this queue
	# songs = DBSession.query(Song).join(Queue, Song.queues).filter(Song.queues.any()).all()
	songs = DBSession.query(Song).join(Queue, Song.queues).filter(Queue.id == queue_id).all()

	# # Check to see if POST
	# if  request.environ['REQUEST_METHOD'] == 'POST':
	# 	# Redirect to a results view and override template
	# 	request.override_renderer = 'results.jinja2'
	# 	query_songs = results_view(request)
	# 	print('got the results back from results_view:')
	# 	print(query_songs)
		
	# 	return {
	# 		'app_name': 'ReQuest',
	# 		'userid': userid,
	# 		'queueid': queue_id,
	# 		'songs': query_songs,
	# 		'count': len(query_songs)
	# 	}

	return {
		'app_name': 'ReQuest',
		'userid': userid,
		'queueid': queue_id,
		'songs': songs
	}

@view_config(route_name='results', renderer='results.jinja2')
def results_view(request):
	print('In results_view...')
	# Grab the search text from the form
	search_text = request.params['search_text']
	print(request.params['search_text'])
	
	# Query the DB for songs
	query_songs_title = DBSession.query(Song).filter(Song.title.like('%'+search_text+'%')).all()
	query_songs_artist = DBSession.query(Song).filter(Song.artist.like('%'+search_text+'%')).all()
	query_songs = query_songs_artist + query_songs_title
	query_songs = list(OrderedDict.fromkeys(query_songs))

	print(query_songs)

	return {
		'app_name': 'ReQuest',
		'userid': userid,
		'queueid': queue_id,
		'songs': query_songs,
		'count': len(query_songs)
	}

@view_config(route_name='songadd')
def songadd_view(request):
	print('In songadd_view...')
	# Check if a user is logged in
	userid = authenticated_userid(request)
	if userid is None:
		raise Forbidden()

	queue_id = request.matchdict['queue_id']
	song_id = request.matchdict['song_id']
	print(queue_id + song_id)

	# Add the song and querue to the association table
	queue = DBSession.query(Queue).filter_by(id=queue_id).first()
	print('found queue')
	print(queue)
	song = DBSession.query(Song).filter_by(id=song_id).first()
	print('found song')
	print(song)

	queue.songs.append(song)
	print('association added')

	# DBSession.commit()
	print('commited to database')

	# Grab the songs for this queue
	# songs = DBSession.query(Song).filter_by(id=song_id).filter(Song.queues.any()).all()
	# songs = DBSession.query(Song).join(Queue, Song.queues).filter(Queue.id == queue_id).all()
	# print('got songs in queue')
	# print(songs)
	# print('afterwards...')

	queue_view(request)
	# return {
	# 	'app_name': 'ReQuest',
	# 	'userid': userid,
	# 	'queueid': queue_id,
	# 	'songs': songs
	# }


@view_config(route_name='users', renderer='users.jinja2')
def users_view(request):
	# Check if a user is logged in
	userid = authenticated_userid(request)
	if userid is None:
		raise Forbidden()

	# Pull users from database
	users = DBSession.query(User)

	return {
		'app_name': 'ReQuest',
		'userid': userid,
		'users': users
	}

@view_config(route_name='user', renderer='user.jinja2')
def user_view(request):
	# Check if a user is logged in
	userid = authenticated_userid(request)
	if userid is None:
		raise Forbidden()
		
	user_id = request.matchdict['user_id']

	# Pull user with user_id from database
	user = DBSession.query(User).filter_by(id=user_id).first()

	# Check to see if POST
	if  request.environ['REQUEST_METHOD'] == 'POST':
		print(request.params['email'])
		print(request.params['password'])

		# Write POST info to database
		user.email = request.params['email']
		user.password = request.params['password']
		DBSession.add(user)

	return {
		'app_name': 'ReQuest',
		'userid': userid,
		'user': user
	}