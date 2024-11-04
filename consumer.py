from kafka import KafkaConsumer
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.gridspec import GridSpec
from sensor_simulation import decode

# Configuracion del servidor Kafka
KAFKA_SERVER = 'lab9.alumchat.lol:9092'
TOPIC = '21469'

# Inicializar el consumidor de Kafka
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    group_id='foo2',
    value_deserializer=lambda m: decode(m)
)

# Listas para almacenar los datos recibidos
all_temp = []
all_hume = []
all_wind = []
all_colors = []

# Diccionario de direcciones del viento
wind_direction = {
    "N": 0,
    "NE": 45,
    "E": 90,
    "SE": 135,
    "S": 180,
    "SO": 225,
    "O": 270,
    "NO": 315
}

# Configuracion de la grafica
fig = plt.figure(figsize=(10, 10))
gs = GridSpec(4, 1, figure=fig)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[2, 0])
ax4 = fig.add_subplot(gs[3, 0], projection='polar')

ax1.set_title('Temperatura')
ax2.set_title('Humedad')
ax3.set_title('Dirección del Viento (Lineal)')
ax4.set_title('Dirección del Viento (Polar)')

# Etiquetas de los ejes para la dirección del viento
wind_labels = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
wind_angles = [0, 45, 90, 135, 180, 225, 270, 315]

def animate_plot(i):
    """
    Function to animate the real-time plotting of temperature, humidity, and wind direction data.
    Parameters:
        i: Frame index (required by FuncAnimation, but not used here)
    Returns:
        None
    """
    for mensaje in consumer:
        # Procesar el mensaje
        payload = mensaje.value
        print(f"Mensaje recibido: {payload}")
        
        # Almacenar los datos
        all_temp.append(payload['temperature'])
        all_hume.append(payload['humidity'])
        all_wind.append(wind_direction[payload['wind_direction']])
        all_colors.append(np.random.rand(3,))  # Generar un color aleatorio

        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()

        ax1.plot(all_temp, label='Temperatura (°C)')
        ax2.plot(all_hume, label='Humedad (%)')
        ax3.plot(range(len(all_wind)), all_wind, label='Dirección del Viento (°)')
        
        # Graficar la dirección del viento en coordenadas polares con colores aleatorios
        angles = np.deg2rad(all_wind)
        radii = np.ones_like(angles)
        ax4.scatter(angles, radii, c=all_colors, label='Dirección del Viento', marker='o')
        
        # Etiquetas y leyendas
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper left')
        ax3.legend(loc='upper left')
        ax4.legend(loc='upper left')
        ax1.set_title('Temperatura')
        ax2.set_title('Humedad')
        ax3.set_title('Dirección del Viento (Lineal)')
        ax4.set_title('Dirección del Viento (Polar)')
        
        # Configurar etiquetas de los ejes para la dirección del viento
        ax3.set_yticks(wind_angles)
        ax3.set_yticklabels(wind_labels)
        ax4.set_xticks(np.deg2rad(wind_angles))
        ax4.set_xticklabels(wind_labels)
        
        # Salir del bucle después de procesar un mensaje
        break

# Configurar animacion
ani = animation.FuncAnimation(fig, animate_plot, interval=1000)

plt.tight_layout()
plt.show()