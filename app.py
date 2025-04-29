from database import Users, Scheduling, app, db
from flask import request, jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash
import jwt

# ========== ROTAS DE AUTENTICAÇÃO ==========
@app.route('/register', methods= ['POST'])
def register():
    data= request.get_json()
    name= data.get('name')
    email= data.get('email')
    password= data.get('password')
    type= data.get('type')
    
    if not all([name, email, password, type]):
        return jsonify({'message': 'Por favor preencha todos os campos.'}, 400)
    
    existing_user= Users.query.filter_by(email= email).first()
    if existing_user:
        return jsonify({'message': 'Email já cadastrado no sistema.'})
    
    hashed_password= generate_password_hash(password)
    user= Users(name= name, email= email, password= hashed_password, type= type)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuário registrado no sistema.'}, 200)

@app.route('/login', methods= ['POST'])
def login():
    pass


# ========== ROTAS DE AGENDAMENTO ==========
@app.route('/appointments', methods= ['GET'])
def list_appointments():
    appointments= Scheduling.query.all()
    result= []
    
    for appt in appointments:
        result.append({
            'id': appt['id'],
            'paciente_nome': appt['paciente_nome'],
            'paciente_email':appt['paciente_email'],
            'medico_nome': appt['medico_nome'],
            'medico_email': appt['medico_email'],
            'especialidade': appt['especialidade'],
            'data': appt['data'],
            'hora': appt['hora'],
            'observacoes': appt['observacoes']
        })
    return jsonify(result, 200)

@app.route('/schedule', methods= ['POST'])
def schedule():
    data= request.get_json()
    new_schedule= Scheduling(
        paciente_nome= data['paciente_nome'],
        paciente_email=data['paciente_email'],
        medico_nome= data['medico_nome'],
        medico_email= data['medico_email'],
        especialidade= data['especialidade'],
        data= data['data'],
        hora= data['hora'],
        observacoes= data['observacoes']
    )
    db.session.add(new_schedule)
    db.session.commit()
    
    return jsonify({'message': 'Consulta agendada com sucesso!'})


app.run(port= 5000, host= 'localhost', debug= True)