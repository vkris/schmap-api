import urllib
import re,sys,os
import time
import urllib2, urllib
import base64
try:
    import json
except ImportError,e:
    import simplejson as json

import threading, Queue

sys.path.append(".")
from exception import SchmapAPIException
from schmap_api import log

class SchmapAPIClient:
    api_username = ""
    api_password = ""
    frequency = 5
    api_version=1
    base_uri="https://www.schmap.it/api/social_analysis/"
    request_queue = Queue.Queue()
    no_of_threads = 5
    out_dir = "/tmp/schm_test/"
    counter = 0
    max_wait_time = 60 # seconds
    sleep_time = 3 # seconds
    request_ids_file = "queue.out"

    def __init__(self, username, password, base_uri=""):
        self.api_username = username
        self.api_password = password
        log.debug("Setting username and password")

    def set_crendentials(self, username, password):
        self.api_username = username
        self.api_password = password
        log.debug("Setting credentitals")

    def set_frequency(self, frequency):
        self.frequency = frequency


    def set_base_uri(self,uri):
        self.base_uri = uri

    def set_output_file(self, filename):
        self.out_file = filename

    def request_uri(self,uri,data={}):
        data = urllib.urlencode(data)
        if len(data) > 0:
            # Makes a POST request
            request = urllib2.Request(uri,data)
        else:
            # Makes a GET request
            request = urllib2.Request(uri)
        base64string = base64.encodestring('%s:%s' % 
                (self.api_username, self.api_password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        try:
            return urllib2.urlopen(request).read()
        except urllib2.HTTPError,e:
            if (e.code == 401):
                raise SchmapAPIException(401)
    
    def analyze_account(self, user_list):
        uri = self.base_uri + "analyze_account"
        for user in user_list:
            post = {"screen_name":user, "analysis_type":"profiled_dataset"}
            self.analyze(uri, post)

    def analyze_list(self, user_list, list_name):
        post = {"list_members":"|".join(user_list), "list_name":list_name, "analysis_type":"profiled_dataset"}
        uri = self.base_uri + "analyze_list"
        self.analyze(uri, post)
        

    def analyze(self, uri, post):
        response = self.request_uri(uri, post)
        log.info("Response :"+ response)
        try:
            response = self.get_response(response)
        except SchmapAPIException,e :
            log.info(str(e))
        
        request_id = response["request_id"]
        try:
            data = str(request_id)+"##"+post['list_name']
            self.request_queue.put(data)
        except KeyError,e:
            data = str(request_id)+"##"+post['screen_name']
            self.request_queue.put(data)
        self.save_to_file(data+"\n",self.request_ids_file) 

    
    def check_status(self, request_id):
        self.counter = self.counter + 1
        if request_id < 0: 
            raise SchmapAPIException(7004)
        uri = self.base_uri + "get_status?request_id="+str(request_id)
        response = self.get_response(self.request_uri(uri))
        p_complete = response['percent_complete']
        if (p_complete != 100):
            log.info("Completed "+str(p_complete)+"% for request_id "+str(request_id))
            time.sleep(self.sleep_time)
            if( self.counter > ( self.max_wait_time / self.sleep_time)):
                    raise SchmapAPIException(7005)
            self.check_status(request_id)            
        else:
            log.info("Completed "+str(p_complete)+"% for request_id "+str(request_id))
            return 0

    def get_data(self):
        threads = []
        for i in range(self.no_of_threads):
            t = threading.Thread(target=self.get_data_thread)
            threads.append(t)
            t.start()
        for t in threads: t.join()
        return 0

    def get_data_thread(self, filename):
        for line in open(filename):
            request_id, list_name = line.strip().split('##')
            self.check_status(request_id)
            uri = self.base_uri + "get_dataset?request_id=" + str(request_id)
            response = self.request_uri(uri)
            self.save_to_file(response,request_id+"_"+list_name)

    def get_data_thread(self,filename=""):
        def fetch():
            self.check_status(request_id)
            uri = self.base_uri + "get_dataset?request_id=" + str(request_id)
            response = self.request_uri(uri)
            self.save_to_file(response,request_id+"_"+list_name+".json")

        if (filename == ""):
            try:
                request_id,list_name = self.request_queue.get(block=0).split('##')
                fetch()
            except Queue.Empty,e:
                return
        else:
            for line in open(filename):
                request_id,list_name = line.strip().split('##')
                fetch()

    def save_to_file(self, response,filename):
        try:
            os.mkdir(self.out_dir)
        except OSError, e:
            log.debug("Folder already exists, "+ str(e))
        try:
            fp = open(self.out_dir+"/"+str(filename), 'a')            
            fp.write(response)
            fp.close()
        except IOError,e:
            log.info("Cannot create file"+str(e))


    def get_response(self, response):
        if (response == ""):
            log.info("Empty Response")
            raise SchmapAPIException(7000)
        elif (response.startswith("<!DOCTYPE HTML")):
            log.debug("No the expected response")
            raise SchmapAPIException(7001) 
        else:
            try:
                json_response = json.loads(response)
            except json.decoder.JSONDecodeError, e:
                raise SchmapAPIException(7003)
            try:
                if (json_response['code'] == 0):
                    return json_response
                else:
                    raise SchmapAPIException(json_response['code'])
            except KeyError,e:
                raise SchmapAPIException(7000)

    def catch_up(self, filename=""):
        if (filename == ""):
            filename  = self.out_dir+"/"+self.request_ids_file
        self.get_data_thread(filename)


