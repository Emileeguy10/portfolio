# app.py
try:
    from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
    from werkzeug.utils import secure_filename
    from werkzeug.security import check_password_hash, generate_password_hash
    from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
    from PIL import Image
except Exception as e:
    # Helpful error at runtime when dependencies are missing.
    # This tells users / CI how to fix the "Import 'flask' could not be resolved" issue.
    raise RuntimeError(
        "Required packages are not installed or cannot be imported.\n\n"
        "Please create/activate your virtual environment and run:\n\n"
        "    pip install -r requirements.txt\n\n"
        f"Original error: {e}"
    )

import os
from datetime import datetime
import json

app = Flask(__name__)
app.config.from_object('config.Config')
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Path for user data
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

# Sample data for portfolio
projects = [
    {
        'id': 1,
        'title': 'Neural Canvas',
        'category': 'AI Art',
        'description': 'Generative art platform using GANs to create unique digital masterpieces',
        'image': 'project1.jpg',
        'color': '#FF6B6B',
        'technologies': ['Python', 'TensorFlow', 'React'],
        'featured': True
    },
    {
        'id': 2,
        'title': 'EcoVision',
        'category': 'Sustainability',
        'description': 'Real-time environmental monitoring system using satellite imagery',
        'image': 'project2.jpg',
        'color': '#4ECDC4',
        'technologies': ['Python', 'Computer Vision', 'AWS'],
        'featured': True
    },
    {
        'id': 3,
        'title': 'Quantum Chat',
        'category': 'Communication',
        'description': 'End-to-end encrypted messaging with quantum-resistant algorithms',
        'image': 'project3.jpg',
        'color': '#45B7D1',
        'technologies': ['Python', 'WebSockets', 'Cryptography'],
        'featured': True
    },
    {
        'id': 4,
        'title': 'VR Studio',
        'category': 'Virtual Reality',
        'description': 'Collaborative VR environment for 3D design and prototyping',
        'image': 'project4.jpg',
        'color': '#96CEB4',
        'technologies': ['Unity', 'Python', 'WebXR'],
        'featured': False
    },
    {
        'id': 5,
        'title': 'HealthSync',
        'category': 'Health Tech',
        'description': 'AI-powered personal health assistant and analytics platform',
        'image': 'project5.jpg',
        'color': '#FFEAA7',
        'technologies': ['Python', 'Machine Learning', 'Flutter'],
        'featured': False
    },
    {
        'id': 6,
        'title': 'SmartGrid',
        'category': 'IoT',
        'description': 'Intelligent energy distribution system for smart cities',
        'image': 'project6.jpg',
        'color': '#DDA0DD',
        'technologies': ['Python', 'IoT', 'Blockchain'],
        'featured': False
    }
]

skills = [
    {'name': 'Python', 'level': 95, 'color': '#3776AB'},
    {'name': 'Machine Learning', 'level': 88, 'color': '#FF6B6B'},
    {'name': 'React', 'level': 85, 'color': '#61DAFB'},
    {'name': 'Cloud Architecture', 'level': 82, 'color': '#FFA07A'},
    {'name': 'UI/UX Design', 'level': 78, 'color': '#9B59B6'},
    {'name': 'DevOps', 'level': 75, 'color': '#3498DB'}
]

timeline = [
    {'year': '2024', 'title': 'Senior AI Engineer', 'company': 'Tech Innovations Inc.', 'description': 'Leading AI research and development team'},
    {'year': '2022', 'title': 'Full Stack Developer', 'company': 'Digital Solutions', 'description': 'Developed scalable web applications'},
    {'year': '2020', 'title': 'ML Engineer', 'company': 'DataTech', 'description': 'Built ML models for predictive analytics'},
    {'year': '2018', 'title': 'CS Graduate', 'company': 'University of Technology', 'description': 'Bachelor\'s in Computer Science'}
]

