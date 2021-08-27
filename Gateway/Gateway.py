from flask import Flask, json, request
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
api = Api(app)


@app.route("/unprotected")
def unprotected():
    response = requests.get("http://jwtapi-service/unprotected")  
    return response.json()

@app.route("/getToken")
def getToken():
    header = {"Authorization": request.headers.get("Authorization")}
    response = requests.get("http://jwtapi-service/getToken", headers=header)
    if response.status_code == 401:
        return "Unauthorized access"
    else:
        return response.json()

@app.route('/protected')
def protected():
    token = request.headers.get('x-access-token')
    header = {'x-access-token': token}
    response = requests.get("http://jwtapi-service/protected", headers=header)
    return response.json()


class VideoResources(Resource):
    def get(self, video_id):
        response = requests.get("http://videoapi-service/video/" + str(video_id))
        return response.json()

    def put(self, video_id):
        response = requests.put("http://videoapi-service/video/" + str(video_id), request.json)
        return response.json()

    def patch(self, video_id):
        response = requests.patch("http://videoapi-service/video/" + str(video_id), request.json)
        return response.json()

    def delete(self, video_id):
        response = requests.delete("http://videoapi-service/video/" + str(video_id))
        if response.status_code == 204:
            return 'Deleted Succesfully', 204
        return response.json()


api.add_resource(VideoResources, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True, port=80, host= "0.0.0.0") #8085