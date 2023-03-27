# A few imports I googled together on the internet. I'm just happy they don't break.
import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# his is
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Recording

db.init_app(app)

# project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# this piece of code imports the python files i wrote to call the apis
# it should also import the recording.
from audio_processing.speech_to_text import speech_to_text
from dalle_processing.dalle_handler import generate_image_from_text
from models import Recording

#the homepage
@app.route('/')
def index():
    return render_template('index.html')

# this should return the past images with the app
@app.route('/past_images')
def past_images():
    recordings = Recording.query.order_by(Recording.date_posted.desc()).all()
    return render_template('basic.html', recordings=recordings)


# the idea was to get an enlarged version of a past image when clicking on it
@app.route('/image/<int:image_id>')
def image(image_id):
    recording = Recording.query.get_or_404(image_id)
    return render_template('images.html', recording=recording)


@app.route('/show_data')
def show_data():
    recordings = Recording.query.all()
    return jsonify([recording.to_dict() for recording in recordings])
    
# this part of the code runs on thoughts and prayers. the basic idea was to receive a text and send it to the next api.
# after adding the database function it sometimes breaks and I have no idea why. Is there a better way to write it down?
@app.route('/process_audio', methods=['POST'])
def process_audio():
    audio_file = request.files.get('audio')
    if audio_file:
        text = speech_to_text(audio_file)
        if text:
            processed_text = text
            image_url = generate_image_from_text(processed_text)
            if image_url:
                recording = Recording(title="Generated Image", image_url=image_url, thumbnail_url=image_url)
                db.session.add(recording)
                db.session.commit()
                return jsonify({'success': True, 'image_url': image_url})
            else:
                return jsonify({'success': False, 'error': 'Error generating image'})
        else:
            return jsonify({'success': False, 'error': 'Error converting audio to text'})
    else:
        return jsonify({'success': False, 'error': 'No audio file received'})

# I wanted to provide some Image samples to test my app and showcase if the person doesn't have an open_AI_API Key
def insert_sample_data():
    sample_data = sample_data = [
    {
        'title': 'Image 1',
        'date_posted': datetime.utcnow(),
        'image_url': '/static/images/image1.jpg',
        'thumbnail_url': '/static/images/preview_image1.jpg'
    },
    {
        'title': 'Image 2',
        'date_posted': datetime.utcnow(),
        'image_url': '/static/images/image2.jpg',
        'thumbnail_url': '/static/images/preview_image2.jpg'
    },
]

    for data in sample_data:
        recording = Recording(title=data['title'], date_posted=data['date_posted'],
                              image_url=data['image_url'], thumbnail_url=data['thumbnail_url'])
        db.session.add(recording)
    db.session.commit()

def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_tables()  # This creates the tables if they don't exist
    with app.app_context():
        insert_sample_data()  # This inserts the sample data hopefully
    app.run(debug=True)