@app.route('/')
def index():
    user = load_user()
    return render_template('index.html', 
                         projects=projects[:3], 
                         skills=skills[:4],
                         timeline=timeline,
                         user=user)

@app.route('/projects')
def projects_page():
    return render_template('projects.html', projects=projects)

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    # Here you would typically send an email or save to database
    return jsonify({'status': 'success', 'message': 'Message received!'})

@app.route('/api/projects/<int:project_id>')
def get_project(project_id):
    project = next((p for p in projects if p['id'] == project_id), None)
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404


# --- User data helpers and admin routes ---
def load_user():
    default = {
        'name': 'Muluh Emile',
        'title': 'Creative Developer & AI Innovator',
        'bio': 'Crafting digital experiences that blend creativity with cutting-edge technology.',
        'profile_image': '/static/profile-placeholder.svg',
        'email': ''
    }
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # merge defaults
                for k, v in default.items():
                    data.setdefault(k, v)
                return data
    except Exception:
        pass
    return default


# Simple user model for Flask-Login
class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name


@login_manager.user_loader
def user_loader(user_id):
    # only single admin user supported; return a User object if matches
    admin_username = os.environ.get('ADMIN_USER', 'admin')
    if str(user_id) == admin_username:
        return User(user_id, admin_username)
    return None


def save_user(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # directory for uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

    if request.method == 'POST':
        # gather fields from form (simple text fields)
        name = request.form.get('name', '').strip()
        title = request.form.get('title', '').strip()
        bio = request.form.get('bio', '').strip()
        profile_image_url = request.form.get('profile_image', '').strip()
        email = request.form.get('email', '').strip()

        # handle uploaded file (profile image)
        profile_file = request.files.get('profile_file')
        profile_image = profile_image_url or '/static/profile-placeholder.svg'
        if profile_file and profile_file.filename:
            filename = secure_filename(profile_file.filename)
            if allowed_file(filename):
                # avoid collisions by prefixing timestamp
                prefix = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                filename = f"{prefix}_{filename}"
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                profile_file.save(save_path)
                # try to resize image for large and thumbnail
                try:
                    img = Image.open(save_path)
                    img_format = img.format or 'JPEG'
                    # create a large resized version (max 1200x1200)
                    max_size = (1200, 1200)
                    img_copy = img.copy()
                    img_copy.thumbnail(max_size, Image.LANCZOS)
                    # overwrite saved image with resized large
                    if img_copy.mode in ("RGBA", "P"):
                        img_copy = img_copy.convert('RGB')
                    img_copy.save(save_path, format=img_format, optimize=True, quality=85)

                    # create thumbnail (300x300)
                    thumb_size = (300, 300)
                    thumb = img.copy()
                    thumb.thumbnail(thumb_size, Image.LANCZOS)
                    if thumb.mode in ("RGBA", "P"):
                        thumb = thumb.convert('RGB')
                    thumb_name = f"thumb_{filename}"
                    thumb_path = os.path.join(UPLOAD_FOLDER, thumb_name)
                    thumb.save(thumb_path, format=img_format, optimize=True, quality=80)
                except Exception:
                    # If Pillow fails, keep original file
                    pass
                # store web path (point to resized large)
                profile_image = f'/static/uploads/{filename}'

        user = {
            'name': name or 'Muluh Emile',
            'title': title or 'Creative Developer & AI Innovator',
            'bio': bio or 'Crafting digital experiences that blend creativity with cutting-edge technology.',
            'profile_image': profile_image,
            'email': email
        }
        ok = save_user(user)
        if ok:
            return redirect(url_for('admin', saved=1))
        else:
            return render_template('admin.html', user=user, error='Failed to save data')

    # GET
    user = load_user()
    saved = request.args.get('saved')
    return render_template('admin.html', user=user, saved=saved)


@app.context_processor
def inject_user():
    # make user available in all templates
    return {'user': load_user()}

if __name__ == '__main__':
    app.run(debug=True, port=5000)