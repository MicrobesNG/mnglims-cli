import json
import requests
import urllib

from .settings import *

def limsfm_request(rel_uri, method='get', params={}, json=None):
    """Send an API request to LIMSfm (RESTfm).
       Returns a response object or raises an exception"""

    params['RFMkey'] = settings.RESTFM_KEY
    uri = (
        "%(base)s%(rel_uri)s.json" %
        {'base': settings.RESTFM_BASE_URL, 'rel_uri': rel_uri}
    )
    s = requests.Session()
    prepped_request = requests.Request(
        method, uri, params=params, json=json).prepare()
    response = s.send(prepped_request, timeout=60)
    response.raise_for_status()

    return response


def get_plate_meta(args):
    """Get tab separated plate meta data"""
    try:
        response = limsfm_request('layout/aliquot_plate_meta', 'get', {
            'RFMsF1': 'Procedure::reference',
            'RFMsV1': args.ref,
            'RFMsF2': 'aliquottype_id',
            'RFMsV2': 1,
            'RFMmax': 0
        })
    except requests.RequestException as e:
        print(e.response.text)
    else:
        for r in sorted(response.json()['data'],
                        key=lambda x: x['container_position']):
            print('{}\t{}'.format(
                r['container_position'],
                r['unstored_project_plate_row']))

def get_queues(args):
    """Get Queue data"""
    try:
        response = limsfm_request('layout/queue_api', 'get', {
            'RFMmax': 0
        })
    except requests.RequestException as e:
        print(e.response.text)
    else:
        print('ID\tName')
        for r in sorted(response.json()['data'],
                        key=lambda x: int(x['sort_order'])):
            print('{}\t{}'.format(
                r['queue_id'],
                r['name']))


def set_sample_queue(args):
    """Set the (most recent projectline queue) for one or more samples refs"""
    script_param = {'queueId': args.queue_id, 'sampleRefList': args.ref}
    uri = 'script/set_sample_queue/REST'
    try:
        response = limsfm_request(uri, 'get', params={'RFMscriptParam': json.dumps(script_param)})
        print(response.text)
    except requests.RequestException as e:
        print(e.response.text)


def set_project_results_path(args):
    """Update project results path"""
    json = {'data': [{'results_path': args.path}]}
    uri = ('layout/project_api/%(field)s%(value)s' %
           {
               'field': urllib.parse.quote('reference==='),
               'value': urllib.parse.quote(args.ref)
           })
    try:
        response = limsfm_request(uri, 'put', json=json)
    except requests.RequestException as e:
        print(e.response.text)

