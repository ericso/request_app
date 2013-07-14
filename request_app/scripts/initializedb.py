import os
import sys
import transaction
import datetime

from sqlalchemy import engine_from_config

from pyramid.paster import (
	get_appsettings,
	setup_logging,
	)

from ..models import (
	DBSession,
	Base,
	DJ,
	Song,
	Queue,
	User,
	Venue
	)


def usage(argv):
	cmd = os.path.basename(argv[0])
	print('usage: %s <config_uri>\n'
		  '(example: "%s development.ini")' % (cmd, cmd))
	sys.exit(1)


def main(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	setup_logging(config_uri)
	settings = get_appsettings(config_uri)
	engine = engine_from_config(settings, 'sqlalchemy.')
	DBSession.configure(bind=engine)
	Base.metadata.create_all(engine)
	with transaction.manager:
		# TODO: there has to be a way to add database objects other than here
		user = User(email='me@eric.so', name='Eric So', password='password', join_date=datetime.datetime.now())
		DBSession.add(user)
		user = User(email='jfizz@doggpound.com', name='Jazzy Fizzle', password='password', join_date=datetime.datetime.now())
		DBSession.add(user)
		user = User(email='SamanthaH@google.com', name='Sam Hugnkiss', password='password', join_date=datetime.datetime.now())
		DBSession.add(user)

		# DJs
		dj = DJ(email='djjj@fpba.org', name='DJ Jazzy Jeff', bio='From the Fresh Prince of Bel Air')
		DBSession.add(dj)
		dj = DJ(email='binxy@sanger.net', name='DJ Binx', bio='Les Love')
		DBSession.add(dj)
		dj = DJ(email='manhunt@ihuntmen.com', name='DJ Manhunt', bio='I hunt men')
		DBSession.add(dj)
		dj = DJ(email='sleepercell@gmail.com', name='SleeperCell', bio='We hide in the shadows.')
		DBSession.add(dj)

		# Songs
		song = Song(title='Domino', artist='Jessie J', album='Who You Are', year=2011)
		DBSession.add(song)
		song = Song(title='Price Tag', artist='Jessie J', album='Who You Are', year=2011)
		DBSession.add(song)
		song = Song(title='Enter Sandman', artist='Metallica', album='Metallica', year=1991)
		DBSession.add(song)
		song = Song(title='No One Knows', artist='Queens of the Stone Age', album='Songs for the Deaf', year=2002)
		DBSession.add(song)
		song = Song(title='Stairway to Heaven', artist='Led Zeppelin', album='Led Zeppelin IV', year=1971)
		DBSession.add(song)
		song = Song(title='AEnema', artist='Tool', album='AEnima', year=1996)
		DBSession.add(song)


		# Venues
		venue = Venue(name='The Boom Boom Room', email='bbroom@gmail.com', address='123 Fake Street, San Francisco, CA 94103')
		DBSession.add(venue)
		venue = Venue(name='The Rickshaw Stop', email='rickshawstop@gmail.com', address='340 South Van Ness Avenue, San Francisco, CA 94103')
		DBSession.add(venue)
		venue = Venue(name='Rainbow Club', email='rainbowclub@gmail.com', address='100 California Avenue, San Francisco, CA 94103')
		DBSession.add(venue)

		# Queues
		queue = Queue(dj_id=1, venue_id=1, date='June 7, 2013')
		DBSession.add(queue)
		queue = Queue(dj_id=2, venue_id=3, date='July 4, 2013')
		DBSession.add(queue)
		queue = Queue(dj_id=3, venue_id=1, date='August 2, 2013')
		DBSession.add(queue)
		queue = Queue(dj_id=4, venue_id=2, date='August 2, 2013')
		DBSession.add(queue)
