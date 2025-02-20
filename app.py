import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from typing import Dict, List

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Necesario para mensajes flash

class ContactDatabase:
    def __init__(self, filename: str = "contacts.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self) -> List[Dict]:
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def add_contact(self, contact: Dict):
        self.data.append(contact)
        self.save_data()

    def search_by_poblacion(self, poblacion: str) -> List[Dict]:
        return [contact for contact in self.data 
                if contact.get('poblacion', '').lower() == poblacion.lower()]

    def edit_contact(self, index: int, new_data: Dict):
        if 0 <= index < len(self.data):
            self.data[index].update(new_data)
            self.save_data()

    def delete_contact(self, index: int):
        if 0 <= index < len(self.data):
            del self.data[index]
            self.save_data()

db = ContactDatabase()

# Plantilla HTML base (guardar como templates/base.html)
base_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %} - Gestión de Contactos</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 8px; }
        button { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .flash { padding: 10px; margin-bottom: 15px; }
        .success { background-color: #dff0d8; color: #3c763d; }
        .error { background-color: #f2dede; color: #a94442; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Gestión de Contactos</h1>
        <nav>
            <a href="{{ url_for('index') }}">Inicio</a> |
            <a href="{{ url_for('add_contact') }}">Añadir Contacto</a> |
            <a href="{{ url_for('search') }}">Buscar</a>
        </nav>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        contact = {
            "nombre": request.form['nombre'],
            "telefono": request.form['telefono'],
            "email": request.form['email'],
            "poblacion": request.form['poblacion'],
            "unidad": request.form['unidad'],
            "moderador": request.form['moderador'],
            "tel_moderador": request.form['tel_moderador'],
            "archipretazgo": request.form['archipretazgo'],
            "arcipreste": request.form['arcipreste'],
            "tel_arcipreste": request.form['tel_arcipreste'],
            "animador": request.form['animador'],
            "tel_animador": request.form['tel_animador']
        }
        db.add_contact(contact)
        flash('Contacto añadido exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('add_contact.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        poblacion = request.form['poblacion']
        contacts = db.search_by_poblacion(poblacion)
        return render_template('search_results.html', contacts=contacts, poblacion=poblacion)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)