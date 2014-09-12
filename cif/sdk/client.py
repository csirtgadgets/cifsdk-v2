import json
import requests
import time
import logging
import cif.sdk
import pprint
pp = pprint.PrettyPrinter()

REMOTE ='https://localhost'

class Client(object):

    def __init__(self, remote=REMOTE, logger=logging.getLogger(__name__), 
                 token=None, proxy=None, timeout=300, no_verify_ssl=False, **kwargs):
        
        self.logger = logger
        self.remote = remote
        self.token = str(token)
        self.proxy = proxy
        self.timeout = timeout
        
        if no_verify_ssl:
            self.verify_ssl = False
        else:
            self.verify_ssl = True
        
        self.session = requests.session()
        self.session.headers["Accept"] = "application/json"
        self.session.headers["X-CIF-Media-Type"] = 'vnd.cif.' + cif.sdk.__api_version__
        self.session.headers['User-Agent'] = 'cif-sdk-python/' + cif.sdk.__version__
    
    def search(self,query=None,remote=None,limit=500,token=None,group=None,
               nolog=False,confidence=None,*args,**kwargs):
        if not token:
            token = self.token
        elif not self.token:
            raise Exception("Required token for server not provided")
        if not remote:
            remote = self.remote
            
        uri = self.remote + '/observables?q=' + query + '&token=' + str(token)
        self.logger.debug(uri)
         
        ## TODO - pass these into requests by param
        if group:
            uri += '&group=' + group
        if confidence:
            uri += '&confidence=' + confidence
        if limit:
            uri += '&limit=' + str(limit)
            
        if nolog:
            uri += '&nolog=1'
       
        self.logger.debug(uri)
        
        body = self.session.get(uri, verify=self.verify_ssl)
        
        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            return 'request failed: %s' % str(body.status_code)
        
        body = json.loads(body.text)
        return body

    def submit(self, token=None, submit=None, **kwargs):
        '''
        '{"observable":"example.com","confidence":"50",":tlp":"amber",
        "provider":"me.com","tags":["zeus","botnet"]}'
        '''
        if not submit:
            return None
        
        if not token:
            token = self.token
            
        token = str(token)
        
        uri = self.remote + '/observables?token=' + token
         
        body = self.session.post(uri,data=submit,verify=self.verify_ssl)
        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            self.logger.error(json.loads(body.text).get('message'))
            return None
        
        body = json.loads(body.text)
        return body
    
    def ping(self):
        t0 = time.time()
        uri = str(self.remote) + '/ping?token=' + str(self.token)
        body = self.session.get(uri,verify=self.verify_ssl)
        
        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            return 'request failed: %s' % str(body.status_code)
        
        t1 = (time.time() - t0)
        self.logger.debug('return time: %.15f' % t1)
        return t1
