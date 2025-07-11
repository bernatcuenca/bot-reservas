from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Conexión a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Calendario_Reservas_Demo").sheet1

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    mensaje = data.get("mensaje", "").lower()
    telefono = data.get("telefono", "")

    if "reservar" in mensaje:
        reservas = sheet.get_all_records()
        for i, fila in enumerate(reservas):
            # Convertimos el valor del cliente a texto antes de hacer .lower()
            if str(fila["Cliente"]).lower() == "vacío":
                # Reservamos en la hoja
                sheet.update_cell(i + 2, 3, telefono)
                return jsonify({
                    "respuesta": f"Reservado para las {fila['Hora']} el {fila['Fecha']}"
                })

        return jsonify({"respuesta": "No quedan horas libres."})

    return jsonify({"respuesta": "Hola, ¿quieres reservar una hora?"})

if __name__ == "__main__":
    app.run(debug=True)
