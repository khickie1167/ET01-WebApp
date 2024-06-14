from flask import Flask, render_template
from upload_handler import upload
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dataupload')
def dataupload():
    return render_template('dataupload.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload_endpoint():
    return upload()

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode to get detailed error information
