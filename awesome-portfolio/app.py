# app.py
from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import json

app = Flask(__name__)

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
    return render_template('index.html', 
                         projects=projects[:3], 
                         skills=skills[:4],
                         timeline=timeline)

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)