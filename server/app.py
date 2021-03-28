from flask import Flask, jsonify
from flask_cors import CORS

import aqi


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
  return jsonify('pong!')

# get a aqi, provided lat and long
@app.route('/aqi/<lat>/<lon>', methods=['GET'])
def get_aqi_lat_long(lat, lon) -> int:
  # strList = latlong.split('/')
  # return jsonify(aqi.lat_lon_mode(float(strList[0]), float(strList[1])))
  print(lat, lon)
  return jsonify(aqi.lat_lon_mode(float(lat), float(lon)))


# get a aqi, provided address
@app.route('/aqi/<string:addr>', methods=['GET'])
def get_aqi_addr(addr) -> int:
  newAddr = addr.strip()
  return jsonify(aqi.addr_mode(newAddr))


if __name__ == '__main__':
    app.run()