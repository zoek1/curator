#!/usr/bin/python3

import requests
import re
import models
import mongoengine
import time

options = {
 'page': 1,
 'limit': 15,
 'has_next': True,
}


def get_grants_endpoint(**options):
    grants_endpoint = 'https://gitcoin.co/grants/cards_info?network=mainnet&state=activetype=all'

    for key, value in options.items():
        grants_endpoint += f'&{key}={value}'
        
    return grants_endpoint
    
grants_endpoint_limited = request = get_grants_endpoint(page=1, limit=6)

def get_grants(options, limit_page=10000):
    grants = []
    
    while options['has_next'] and options['page'] < limit_page:
        grants_endpoint_limited = request = get_grants_endpoint(page=options['page'], limit=options['limit'])
        print(f'100% = ${grants_endpoint_limited}')
        endpoint = requests.get(grants_endpoint_limited)
        grants_json = endpoint.json()
        grants += grants_json['grants']
        # grant_types = grants_json['grant_types']
        options['has_next'] = grants_json['has_next']
        options['count'] = grants_json['count']
        options['num_pages'] = grants_json['num_pages']
        options['page'] += 1
        
        time.sleep(0.8)
        
    return grants

 
def convert_grant(grant):
    return {
        'id': grant['id'], # numeric
        'owner': grant['admin_address'],
        'payee': '',
        'metaPtr': '',
        'metadata': {
            'name': grant['title'],
            'description': grant['description'],
            'image': grant['logo_url'],
            'properties': {
                'projectWebsite': grant['reference_url'],
                'projectGithub': grant['github_project_url'],
                'projectMembers': [member['fields']['handle'] for member in grant['team_members']],
                'bannerImage': '',
                'twitterHandle': grant['twitter_handle_1'],
                'keywords': [category['fields']['name'] for category in grant['grant_tags']],
                'endDate': ''
            }
        }   
    }

    
import copy

grants = get_grants(copy.deepcopy(options), 10)

cleaned_grants = [ convert_grant(grant) for grant in grants]

mongoengine.connect('grants')

for grant in cleaned_grants:
    grant = models.Grant(grant_id=grant['id'], owner=grant['owner'], payee=grant['payee'], metaPtr=grant['metaPtr'],
                 metadata=models.Metadata(name=grant['metadata']['name'], description=grant['metadata']['description'], 
                                   image=grant['metadata']['image'], 
                                   properties=models.Project(
                                            projectGithub=grant['metadata']['properties']['projectGithub'],
                                            projectMembers=grant['metadata']['properties']['projectMembers'],
                                            bannerImage=grant['metadata']['properties']['bannerImage'],
                                            twitterHandle=grant['metadata']['properties']['twitterHandle'],
                                            keywords=grant['metadata']['properties']['keywords'],
                                            )
                                  )
                )
    grant.save()
    
    
print(f'Grants saved: {models.Grant.objects.count()}')
