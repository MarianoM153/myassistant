from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL en Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Recordatorio(db.Model):
    __tablename__ = 'recordatorios'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(250), nullable=False)
    fecha = db.Column(db.String(10), nullable=False)
    hora = db.Column(db.String(5), nullable=False)

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    data = request.json
    descripcion = data['descripcion']
    fecha = data['fecha']
    hora = data['hora']
    
    new_reminder = Recordatorio(descripcion=descripcion, fecha=fecha, hora=hora)
    db.session.add(new_reminder)
    db.session.commit()
    
    return jsonify({"message": "Recordatorio agregado con éxito"}), 201

@app.route('/get_reminders', methods=['GET'])
def get_reminders():
    recordatorios = Recordatorio.query.all()
    return jsonify([{
        'id': r.id,
        'descripcion': r.descripcion,
        'fecha': r.fecha,
        'hora': r.hora
    } for r in recordatorios])

if __name__ == '__main__':
    app.run(debug=True)
