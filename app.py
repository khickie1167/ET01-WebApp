from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from upload_handler import upload

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

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

@app.route('/upload', methods=['POST'])
def upload_endpoint():
    return upload()

@app.route('/delete_link/<int:link_id>', methods=['POST'])
def delete_link(link_id):
    print(f"Attempting to delete link with ID: {link_id}")  # Debug statement
    link = Link.query.get(link_id)
    if link:
        db.session.delete(link)
        db.session.commit()
        flash('Link deleted successfully!', 'success')
        print(f"Link with ID: {link_id} deleted successfully")  # Debug statement
    else:
        flash('Link not found!', 'danger')
        print(f"Link with ID: {link_id} not found")  # Debug statement
    return redirect(url_for('dataupload'))

@app.route('/delete_all_links', methods=['POST'])
def delete_all_links():
    try:
        db.session.query(Link).delete()
        db.session.commit()
        flash('All links deleted successfully!', 'success')
    except Exception as e:
        flash('Error deleting all links: ' + str(e), 'danger')
    return redirect(url_for('dataupload'))

if __name__ == '__main__':
    app.run()
