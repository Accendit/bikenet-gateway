from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# 
# Models
# 


class Update(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True, default=datetime.now)
    bike = db.Column(db.Integer)
    longtitude = db.Column(db.Float)
    latitude = db.Column(db.Float)


#
# Schemas
#


class UpdateSchema(ma.Schema):
    class Meta:
        fields = ("datetime", "bike", "longtitude", "latitude")

update_schema = UpdateSchema()
updates_schema = UpdateSchema(many=True)


#
# RESTful Resources
#


class UpdateListResource(Resource):
    def get(self):
        updates = Update.query.all()
        return updates_schema.dump(updates)

    def post(self):
        new_update = Update(
            bike = request.json['bike'],
            longtitude = request.json['longtitude'],
            latitude = request.json['latitude']
        )
        db.session.add(new_update)
        db.session.commit()
        return update_schema.dump(new_update)


api.add_resource(UpdateListResource, '/updates')


#
# Shit
#

if __name__ == '__main__':
    app.run(port='80', debug=True)