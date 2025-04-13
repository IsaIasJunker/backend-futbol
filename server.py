

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Lista donde almacenamos los jugadores y arqueros
jugadores = []

# Objeto jugador
class Jugador:
    def __init__(self, numCamiseta, apellido, posicion, minJugados):
        self.numCamiseta = numCamiseta
        self.apellido = apellido
        self.posicion = posicion
        self.minJugados = minJugados
    def to_dict (self):
        return {
            "numCamiseta": self.numCamiseta,
            "apellido":self.apellido,
            "posicion":self.posicion,
            "minJugados":self.minJugados
        }
    
# Objeto Arquero
class Arquero(Jugador):
    def __init__(self, numCamiseta, apellido, minJugados):
        super().__init__(numCamiseta, apellido, "arquero", minJugados)
    
# Objeto JugadorCompleto
class JugadorCompleto(Jugador):
    def __init__(self,numCamiseta, apellido, posicion, minJugados, goles):
        super().__init__ (numCamiseta, apellido, posicion, minJugados)
        self.goles = goles
    
    def to_dict(self):
        data = super().to_dict()
        data["goles"]=self.goles
        return data
     
# Endpoint que permite agregar jugadores    
@app.route("/jugadores", methods=["POST"])
def agregar_jugador():
    data = request.get_json()
 
# Condición para verificar si el jugador es arquero o jugador de campo"
    if data["posicion"] == "arquero":
        jugador = Arquero(numCamiseta=data["numCamiseta"], apellido=data["apellido"], minJugados=data["minJugados"])
    else:
        jugador = JugadorCompleto(numCamiseta=data["numCamiseta"], apellido=data["apellido"], posicion=data["posicion"],
                                  minJugados=data["minJugados"], goles=data.get("goles", 0))
    
    # Verifico que minJugados no sea menor que 0 
    if data["minJugados"]  < 0:
        return jsonify({"Mensaje": "ERROR! El tiempo no puede ser menor que cero"}),404
    
    jugadores.append(jugador)
    return jsonify({"mensaje": "Jugador agregado correctamente"}),200 


# Endpoint que obtiene todos los jugadores de la lista "jugadores"
@app.route("/jugadores",methods=["GET"])
def obtener_jugadores():
    return jsonify({"jugadores": [j.to_dict() for j in jugadores]}),200


if __name__ == "__main__":
    app.run(debug=True)