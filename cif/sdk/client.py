import json
import requests
import time
import logging
import cif.sdk
import pprint
pp = pprint.PrettyPrinter()

REMOTE ='https://localhost'
LIMIT = 5000

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
        self.session.headers["Accept"] = 'application/vnd.cif.v' + cif.sdk.__api_version__ + 'json'
        self.session.headers['User-Agent'] = 'cif-sdk-python/' + cif.sdk.__version__
        self.session.headers['Authorization'] = 'Token token=' + self.token
        self.session.headers['Content-Type'] = 'application/json'
    
    def search(self,limit=LIMIT,nolog=None,filters={},sort='lasttime'):
        filters['limit'] = limit
        filters['nolog'] = nolog
        
        uri = self.remote + '/observables'
            
        self.logger.debug('uri: %s' % uri)
        self.logger.debug('params: %s', json.dumps(filters))
        
        body = self.session.get(uri, params=filters, verify=self.verify_ssl)
        
        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            return 'request failed: %s' % str(body.status_code)
        
        body = json.loads(body.text)
        body = sorted(body, key=lambda o: o[sort])
        return body

    def submit(self, submit=None, **kwargs):
        '''
        '{"observable":"example.com","confidence":"50",":tlp":"amber",
        "provider":"me.com","tags":["zeus","botnet"]}'
        '''
        if not submit:
            return None
        
        ##TODO - http://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests
        uri = self.remote + '/observables'
        
        self.logger.debug('uri: %s' % uri)
         
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
        uri = str(self.remote) + '/ping'
        body = self.session.get(uri,params={}, verify=self.verify_ssl)
        
        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            return 'request failed: %s' % str(body.status_code)
        
        t1 = (time.time() - t0)
        self.logger.debug('return time: %.15f' % t1)
        return t1
