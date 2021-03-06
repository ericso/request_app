from sqlalchemy import (
	Table,
	Column,
	Integer,
	Text,
	DateTime,
	ForeignKey
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
	scoped_session,
	sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
	""" The SQLAlchemy declarative model class for a User object. """
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	email = Column(Text)
	name = Column(Text)
	password = Column(Text)
	join_date = Column(DateTime)

	def __init__(self, email, name, password, join_date=datetime.datetime.now()):
		self.email = email
		self.name = name
		self.password = password
		self.join_date = join_date
	def __repr__(self):
	    return "<User('%s','%s', '%s, '%s')>" % (self.email, self.name, self.password, self.join_date)


class DJ(Base):
	""" The SQLAlchemy declarative model class for a DJ object. """
	__tablename__ = 'djs'
	id = Column(Integer, primary_key=True)
	email = Column(Text)
	name = Column(Text)
	bio = Column(Text)

	# A DJ can have multiple Queues
	queue = relationship('Queue', order_by='Queue.id', backref='djs')

	def __init__(self, email, name, bio):
		self.email = email
		self.name = name
		self.bio = bio


songs_to_queues_table = Table('songs_to_queues', Base.metadata,
	Column('song_id', Integer, ForeignKey('songs.id')),
	Column('queue_id', Integer, ForeignKey('queues.id'))
)


class Song(Base):
	""" The SQLAlchemy declarative model class for a Song object. """
	__tablename__ = 'songs'
	id = Column(Integer, primary_key=True)
	title = Column(Text)
	artist = Column(Text)
	album = Column(Text)
	year = (Integer)

	# queues = relationship('Queue', secondary=songs_to_queues_table, backref='songs')

	def __init__(self, title, artist, album, year):
		self.title = title
		self.artist = artist
		self.album = album
		self.year = year


class Queue(Base):
	""" The SQLAlchemy declarative model class for a Queue object. """
	__tablename__ = 'queues'
	id = Column(Integer, primary_key=True)

	dj_id = Column(Integer, ForeignKey('djs.id'))
	venue_id = Column(Integer, ForeignKey('venues.id'))
	date = Column(Text)

	# Each Queue has a single DJ and a single Venue
	dj = relationship('DJ', backref=backref('djs', order_by=id))
	venue = relationship('Venue', backref=backref('venues', order_by=id))

	# Each Queue has many Songs
	songs = relationship('Song', secondary=songs_to_queues_table, backref='queues')

	def __init__(self, dj_id, venue_id, date):
		self.dj_id = dj_id
		self.venue_id = venue_id
		self.date = date


class Venue(Base):
	""" The SQLAlchemy declarative model class for a Venue object. """
	__tablename__ = 'venues'
	id = Column(Integer, primary_key=True)
	email = Column(Text)
	name = Column(Text)
	address = Column(Text)
	queues = relationship('Queue', order_by='Queue.id', backref='venues') # A Venue can have multiple Queues

	def __init__(self, email, name, address):
		self.email = email
		self.name = name
		self.address = address

