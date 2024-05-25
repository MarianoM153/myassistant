from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL en Heroku
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL environment variable set")

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Recordatorio(Base):
    __tablename__ = 'recordatorios'
    id = Column(Integer, Sequence('recordatorio_id_seq'), primary_key=True)
    descripcion = Column(String(250), nullable=False)
    fecha = Column(String(10), nullable=False)
    hora = Column(String(5), nullable=False)

Base.metadata.create_all(engine)

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove()

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    data = request.json
    if not all(k in data for k in ("descripcion", "fecha", "hora")):
        return jsonify({"error": "Faltan datos"}), 400

    descripcion = data['descripcion']
    fecha = data['fecha']
    hora = data['hora']
    
    new_reminder = Recordatorio(descripcion=descripcion, fecha=fecha, hora=hora)
    
    try:
        session.add(new_reminder)
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"message": "Recordatorio agregado con éxito"}), 201

@app.route('/get_reminders', methods=['GET'])
def get_reminders():
    try:
        recordatorios = session.query(Recordatorio).all()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify([{
        'id': r.id,
        'descripcion': r.descripcion,
        'fecha': r.fecha,
        'hora': r.hora
    } for r in recordatorios])

if __name__ == '__main__':
    app.run(debug=True)
