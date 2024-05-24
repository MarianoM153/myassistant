from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL en Heroku
DATABASE_URL = os.environ.get('DATABASE_URL')  # Heroku establece automáticamente esta variable de entorno
engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Recordatorio(Base):
    __tablename__ = 'recordatorios'
    id = Column(Integer, Sequence('recordatorio_id_seq'), primary_key=True)
    descripcion = Column(String(250), nullable=False)
    fecha = Column(String(10), nullable=False)
    hora = Column(String(5), nullable=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    data = request.json
    descripcion = data['descripcion']
    fecha = data['fecha']
    hora = data['hora']
    
    new_reminder = Recordatorio(descripcion=descripcion, fecha=fecha, hora=hora)
    session.add(new_reminder)
    session.commit()
    
    return jsonify({"message": "Recordatorio agregado con éxito"}), 201

@app.route('/get_reminders', methods=['GET'])
def get_reminders():
    recordatorios = session.query(Recordatorio).all()
    return jsonify([{
        'id': r.id,
        'descripcion': r.descripcion,
        'fecha': r.fecha,
        'hora': r.hora
    } for r in recordatorios])

if __name__ == '__main__':
    app.run(debug=True)
