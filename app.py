import streamlit as st
import mysql.connector
import paho.mqtt.publish as publish

# Configuración de conexión MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="iot_datos_budnik"
)

# Consulta los datos
def obtener_datos():
    cursor = db.cursor()
    cursor.execute("SELECT sensor, eje_x, eje_y, eje_z, total, timestamp FROM vibraciones ORDER BY timestamp DESC LIMIT 100")
    return cursor.fetchall()

# Botón para controlar el envío de datos desde el ESP32
def controlar_envio(estado: bool):
    publish.single(
        topic="control/maquina1",
        payload="ON" if estado else "OFF",
        hostname="k7a1e7ea.ala.us-east-1.emqxsl.com",
        port=8883,
        auth={'username': "EM", 'password': "EM21082002"}
    )

# UI Streamlit
st.title("🔧 Dashboard IoT - Vibraciones")
if st.button("🟢 Activar envío de datos"):
    controlar_envio(True)
    st.success("Envío activado")

if st.button("🔴 Desactivar envío de datos"):
    controlar_envio(False)
    st.warning("Envío desactivado")

# Mostrar tabla con datos
datos = obtener_datos()
st.subheader("📊 Últimos datos registrados")
for fila in datos:
    st.text(f"Sensor: {fila[0]}, X: {fila[1]}, Y: {fila[2]}, Z: {fila[3]}, Total: {fila[4]}, Hora: {fila[5]}")
