from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import logging

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

db = SQLAlchemy(app)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dataupload', methods=['GET', 'POST'])
def dataupload():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            if Link.query.filter_by(url=url).first():
                flash('Link already exists!', 'danger')
            else:
                new_link = Link(url=url)
                db.session.add(new_link)
                db.session.commit()
                flash('Link added successfully!', 'success')
    links = Link.query.order_by(Link.date_added.desc()).all()
    return render_template('dataupload.html', links=links)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/delete_link/<int:link_id>', methods=['POST'])
def delete_link(link_id):
    link = Link.query.get(link_id)
    if link:
        db.session.delete(link)
        db.session.commit()
        flash('Link deleted successfully!', 'success')
    else:
        flash('Link not found!', 'danger')
    return redirect(url_for('dataupload'))

@app.route('/delete_all_links', methods=['POST'])
def delete_all_links():
    try:
        num_rows_deleted = db.session.query(Link).delete()
        db.session.commit()
        flash(f'All links deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting all links: {str(e)}', 'danger')
    return redirect(url_for('dataupload'))

@app.route('/refresh_dashboard', methods=['POST'])
def refresh_dashboard():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(timestamp=current_time)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        try:
            # Connect to Azure Blob Storage
            blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
            container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)

            # Upload the file to Azure Blob Storage
            blob_client.upload_blob(file, overwrite=True)
            return jsonify({"message": "File uploaded successfully!"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 500
    return jsonify({"message": "No file provided"}), 400

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
