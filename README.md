# Speech-to-Picture

This is a simple Flask web application that allows users to record images and view past images.

## Installation

1. Install Python 3.7+ and `pip`
2. Install the required dependencies by running: `pip install -r requirements.txt`
3. Install Homebrew using  
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
4. Install FFMPEG using "brew install ffmpeg" in your terminal
5. Get yourself an OPENAI_API_KEY that you set in you terminal with export OPENAI_API_KEY=<"your key"> or ask me for a demo.
6. Run the Flask app by running `python app.py`
   This should also automatically set up a SQLite database and insert sample data.

## Usage

1. Access the web application at `www.fraime.herokuapp.com"
2. The main page allows you to record an image using your voice after allowing the browser to access you microphone (and having an openai key)
3. To view past images, visit `www.fraime.herokuapp.com"
4. To view a specific image, visit `https://fraime.herokuapp.com/image/{image_id}`, where `{image_id}` is the ID of the image you want to view. There you also delete the image from the databank or edit it's name. To navigate back after doing that type in one of the other URLs mentioned

## Features

- Record images using the browser
- View past images in a list
- View a specific image by ID
- Edit or delete iamges
