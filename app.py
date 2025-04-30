from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, jsonify, make_response
from database import Users, Scheduling, app, db
from datetime import datetime, timedelta
from functools import wraps
import jwt

# ========== AUTENTICAÇÃO ==========

def mandatory_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token ausente'}), 401

        try:
            result = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = Users.query.filter_by(id=result['id']).first()
        except:
            return jsonify({'message': 'Token inválido.'}), 401

        return f(user, *args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    type = data.get('type')

    if not all([name, email, password, type]):
        return jsonify({'message': 'Por favor preencha todos os campos.'}), 400

    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email já cadastrado no sistema.'})

    hashed_password = generate_password_hash(password)
    user = Users(name=name, email=email, password=hashed_password, type=type)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuário registrado no sistema.'}), 200

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Fill in the fields', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    user = Users.query.filter_by(email=auth.username).first()
    if not user or not check_password_hash(user.password, auth.password):
        return make_response('Login Inválido', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    token_payload = {
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=60)
    }
    token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token})


# ========== AGENDAMENTO ==========

@app.route('/consultas', methods=['GET'])
@mandatory_token
def list_appointments(current_user):
    appointments = Scheduling.query.all()
    result = []

    for appt in appointments:
        result.append({
            'id': appt.id,
            'paciente_nome': appt.paciente_nome,
            'paciente_email': appt.paciente_email,
            'medico_nome': appt.medico_nome,
            'medico_email': appt.medico_email,
            'especialidade': appt.especialidade,
            'data': appt.data.strftime('%Y-%m-%d'),
            'hora': appt.hora.strftime('%H:%M'),
            'observacoes': appt.observacoes
        })
    return jsonify(result), 200

@app.route('/consultas/<int:id>', methods=['GET'])
@mandatory_token
def get_appointment(current_user, id):
    appt = Scheduling.query.filter_by(id=id).first()
    if not appt:
        return jsonify({'message': 'Consulta não encontrada.'}), 404

    return jsonify({
        'id': appt.id,
        'paciente_nome': appt.paciente_nome,
        'paciente_email': appt.paciente_email,
        'medico_nome': appt.medico_nome,
        'medico_email': appt.medico_email,
        'especialidade': appt.especialidade,
        'data': appt.data.strftime('%Y-%m-%d'),
        'hora': appt.hora.strftime('%H:%M'),
        'observacoes': appt.observacoes
    }), 200

@app.route('/consultas/paciente/<string:name>', methods=['GET'])
@mandatory_token
def get_patient(current_user, name):
    appointments = Scheduling.query.filter_by(paciente_nome=name).all()
    if not appointments:
        return jsonify({'message': 'Nenhuma consulta encontrada para esse paciente.'}), 404

    result = [{
        'id': appt.id,
        'paciente_nome': appt.paciente_nome,
        'paciente_email': appt.paciente_email,
        'medico_nome': appt.medico_nome,
        'medico_email': appt.medico_email,
        'especialidade': appt.especialidade,
        'data': appt.data.strftime('%Y-%m-%d'),
        'hora': appt.hora.strftime('%H:%M'),
        'observacoes': appt.observacoes
    } for appt in appointments]

    return jsonify(result), 200

@app.route('/consultas/medico/<string:name>', methods=['GET'])
@mandatory_token
def get_doctor(current_user, name):
    appointments = Scheduling.query.filter_by(medico_nome=name).all()
    if not appointments:
        return jsonify({'message': 'Nenhuma consulta encontrada para esse médico.'}), 404

    result = [{
        'id': appt.id,
        'paciente_nome': appt.paciente_nome,
        'paciente_email': appt.paciente_email,
        'medico_nome': appt.medico_nome,
        'medico_email': appt.medico_email,
        'especialidade': appt.especialidade,
        'data': appt.data.strftime('%Y-%m-%d'),
        'hora': appt.hora.strftime('%H:%M'),
        'observacoes': appt.observacoes
    } for appt in appointments]

    return jsonify(result), 200

@app.route('/consultas', methods=['POST'])
@mandatory_token
def create_schedule(current_user):
    data = request.get_json()

    try:
        # Converta para tipos apropriados
        data_formatada = datetime.strptime(data['data'], '%Y-%m-%d').date()
        hora_formatada = datetime.strptime(data['hora'], '%H:%M').time()
    except ValueError:
        return jsonify({'message': 'Formato inválido de data ou hora. Use "YYYY-MM-DD" para data e "HH:MM" para hora.'}), 400

    if Scheduling.query.filter_by(data= data_formatada, hora= hora_formatada).first():
        return jsonify({'message': 'Já existe uma consulta agendada nesse horário.'}, 409)

    new_schedule = Scheduling(
        paciente_nome=data['paciente_nome'],
        paciente_email=data['paciente_email'],
        medico_nome=data['medico_nome'],
        medico_email=data['medico_email'],
        especialidade=data['especialidade'],
        data=data_formatada,
        hora=hora_formatada,
        observacoes=data['observacoes']
    )

    db.session.add(new_schedule)
    db.session.commit()

    return jsonify({'message': 'Consulta agendada com sucesso!'})

@app.route('/consultas/<int:id>', methods=['PUT'])
@mandatory_token
def update_appointment(current_user, id):
    appointment = Scheduling.query.get(id)
    if not appointment:
        return jsonify({'message': 'Consulta não encontrada'}), 404

    data = request.get_json()

    try:
        if data.get('data'):
            appointment.data = datetime.strptime(data['data'], '%Y-%m-%d').date()
        if data.get('hora'):
            appointment.hora = datetime.strptime(data['hora'], '%H:%M').time()
    except ValueError:
        return jsonify({'message': 'Formato inválido de data ou hora. Use "YYYY-MM-DD" para data e "HH:MM" para hora.'}), 400

    if 'observacoes' in data:
        appointment.observacoes = data['observacoes']

    db.session.commit()
    
    #retornando consulta atualizada
    return jsonify(
        {'message': 'Consulta atualizada com sucesso'},
        {
            'id': appointment.id,
            'paciente_nome': appointment.paciente_nome,
            'paciente_email': appointment.paciente_email,
            'medico_nome': appointment.medico_nome,
            'medico_email': appointment.medico_email,
            'especialidade': appointment.especialidade,
            'data': appointment.data.strftime('%Y-%m-%d'),
            'hora': appointment.hora.strftime('%H:%M'),
            'observacoes': appointment.observacoes
        }, 200)

@app.route('/consultas/<int:id>', methods=['DELETE'])
@mandatory_token
def delete_schedule(current_user, id):
    appointment = Scheduling.query.get(id)
    if not appointment:
        return jsonify({'message': 'Consulta não encontrada'}), 404

    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Consulta excluída com sucesso.'}), 200

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)