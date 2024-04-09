import json
import requests
from app import app

def getAxxonCameraList(url):
    loaded = False
    r = requests.get(url)
    if r.status_code != 200:
        return ('Error {} ({}): the translation service failed.'.format(r.status_code, r.reason)), loaded
    rj = json.loads(r.content.decode('utf-8-sig'))
    response = []
    for r in rj['cameras']:
        item = {r['displayName']: r['accessPoint']}
        response.append(item)
        if response.count !=0: loaded=True
    return response, loaded
