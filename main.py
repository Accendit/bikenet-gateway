from flask import Flask, request
from flask_restful import Api, Resource
from Bike import Bike
from serial import Serial
from time import sleep

app = Flask(__name__)
api = Api(app)
ser = Serial(port='COM4', baudrate=9600, timeout=2)
sleep(2)
bike = Bike(ser)

#
# Resources
#

class UpdateResource(Resource):
    def get(self):
        return bike.getStatus()

api.add_resource(UpdateResource, '/status')

class UnlockResource(Resource):
    def post(self):
        bike.unlock()

api.add_resource(UnlockResource, '/unlock')


#
# Main
#

if __name__ == '__main__':
    # initialiseer seriele Bike

    app.run(port='80', debug=True, use_reloader=False)
    
    ser.close()