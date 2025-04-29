from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Time, Date, String, CheckConstraint
from werkzeug.security import generate_password_hash

#API Flask
app= Flask(__name__)

#Criar instância do SQL Alchemy
app.config['SECRET_KEY'] = 'Senha#123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scheduling.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db= SQLAlchemy(app)
db:SQLAlchemy

class Users(db.Model):
    __tablename__= 'users'
    id= db.Column(db.Integer, primary_key= True)
    name= db.Column(String, nullable= False)
    email= db.Column(String, nullable= False, unique= True)
    password= db.Column(String, nullable= False)
    type= db.Column(String, nullable= False)
    
    __table_args__= (
        CheckConstraint('type IN ("medico", "paciente", "dev")', name='check_user_type'),
        )

class Scheduling(db.Model):
    __tablename__= 'scheduling'
    id= db.Column(db.Integer, primary_key= True)
    paciente_nome= db.Column(String, nullable= False)
    paciente_email= db.Column(String, nullable= False)
    medico_nome= db.Column(String, nullable= False)
    medico_email= db.Column(String, nullable= False)
    especialidade= db.Column(String, nullable= False)
    data= db.Column(Date, nullable= False)
    hora= db.Column(Time, nullable= False)
    observacoes= db.Column(String)
    
def start_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
if __name__ == '__main__':
    start_db()