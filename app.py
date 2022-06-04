#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
import sys
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
# app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://temi_@localhost:5432/fyyurapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(500), nullable=False)
    genres = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(500), nullable=False)
    looking_for_talent = db.Column(db.String, nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repl__(self):
      return f'<Venue {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(500), nullable=False)
    genres = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(500), nullable=False)
    looking_for_venues = db.Column(db.String, nullable=False)
    description = db.Column(db.String(1500), nullable=False)

    def __repl__(self):
      return f'<Artist {self.id} {self.name}>'

class Shows(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, nullable=False)
    venue_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.String(120), nullable=False)

    def __repl__(self):
      return f'<Artist {self.id} {self.artist}>'

db.create_all()
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  return render_template('pages/venues.html', areas=Venue.query.all())

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.filter_by(venue_id=venue_id)[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  body = {}
  try:
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    address = request.get_json()['address']
    phone = request.get_json()['phone']
    genres = request.get_json()['genres']
    facebook_link = request.get_json()['facebook_link']
    image_link = request.get_json()['image_link']
    website_link = request.get_json()['website_link']
    looking_for_talent = request.get_json()['seeking_talent']
    description = request.get_json()['description']

    venueData = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website_link=website_link, looking_for_talent=looking_for_talent, description=description)
    print(venueData, 'venueData')
    db.session.add(venueData)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

    if error:
      abort (400)
    else:
      return jsonify(body)

  return redirect(url_for('index'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  artist_name = request.get_json()['artist_name']
  print(artist_name)
  response = Artist.query.filter_by(name=artist_name)[0]
  return render_template('pages/search_artists.html', results=response.query.all(), search_term=request.form.get('search_term', ''))
  # return render_template('pages/search_artists.html', data=response.query.all())

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = Artist.query.filter_by(id=artist_id)[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).all()
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  error = False
  body = {}
  try:
    # TODO: insert form data as a new Venue record in the db, instead
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    phone = request.get_json()['phone']
    genres = request.get_json()['genres']
    facebook_link = request.get_json()['facebook_link']
    image_link = request.get_json()['image_link']
    website_link = request.get_json()['website_link']
    looking_for_venues = request.get_json()['seeking_venue']
    description = request.get_json()['description']
    # TODO: modify data to be the data object returned from db insertion
    editArtistData = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website_link=website_link, looking_for_venues=looking_for_venues, description=description)
    db.session.query(Artist).filter_by(id=artist_id).update(editArtistData)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

    if error:
      abort (400)
    else:
      return jsonify(body)

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).all()
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  error = False
  body = {}
  try:
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    address = request.get_json()['address']
    phone = request.get_json()['phone']
    genres = request.get_json()['genres']
    facebook_link = request.get_json()['facebook_link']
    image_link = request.get_json()['image_link']
    website_link = request.get_json()['website_link']
    looking_for_talent = request.get_json()['seeking_talent']
    description = request.get_json()['description']

    editVenueData = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website_link=website_link, looking_for_talent=looking_for_talent, description=description)
    db.session.query(Venue).filter_by(id=venue_id).update(editVenueData)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

    if error:
      abort (400)
    else:
      return jsonify(body)
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  error = False
  body = {}
  try:
    # TODO: insert form data as a new Venue record in the db, instead
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    phone = request.get_json()['phone']
    genres = request.get_json()['genres']
    facebook_link = request.get_json()['facebook_link']
    image_link = request.get_json()['image_link']
    website_link = request.get_json()['website_link']
    looking_for_venues = request.get_json()['seeking_venue']
    description = request.get_json()['description']
    # TODO: modify data to be the data object returned from db insertion
    artistData = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website_link=website_link, looking_for_venues=looking_for_venues, description=description)
    print(artistData, 'artistData')
    db.session.add(artistData)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

    if error:
      abort (400)
    else:
      return jsonify(body)

  return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[]

  for show in Show.query.filter(Show.artist_id != None).filter(Show.venue_id != None ).all(): 
    new_show = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link":show.artist.image_link,
      "start_time": show.start_time
    }
    data.append(new_show)
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
    form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  error = False
  body = {}
  try:
    # TODO: insert form data as a new Venue record in the db, instead
    artist_id = request.get_json()['artist_id']
    venue_id = request.get_json()['venue_id']
    start_time = request.get_json()['start_time']

    # TODO: modify data to be the data object returned from db insertion
    showsData = Shows(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    print(showsData, 'showsData')
    db.session.add(showsData)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

    if error:
      abort (400)
    else:
      return jsonify(body)

  # on successful db insert, flash success
  flash('Show was successfully listed!')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
'''
