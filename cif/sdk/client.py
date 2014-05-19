import json
import requests
import time
import logging
import cif.sdk

class Client(object):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger') or logging.getLogger(__name__)
        
        self.host = kwargs.get('host')
        self.token = kwargs.get('token')
        self.port = kwargs.get('port')
        self.proxy = kwargs.get('proxy')
        self.timeout = kwargs.get('timeout')
        self.no_verify_ssl = kwargs.get('noverifyssl')
        
        self.session = requests.session()
        self.session.headers["Accept"] = "application/json"
        self.session.headers['User-Agent'] = 'cif-sdk-python/' + cif.sdk.__version__
                
    def search(self, **kwargs):
        confidence = kwargs.get('confidence')
        query = kwargs.get('query')
        limit = kwargs.get('limit') or 500
        token = kwargs.get('token') or self.token()
        group = kwargs.get('group')
       
        uri = self.host + ':' + str(self.port) + '/' + query + '?token=' + token 
         
        if group:
            uri += '&group=' + group
        if confidence:
            uri += '&confidence=' + confidence
        if limit:
            uri += '&limit=' + str(limit)
       
        self.logger.debug(uri)
         
        body = self.session.get(uri, verify=self.no_verify_ssl)
       
        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            return 'request failed: %s' % str(body.status_code)
        
        body = json.loads(body.text)
        return body

    def submit(self, **kwargs):
        '''
        '{"observable":"example.com","confidence":"50",":tlp":"amber",
        "provider":"me.com","tags":["zeus","botnet"]}'
        '''
        token = kwargs.get('token') or self.token
        body = kwargs.get('submit')

        if not body: return None
        
        uri = self.host + ':' + str(self.port) + '/?token=' + token
         
        body = self.session.post(uri,data=body,verify=self.no_verify_ssl)
        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            self.logger.error(json.loads(body.text).get('message'))
            return None
        
        body = json.loads(body.text)
        return body
    
    def ping(self):
        t0 = time.time()
        uri = self.host + ':' + self.port + '/_ping?token=' + self.token
        body = self.session.get(uri)
        
        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            return 'request failed: %s' % str(body.status_code)
        
        t1 = time.time();
        self.logger.debug('return time: %.15f' % (t1-t0))
        return (t1-t0)