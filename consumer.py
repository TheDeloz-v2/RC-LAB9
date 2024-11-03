from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configuracion del servidor Kafka
KAFKA_SERVER = 'lab9.alumchat.lol:9092'
TOPIC = '21469'

# Inicializar el consumidor de Kafka
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    group_id='foo2',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Listas para almacenar los datos recibidos
all_temp = []
all_hume = []
all_wind = []

# Configuracion de la grafica
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
ax1.set_title('Temperatura')
ax2.set_title('Humedad')
ax3.set_title('Dirección del Viento')

def animate_plot():
    """
    Function to animate the real-time plotting of temperature, humidity, and wind direction data.
    Parameters:
    
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
        all_wind.append(payload['wind_direction'])

        ax1.clear()
        ax2.clear()
        ax3.clear()

        ax1.plot(all_temp, label='Temperatura (°C)')
        ax2.plot(all_hume, label='Humedad (%)')
        ax3.plot(all_wind, label='Dirección del Viento', linestyle='-', marker='o')
        
        # Etiquetas y leyendas
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper left')
        ax3.legend(loc='upper left')
        ax1.set_title('Temperatura')
        ax2.set_title('Humedad')
        ax3.set_title('Dirección del Viento')
        
        break

# Configurar animacion
ani = animation.FuncAnimation(fig, animate_plot, interval=1000)

plt.tight_layout()
plt.show()
