from .apiRoutes import REGISTERS, BICYCLEPARKING, PLACE
from .api import get,post,put,postLogin
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
				"createDate": parkingRegister.hourFoto
			}
		)

	data = {
		"registers": formattedRegisters
	}

	return post(REGISTERS, data, token)

def login():
    user = {'username': 'user_camera', 'password': 'camera12'}
    return postLogin('/auth/login', user)

def getParkings():
	response = get(REGISTERS)
	response = json.loads(response.content)
	registers = []
	for parkingRegister in response:
		parkingRegister_new = Parking(parkingRegister['isEgreso'],parkingRegister['position'],
			parkingRegister['pathFoto'],parkingRegister['hourFoto'],parkingRegister['momento'])
		parkingRegister_new.id = parkingRegister['id']
		registers.append(parkingRegister_new)
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
				"momento": parkingRegister.momento
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
