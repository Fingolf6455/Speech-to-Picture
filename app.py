import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import EditTitleForm

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Recording

db.init_app(app)

app.config['SECRET_KEY'] = 'victor_is_nice'

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from audio_processing.speech_to_text import speech_to_text
from dalle_processing.dalle_handler import generate_image_from_text
from models import Recording

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/past_images')
def past_images():
    recordings = Recording.query.order_by(Recording.date_posted.desc()).all()
    return render_template('basic.html', recordings=recordings)

@app.route('/image/<int:image_id>')
def image(image_id):
    recording = Recording.query.get_or_404(image_id)
    if recording:
        return render_template('images.html', recording=recording, edit_title_form=EditTitleForm())
    else:
        return render_template('404.html'), 404

@app.route('/edit_image_title/<int:image_id>', methods=['POST'])
def edit_image_title(image_id):
    new_title = request.form.get('new_title')
    if not new_title:
        return jsonify({'success': False, 'error': 'No new title provided'})

    recording = Recording.query.get_or_404(image_id)
    recording.title = new_title
    db.session.commit()

    return jsonify({'success': True, 'message': 'Title updated'})

@app.route('/process_audio', methods=['POST'])
def process_audio():
    audio_file = request.files.get('audio')

    if not audio_file:
        return jsonify({'success': False, 'error': 'No audio file received'})

    text = speech_to_text(audio_file)
    if not text:
        return jsonify({'success': False, 'error': 'Error converting audio to text'})

    processed_text = text
    image_url = generate_image_from_text(processed_text)

    if not image_url:
        return jsonify({'success': False, 'error': 'Error generating image'})

    recording = Recording(title="Generated Image", image_url=image_url, thumbnail_url=image_url)
    db.session.add(recording)
    db.session.commit()

    return jsonify({'success': True, 'image_url': image_url})

def insert_sample_data():
    sample_data = [
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
    
@app.route('/delete_image/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    recording = Recording.query.get_or_404(image_id)
    db.session.delete(recording)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Image deleted'})

def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    with app.app_context():
        insert_sample_data()
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))