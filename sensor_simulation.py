import random
import struct
import json

# Diccionario para asignacion y decodificacion de valores binarios para la direccion del viento
wind_direction = {
    "N": 0b000,
    "NE": 0b001,
    "E": 0b010,
    "SE": 0b011,
    "S": 0b100,
    "SO": 0b101,
    "O": 0b110,
    "NO": 0b111
}
reverse_wind_direction = {v: k for k, v in wind_direction.items()}

def get_data():
    """
    Simulates sensor data for temperature, humidity, and wind direction.

    Returns:
        dict: A dictionary containing the following keys:
            - "temperature" (float): Simulated temperature value, rounded to 2 decimal places,
              constrained between 0 and 110.
            - "humidity" (int): Simulated humidity value, constrained between 0 and 100.
            - "wind_direction" (str): Simulated wind direction, randomly chosen from predefined directions.
    """
    temperature = max(0, min(round(random.normalvariate(55, 10), 2), 110))
    humidity = max(0, min(int(random.normalvariate(55, 15)), 100))
    direction = random.choice(list(wind_direction.keys()))
    sensor_data = {"temperature": temperature, "humidity": humidity, "wind_direction": direction}
    return sensor_data

def encode(data):
    """
    Encodes sensor data into a binary payload.

    Args:
        data (dict): A dictionary containing sensor data with temperature, humidity and wind_direction.

    Returns:
        bytes: A 3-byte binary payload representing the encoded sensor data.
    """
    temperature = int(data["temperature"] * 100) & 0b11111111111111 # 14 bits
    humidity = int(data["humidity"]) & 0b1111111 # 7 bits
    direction = wind_direction[data["wind_direction"]] & 0b111 # 3 bits
    payload = (temperature << 10) | (humidity << 3) | direction # 24 bits
    return struct.pack('>I', payload)[1:]  # 3 bytes

def decode(data):
    """
    Decodes the given binary data into a dictionary containing temperature, humidity, and wind direction.
    
    Args:
        data (bytes): A 3-byte binary string containing encoded sensor data.
        
    Returns:
        dict: A dictionary containing sensor data with temperature, humidity and wind_direction.
    """
    payload = struct.unpack('>I', b'\x00' + data)[0]
    temperature = ((payload >> 10) & 0b11111111111111) / 100
    humidity = (payload >> 3) & 0b1111111
    wind_direction_bits = payload & 0b111
    direction = reverse_wind_direction[wind_direction_bits]
    return {"temperature": round(temperature, 2), "humidity": humidity, "wind_direction": direction}