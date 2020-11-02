import requests,json

#Se debe pasar por parámetro
url = 'http://127.0.0.1:8000/api'  

headers = {
    "Content-Type": "application/json"
}

#traer los bicicleteros 
def get(resource):
	return requests.get("{}{}".format(url,resource), headers=headers)

#para crear bicicleteros
def post(resource, data, token):
    headers2 = {
    "Content-Type": "application/json",
	"Authorization": "Token " + token
    }
    return requests.post("{}{}/".format(url,resource),data=json.dumps(data), headers=headers2)

def postLogin(resource, data):
    return requests.post("{}{}/".format(url,resource),data=json.dumps(data), headers=headers)

#ocupado-libre
def put(resource,data):
	return requests.put("{}{}/".format(url,resource),data=json.dumps(data), headers=headers)


