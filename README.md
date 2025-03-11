# CLIP-WEB-UI

This is a web application that allows you to search through a folder of images using OpenAI's CLIP model. You can search using text queries or by uploading an image.

## Setup

### automatic setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Majd126/CLIP-WEB-UI.git
2. run 'run first time only.bat'

### maunal setup
1. Clone this repository:
   ```bash
   git clone https://github.com/Majd126/CLIP-WEB-UI.git
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

### automatic usage

1. run 'add images.bat' and choose the folder you want to search within "it'll be copied here"
2. run 'run app.bat' open the link and search..

adding new images deletes the previous ones.. if you want to remove the images manually you can run 'delete images'


### maunal usage
1. Place your images in the static/images/ folder.
2. Run the preprocessing script to generate embeddings:
   ```bash
   python preprocess.py
3. Start the Flask app:
   ```bash
   python app.py
4. Open your browser and navigate to http://127.0.0.1:5000/

## Attribution
This project uses OpenAI's CLIP model. The original CLIP repository can be found here: [OpenAI/CLIP](https://github.com/openai/CLIP).
