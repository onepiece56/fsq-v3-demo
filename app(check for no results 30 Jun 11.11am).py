import flask
import requests
import json
from flask_session import Session
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask import request, url_for, render_template, redirect

app = flask.Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
@app.route("/")
def my_maps():

  mapbox_access_token = 'pk.eyJ1IjoiamluamluNTYiLCJhIjoiY2twNmswNnQ2MmlsMzJucXdpbDRudDI4bSJ9.wKq3aKfwVIXDnLWaQvwH2w'

  return render_template('index.html',
        mapbox_access_token=mapbox_access_token)


@app.route("/gettips", methods=['GET'])
@cross_origin()

def get_tips():
    encoding = 'utf-8'
    venue_id = request.args.get('venueid')
    print('venue_id is:', venue_id)
    request_url = 'https://api.foursquare.com/v3/places/' + venue_id + '/tips'
    print('request url is', request_url)
    response = requests.get(request_url,
    headers={'Accept': 'application/json',
 'Access-Control-Allow-Origin':'*',
    'Authorization': 'fsq321oPL4Ew/sI8I+k1SVrdcUjFa5QuCQSiZ6lpU1rozQk='})
    temp_res = []
    temp_res = response.json()
    print('response is, ', temp_res)
    tips_results = temp_res
    print(tips_results)
    return{'tips_results':tips_results}

@app.route("/getphotos", methods=['GET'])
@cross_origin()

def get_photos():
    encoding = 'utf-8'
    venue_id = request.args.get('venueid')
    print('venue_id is:', venue_id)
    request_url = 'https://api.foursquare.com/v3/places/' + venue_id + '/photos'
    print('request url is', request_url)
    response = requests.get(request_url,
    headers={'Accept': 'application/json',
 'Access-Control-Allow-Origin':'*',
    'Authorization': 'fsq321oPL4Ew/sI8I+k1SVrdcUjFa5QuCQSiZ6lpU1rozQk='})
    temp_res = []
    temp_res = response.json()
    print('response is, ', temp_res)
    photo_results = temp_res
    print(photo_results)
    return {'photo_results':photo_results}

@app.route("/autocomplete", methods=['GET'])
@cross_origin()

def suggest_complete():
    encoding = 'utf-8'
    query = str(request.query_string, encoding)
    print('query is:', query)
    request_url = 'https://api.foursquare.com/v3/autocomplete?' + query
    print('request url is', request_url)
    response = requests.get(request_url,
    headers={'Accept': 'application/json',
 'Access-Control-Allow-Origin':'*',
    'Authorization': 'fsq321oPL4Ew/sI8I+k1SVrdcUjFa5QuCQSiZ6lpU1rozQk='})
    temp_res = []
    temp_res = response.json()
    print(response)
    suggest_results = temp_res["results"]
    print(suggest_results)
    return {'suggest_results':suggest_results}

@app.route('/search',methods=['GET','POST'])
@cross_origin()
def venue_search():
    #print('searching')
    #print(request.query_string)
    encoding = 'utf-8'
    query = str(request.query_string, encoding)
    #query = request.query_string
    print('query is: ',query)
    request_url = 'https://api.foursquare.com/v3/places/search?' + query
    print('request url is: ',request_url)
    response = requests.get(request_url,
    headers={'Accept': 'application/json',
 'Access-Control-Allow-Origin':'*',
    'Authorization': 'fsq321oPL4Ew/sI8I+k1SVrdcUjFa5QuCQSiZ6lpU1rozQk='})
    temp_res = []
    temp_res = response.json()
    print(response)
    # if temp_res["results"]:
    fsq_results = temp_res["results"]
    print(fsq_results)
    results_geojson = []
    no_results = []
    map_center = []
    results_geojson = fsq_result_to_geojson(fsq_results)
    for venue in fsq_results:
        request_url = 'https://api.foursquare.com/v3/places/' + venue["fsq_id"] +\
        '?fields=description,tel,fax,email,website,social_media,verified,hours,hours_popular,rating,stats,price,tastes,menu,date_closed,photos,tips'
        print('request url is: ',request_url)
        response = requests.get(request_url,
        headers={'Accept': 'application/json',
     'Access-Control-Allow-Origin':'*',
        'Authorization': 'fsq321oPL4Ew/sI8I+k1SVrdcUjFa5QuCQSiZ6lpU1rozQk='})
        details_res = []
        details_res = response.json()
        venue["rich"] = details_res
        print(venue)
    #print(results_geojson)
    mapbox_access_token = 'pk.eyJ1IjoiamluamluNTYiLCJhIjoiY2twNmswNnQ2MmlsMzJucXdpbDRudDI4bSJ9.wKq3aKfwVIXDnLWaQvwH2w'
    # return render_template("index.html",no_results=no_results,
    #                         results_geojson=results_geojson, map_center=map_center,
    #                         fsq_results=fsq_results,
    #                         mapbox_access_token=mapbox_access_token)
    return({'fsq_results': fsq_results,'results_geojson':results_geojson})
#    return jsonify(fsq_results)

def fsq_result_to_geojson(results):
    #print(results)
    #name_results = results[0]["name"];
    geojson = {'type': 'FeatureCollection', 'features': []}
    fsq_array = []
    for row in results:
        feature = {'type': 'Feature',
               'properties': {},
               'geometry': {'type': 'Point',
                            'coordinates': []}}
        feature['geometry']['coordinates'] = [row["geocodes"]["main"]["longitude"], row["geocodes"]["main"]["latitude"]]
        feature['properties']['venuename'] = row["name"]
        feature['properties']['venueid'] = row["fsq_id"]
        feature['properties']['location'] = row["location"]["address"]
        geojson['features'].append(feature)
#    print(geojson)
    return geojson


if __name__ == '__main__':
    app.run(debug=True)
