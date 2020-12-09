from .apiRoutes import REGISTERS, BICYCLEPARKING, PLACE, BICYCLEPARKINGALL
from .api import get,post,put,postLogin,getBicycleParkings
import json
from register import Register

def postParkings(registers, token):
	formattedRegisters = []
	for parkingRegister in registers:
		formattedRegisters.append(
			{
				"occupied": bool(parkingRegister.isEgreso),
				"placeNumber": parkingRegister.position,
				"pathPhoto": parkingRegister.pathFoto,
				"createDate": parkingRegister.hourFoto,
    			"photoInBase64": parkingRegister.imgBase64
			}
		)

	data = {
		"registers": formattedRegisters
	}

	return post(REGISTERS, data, token)

def login():
    user = {'username': 'admin', 'password': 'admin'}
    return postLogin('/auth/login', user)

def getParkings():
	response = get(REGISTERS)
	response = json.loads(response.content)
	registers = []
	for parkingRegister in response:
		parkingRegister_new = Parking(parkingRegister['isEgreso'],parkingRegister['position'],
			parkingRegister['pathFoto'],parkingRegister['hourFoto'],parkingRegister['imgBase64'])
		parkingRegister_new.id = parkingRegister['id']
		registers.append(parkingRegister_new)
	return registers

def getAllBicycleParkings(token):
	response = getBicycleParkings(BICYCLEPARKINGALL,token)
	response = json.loads(response.content)
	registers = []
	for parkingRegister in response:
		parkingRegister_new = {
				"id": parkingRegister['id'],
				"description": parkingRegister['description'],
				"number": parkingRegister['number'],
				"positionX": parkingRegister['positionX'],
				"positionY": parkingRegister['positionY'],
			}
		registers.append(parkingRegister_new)
		print("Bicicletero: ",parkingRegister['number']," - descripción: ",parkingRegister['description'])
	return registers


def putParkings(registers):
	formattedParkings = []
	for parkingRegister in registers:
		new_park = {
				"id": parkingRegister.id,
				"isEgreso": parkingRegister.isEgreso,
				"position": parkingRegister.position,
				"pathFoto": parkingRegister.pathFoto,
				"hourFoto": parkingRegister.hourFoto,
			    "photoInBase64": parkingRegister.imgBase64
			}
			
		formattedParkings.append(new_park)

	data = {
		"registers": formattedParkings
	}

	return put(PARKINGS,data)

def postBicycleParkings(token):
	data = {
		"number": 0,
		"description": "origen",
		"positionX": 10,
		"positionY": 20
	}

	return post(BICYCLEPARKING, data, token)

def postPlace(token, idPlace):
	data = idPlace

	return post(PLACE, data, token)
