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
    response = limsfm_request('layout/aliquot_plate_meta', 'get', {
        'RFMsF1': 'Procedure::reference',
        'RFMsV1': args.ref,
        'RFMsF2': 'aliquottype_id',
        'RFMsV2': 1,
        'RFMmax': 0
    })
    for r in sorted(response.json()['data'],
                    key=lambda x: x['container_position']):
        print('{}\t{}'.format(
            r['container_position'],
            r['unstored_project_plate_row']))


def queue_bioinformatics(args):
    pass


def set_project_results_path(args):
    """Update project results path"""
    json = {'data': [{'results_path': args.results_path}]}
    uri = ('layout/project_api/%(field)s%(value)s' %
           {
               'field': urllib.quote('reference==='),
               'value': urllib.quote(args.project_ref)
           })
    try:
        response = limsfm_request(uri, 'put', json=json)
    except Exception as e:
        print(e.response.text)
    print(response)

