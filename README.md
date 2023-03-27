# Speech-to-Picture

This is a simple Flask web application that allows users to record images and view past images.

## Installation

1. Install Python 3.7+ and `pip`
2. Install the required dependencies by running: `pip install -r requirements.txt`
4. Run the Flask app by running `python app.py`
   This should also automatically set up a SQLite database and insert sample data.
5. Get yourself an OPENAI_API_KEY that you set in you terminal with export OPENAI_API_KEY=<"your key"> or ask me for a demo.

## Usage

1. Access the web application at `http://127.0.0.1:5000`
2. The main page allows you to record an image using your voice after allowing the browser to access you microphone (and having an openai key)
3. To view past images, visit `http://127.0.0.1:5000/past_images`
4. To view a specific image, visit `http://127.0.0.1:5000/image/{image_id}`, where `{image_id}` is the ID of the image you want to view.

## Features

- Record images using the browser
- View past images in a list
- View a specific image by ID
- Watch it break down every second attempt (Just kidding ... kinda)
