import time
import random
import json
from kafka import KafkaProducer
from sensor_simulation import get_data, convert_to_json

# Configuración del servidor Kafka
KAFKA_SERVER = 'lab9.alumchat.lol:9092'
TOPIC = '21469'

def wait_interval():
    """
    Pauses the execution of the program for a random interval between 15 and 30 seconds.

    Returns:
        None
    """
    wait_time = random.randint(15, 30)
    print(f"Waiting for {wait_time} seconds.")
    time.sleep(wait_time)

def send_data_with_retry(producer, topic, data, retries=3):
    """
    Sends data to a specified topic using the provided producer with retry logic.

    Args:
        producer: The producer instance used to send data.
        topic (str): The topic to which the data will be sent.
        data (bytes): The data to be sent.
        retries (int, optional): The number of retry attempts in case of failure. Defaults to 3.

    Raises:
        Exception: If the data cannot be sent after the specified number of retries.
    """
    for i in range(retries):
        try:
            producer.send(topic, key=b'sensor1', value=data)
            print(f"Data sent: {data}")
            break
        except Exception as e:
            print(f"Error sending data: {e}")
            if i < retries - 1:
                print("Retrying...")
                time.sleep(1)
            else:
                print("Failed to send data after several attempts.")

# Inicializar el productor de Kafka
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception as e:
    print(f"Kafka connection error: {e}")
    exit(1)

# Bucle principal de envio de datos
try:
    print("Starting data transmission to the Kafka Broker...")
    while True:
        # Generar datos de los sensores
        sensor_data = get_data()
        
        # Enviar datos al tema en Kafka
        send_data_with_retry(producer, TOPIC, sensor_data)
        wait_interval()

except KeyboardInterrupt:
    print("Interrupted by the user. Ending data transmission.")
finally:
    # Cerrar el productor de Kafka
    producer.close()
