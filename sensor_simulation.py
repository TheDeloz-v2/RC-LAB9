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
    "SW": 0b101,
    "W": 0b110,
    "NW": 0b111
}
reverse_wind_direction = {v: k for k, v in wind_direction.items()}

def convert_to_json(data):
    return json.dumps(data)

def get_data():
    temperature = max(0, min(round(random.normalvariate(55, 10), 2), 110))
    humidity = max(0, min(int(random.normalvariate(55, 15)), 100))
    direction = random.choice(list(wind_direction.keys()))
    sensor_data = {"temperature": temperature, "humidity": humidity, "wind_direction": direction}
    return sensor_data

def encode(data):
    temperature = int(data["temperature"] * 100) & 0b111111111111
    humidity = int(data["humidity"]) & 0b1111111
    direction = wind_direction[data["wind_direction"]]
    payload = (temperature << 20) | (humidity << 13) | (direction << 10)
    return struct.pack('>I', payload)

def decode(data):
    payload = struct.unpack('>I', data)[0]
    temperature = ((payload >> 20) & 0b111111111111) / 100
    humidity = (payload >> 13) & 0b1111111
    wind_direction_bits = (payload >> 10) & 0b111
    direction = reverse_wind_direction[wind_direction_bits]
    return {"temperature": round(temperature, 2), "humidity": humidity, "wind_direction": direction}
