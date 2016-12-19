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
        print('\t'.join([
            'Position',
            'Well',
            'Sample reference',
            'Customer\'s sample reference',
            'Library count',
            'Taxon name',
            'Project reference',
            'Gram staining type',
            'GC content %',
            'Genome size mb',
            'Target coverage'
        ]))
        for r in sorted(response.json()['data'],
                        key=lambda x: int(x['container_position'])):
            print('\t'.join([
                r['container_position'],
                r['container_index_alpha'],
                r['Sample::reference'],
                r['Sample::customers_ref'],
                r['Sample::unstored_library_count'],
                r['Sample::taxon_name'],
                r['Project::reference'],
                r['Sample::gram_staining_type'],
                r['Taxon::uc_closest_gc_content'],
                r['Taxon::uc_closest_genome_size_mb'],
                r['unstored_last_target_coverage']
            ]))

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

def update_samples(args):
    """Update sample record(s)"""
    json = {'meta': [], 'data': []}
    field_names = ['suspected_contamination']
    for f, v in ((f, getattr(args, f)) for f in field_names if getattr(args, f)):
        for s in args.ref:
            v = getattr(args, f)
            json['meta'].append({'recordID': 'reference==={}'.format(s)})
            json['data'].append({f: int(v) if type(v) is bool else v})
    print(json)
    try:
        response = limsfm_request('bulk/sample_api', 'put', json=json)
    except requests.RequestException as e:
        print(e.response.text)

