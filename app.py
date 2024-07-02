from flask import Flask, render_template, request, jsonify
from models import db, Link
from upload_handler import upload

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'  # Change this if you use a different database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # For flash messages

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dataupload', methods=['GET', 'POST'])
def dataupload():
    if request.method == 'POST':
        url = request.json.get('url')
        if url:
            if Link.query.filter_by(url=url).first():
                return jsonify({"message": "Link already exists!", "category": "danger"}), 400
            else:
                new_link = Link(url=url)
                db.session.add(new_link)
                db.session.commit()
                links = Link.query.order_by(Link.date_added.desc()).all()
                links_data = [{"id": link.id, "url": link.url} for link in links]
                return jsonify({"message": "Link added successfully!", "category": "success", "links": links_data})

    links = Link.query.order_by(Link.date_added.desc()).all()
    links_data = [{"id": link.id, "url": link.url} for link in links]
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({"links": links_data})

    return render_template('dataupload.html', links=links_data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/upload', methods=['POST'])
def upload_endpoint():
    return upload()


@app.route('/delete_link/<int:link_id>', methods=['POST'])
def delete_link(link_id):
    link = Link.query.get(link_id)
    if link:
        db.session.delete(link)
        db.session.commit()
        links = Link.query.order_by(Link.date_added.desc()).all()
        links_data = [{"id": link.id, "url": link.url} for link in links]
        return jsonify({"message": "Link deleted successfully!", "category": "success", "links": links_data})
    else:
        return jsonify({"message": "Link not found!", "category": "danger"}), 404



@app.route('/delete_all_links', methods=['POST'])
def delete_all_links():
    try:
        db.session.query(Link).delete()
        db.session.commit()
        return jsonify({"message": "All links deleted successfully!", "category": "success"})
    except Exception as e:
        return jsonify({"message": f"Error deleting all links: {str(e)}", "category": "danger"}), 500


if __name__ == '__main__':
    app.run()
