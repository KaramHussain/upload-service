
#!/usr/bin/env python
# coding: utf-8



from flask import Flask, jsonify, request, flash, redirect, url_for

# import re
import pandas as pd
import json
# import dateutil.parser
# import datetime
# from datetime import timedelta
#import requests
# import x12valid
# import x12xml
import pymongo
from confluent_kafka import Producer
import pymongo
import urllib.request
import os 

# p = Producer({'bootstrap.servers': 'impact-analysis-kafka-service.impact.analysis:9092'})
KAFKA_PRODUCER_URL="kafka.carebidsexchange.com:9092"
p = Producer({'bootstrap.servers': KAFKA_PRODUCER_URL})

# p = Producer({'bootstrap.servers': '127.0.0.1:9092'})

from flask_cors import CORS
import zipfile
import glob

import os
from flask import Flask
from werkzeug.utils import secure_filename

cwd = os.getcwd()



UPLOAD_FOLDER = cwd + '/files'
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# client = pymongo.MongoClient("mongodb://root:breeze123@impact-analysis-mongodb.impact.analysis:27017")

# MONGODB_URL ="mongodb://" + os.environ.get('MONGODB_URL')
MONGODB_URL ="mongodb+srv://kreniltechup:8h2bpzzklhpfsqj8@cluster0.nlmmxd5.mongodb.net"
client = pymongo.MongoClient(MONGODB_URL)
# client = 

db = client["carepays"]

file_status = db['file_status']

def read_no_files(path):
    wrong = []
    right = []

    count = 0

    for filename in glob.iglob(path + '**/**/*', recursive=True):
        #print(filename)
        if len(filename.split('.')) > 1: 
        #if not (x12valid.main([filename,'--"verbose"','-l gm.log','--quiet'],filename)):
            #wrong.append(filename)
        #else:
            #right.append(filename)
            count += 1

    return count


def unzip(path,pt):
    try:
        #print (path)
        with zipfile.ZipFile(path,"r") as zip_ref:
            zip_ref.extractall(pt)
            return 1
    except:
        return 0


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health-check', methods=['GET'])
def health_check():
    return 'OK', 200


@app.route('/eob_load', methods=['POST','OPTIONS'])
def upload_file():
#    if request.method == 'POST':
        # check if the post request has the file part
    
    
    print ("Hello")
    dat = request.get_json()
    print (dat)
    #print(dat['file'])
    '''
    print (request)
    print ('file')
    data = request.form
    print (data)
    f = request.files.to_dict(flat=True)
    file = f['file']
    
    data= data.to_dict(flat=True)
    '''
    data = dat
    
    path = ""
    print ("here")
    
    ff = dat['file']
    filename = dat['filename']
    pt = os.path.join(app.config['UPLOAD_FOLDER'], filename.split('.')[0])
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(ff)
    print(path)
    try:
        demo = urllib.request.urlretrieve(ff, path)
        # subprocess.call(['wget', '-O', path, ff])
    except Exception as e:
        print(e)
        return jsonify("Error while fetching file from given URL")
        
    a = unzip(path,pt)
    print (path)
    print (pt)
    #a = unzip(dat['file']['name'],path)
    if a == 0:
        print ("Error Occured While Unzipping")
        return jsonify("Error Occured While UnZipping.")
    count =read_no_files(pt)
    print ("Done processeing")
    print (count)
    try:
        d= {}
        # if type(data['provider_id'])!= int:
        #     d['provider_id']= int(data['provider_id'])
        # else:
        #      d['provider_id']= data['provider_id']

        d['provider_id']=19   
        d['path'] = pt
        
        d['date_upload'] = data['date_upload']
        d['time_upload'] = data['time_upload']
        d['filename'] = filename
        d['no_of_files'] = int(count)
        d['Status'] = "Uploaded"
        d['date_upload'] = pd.to_datetime(data['date_upload'])
        file_status.insert_one(d)
        if '_id' in d:
            del d['_id']
        d['date_upload'] = data['date_upload']
        print (data['claim_type'])
        
        if data['claim_type'] == '837':
            p.produce("client_data_837", value=json.dumps(d))
        else:    
            p.produce("client_data_835", value=json.dumps(d))
        p.flush()

        
        print (d)
        
        

    except Exception as e:
        print("Found exception while writing data in kafka from producer: "+str(e)+"\n")
        
    print ("Sending Response")
    print (str(count))
    return jsonify("Files Successfully Uploaded: " + str(count))
   
    
    
    
    #"Testing"
    '''
    try:

    if type(data['provider_id'])!= int:
        d['provider_id']= int(data['provider_id'])
    else:
         d['provider_id']= data['provider_id']

    d['path'] = path.split('.')[0]
    
    p.produce("client_data1", json.dumps(dat))
    p.flush()
except Exception as e:
    print("Found exception while writing data in kafka from producer: "+str(e)+"\n")

    return jsonify("Files Successfully Uploaded")
    '''
if __name__ == "__main__":
    app.run(host= '0.0.0.0', port = 4000)