from flask import Flask, views, jsonify
import flask
from flask.helpers import flash
from flask_restful import Api, Resource, fields, marshal_with, abort, reqparse
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from requests.api import delete
from requests.sessions import session



app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'     #configuring app for sqlAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        #turning off the sqlalchemy notification by flask
db = SQLAlchemy(app)        #wraping the app in sqlalchemy

class videoModel(db.Model):     #defining the model
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)      #defining the attributes of the model
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    # def __repr__(self):
    #     return f"Video(name = {name}, views = {views}, likes = {likes})"

#db.create_all()        #this command should run only once to create the database. Running this command for more than once will reset the data present in the database.

serialize_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'views':fields.Integer,
    'likes':fields.Integer
}
        

video_put_args = reqparse.RequestParser()
video_put_args.add_argument(name = "video_name", type = str, help = "Video name is required", required = True)
video_put_args.add_argument(name = "views", type = int, help = "views is required", required = True)
video_put_args.add_argument(name = "likes", type = str, help = "likes is required", required = True)


video_patch_args = reqparse.RequestParser()
video_patch_args.add_argument(name = "video_name", type = str, help = "Video name is required")
video_patch_args.add_argument(name = "views", type = int, help = "Video name is required")
video_patch_args.add_argument(name = "likes", type = str, help = "Video name is required")

class video(Resource):
    @marshal_with(serialize_fields)
    def get(self, video_id):
        result = videoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message = "No data found for given video id")
        return result
    
    def put(self, video_id):
        result = videoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message = "Data already exists")
        args = video_put_args.parse_args()    
        video = videoModel(id = video_id, name = args['video_name'], views = args['views'], likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return "Added Successfully", 201

    def patch(self, video_id):      #update request
        result = videoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message = "No data found for the given video id")
        args = video_patch_args.parse_args()
        print(args)
        if args['video_name']:
            result.name = args['video_name']
        if args['likes']:
            result.likes = args['likes']
        if args['views']:
            result.views = args['views']
        db.session.commit()
        return "Updated successfully", 200


    def delete(self, video_id):
        result = videoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message = "No data found for given video id")
        db.session.delete(result)
        db.session.commit()
        return '', 204

api.add_resource(video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug = True, port=80, host='0.0.0.0') #8080