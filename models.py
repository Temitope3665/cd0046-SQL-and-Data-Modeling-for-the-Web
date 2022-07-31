import datetime
from flask_sqlalchemy import SQLAlchemy


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True,nullable=False)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(120))
    description = db.Column(db.String)
    is_talent =db.Column(db.Boolean, default=False) #looking for talent#  accepts list of genres e.g ['r&b','pop']
    genres = db.Column(db.ARRAY(db.String(120)))
    created_at = db.Column(db.DateTime, default= datetime.datetime.utcnow())
    shows = db.relationship('Show',backref='venue',lazy=True,cascade="all,delete",passive_deletes=True)
    def __repr__(self):
      return f'<Venue id={self.id} name={self.name}>'



class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    created_at = db.Column(db.DateTime, default= datetime.datetime.utcnow())

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(120))
    description = db.Column(db.String)
    is_venue =db.Column(db.Boolean, default=False) #looking for venue
    shows = db.relationship('Show',backref='artist',lazy=True,cascade="all,delete",passive_deletes=True)

    def __repr__(self):
      return f'<Artist id={self.id} name={self.name}>'



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ ='show'
  id = db.Column(db.Integer, primary_key=True,nullable=False)
  start_time= db.Column(db.DateTime)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'),nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'),nullable=False)
  created_at = db.Column(db.DateTime, default= datetime.datetime.utcnow())

  def __repr__(self):
    return f'<show id={self.id} artist={self.artist_id} venue={self.venue_id}>'