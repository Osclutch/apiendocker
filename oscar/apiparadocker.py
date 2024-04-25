from flask import Flask, request, jsonify
from cryptography.fernet import Fernet


app = Flask(__name__)
encryption_key = None
cipher_suite = None


#Clave de encriptacion
@app.route('/generar_clave', methods=['GET'])
def generar_clave():
    global encryption_key, cipher_suite
    encryption_key = Fernet.generate_key()
    cipher_suite = Fernet(encryption_key)
    return jsonify({'clave': encryption_key.decode()})

#Despliegue de endpoint para desplegar mensaje en JSON
@app.route('/despliegue_mensaje', methods=['GET'])
def despliegue_mensaje():
    mensaje = request.args.get('SPEEDY')
    return jsonify({'El Mensaje que queria el Prof': mensaje})

#Encriptacion de mensaje
@app.route('/encriptacion', methods=['POST'])
def encriptacion():
    if cipher_suite is None:
        return jsonify({'ERROR': 'No se ha definido la clave de encriptacion'})
    data = request.get_json()
    text = data['mensaje']
    token = cipher_suite.encrypt(text.encode())
    return jsonify({'mensaje_encriptado': token.decode()})

#Desencriptacion de mensaje
@app.route('/desencriptacion', methods=['POST'])
def desencriptacion():
    if cipher_suite is None:
        return jsonify({'ERROR': 'No se ha definido la clave de encriptacion'})
    data = request.get_json()
    token = data['mensaje_encriptado']
    text = cipher_suite.decrypt(token.encode())
    return jsonify({'mensaje_desencriptado': text.decode()})

#Validacion de token
@app.route('/validar_token', methods=['POST'])
def validar_token():
    if cipher_suite is None:
        return jsonify({'ERROR': 'No se ha definido la clave de encriptacion'})
    data = request.get_json()
    token = data['token']
    try:
        cipher_suite.decrypt(token.encode())
        return jsonify({'valido': True})
    except:

        return jsonify({'valido': False})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port= 3000)

