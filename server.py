#!flask/bin/python
from flask import Flask, jsonify, make_response,request
from bulbman import BulbManager

##########################################################################################
# Python Home Bulb Server
##########################################################################################

app = Flask(__name__, static_url_path = "")
bman = BulbManager()

@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/', methods = ['POST'])
def doAlexa():
	name = request.json['request']['intent']['name']
	text = ""
	if name == "Bulb" :
		slots = request.json['request']['intent']['slots']
		if 'value' in slots['command']:
			value = slots['command']['value']
			if value == "on":
				bman.bulbsOn()
				text = "Turning lights on"
			else:
				bman.bulbsOff()
				text = "Turning lights off"
		elif 'value' in slots['setting']:
			setting = slots['setting']['value']
			value = slots['value']['value']
			if setting == "temperature":
				bman.bulbsTemperature(int(value))
				text = "Setting temperature to "+value
			else:
				bman.bulbsBrightness(int(value))
				text = "Setting brightness to "+value

	return jsonify({
	"version":"1.0",
	"response":{
		"outputSpeech":{
			"type": "PlainText",
			"text": text
		},
		"shouldEndSession":True
	},
	"sessionAttributes":{}
	})

@app.route('/api/on', methods = ['GET'])
def bulbOn():
	bman.bulbsOn()
	return jsonify( {'State':'On'} )

@app.route('/api/off', methods = ['GET'])
def bulbOff():
	bman.bulbsOff()
	return jsonify( {'State':'Off'} )

@app.route('/api/brightness/<int:value>', methods = ['GET'])
def bulbBrightness(value):
	if value >= 1 and value <= 10:
		bman.bulbsBrightness(value)
		return jsonify( { 'Brightness': value } )
	else:
		return jsonify( { 'Error': 'Value must be between 1 and 10' } )

@app.route('/api/temp/<int:value>', methods = ['GET'])
def bulbTemp(value):
	if value >= 1 and value <= 10:
		bman.bulbsTemperature(value)
		return jsonify( { 'Temperature': value } )
	else:
		return jsonify( { 'Error': 'Value must be between 1 and 10' } )

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8991, debug= True)

