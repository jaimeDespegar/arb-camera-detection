from .apiRoutes import REGISTERS
from .api import get,post,put
import json
from register import Register

def postParkings(registers):
	formattedRegisters = []
	for parkingRegister in registers:
		formattedRegisters.append(
			{
				"isEgreso": parkingRegister.isEgreso,
				"position": parkingRegister.position,
				"pathFoto": parkingRegister.pathFoto,
				"hourFoto": parkingRegister.hourFoto,
				"momento": parkingRegister.momento,
				"isAlarmActive": parkingRegister.isAlarmActive
			}	
		)

	data = {
		"registers": formattedRegisters
	}

	return post(REGISTERS,data)

def getParkings():
	response = get(REGISTERS)
        # print("Response: %s"%response)
	response = json.loads(response.content)
        # print("Json Response: %s"%response)
	registers = []
	for parkingRegister in response:
		parkingRegister_new = Parking(parkingRegister['isEgreso'],parkingRegister['position'],
			parkingRegister['pathFoto'],parkingRegister['hourFoto'],parkingRegister['momento'])
		parkingRegister_new.id = parkingRegister['id']
		registers.append(parking_new)
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
				"momento": parkingRegister.momento,
				"isAlarmActive": parkingRegister.isAlarmActive
			}
			
		formattedParkings.append(new_park)

	data = {
		"registers": formattedParkings
	}

	return put(PARKINGS,data)
