from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import models
import random
import utils


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongo',
    'db': 'grants'
}

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

db = MongoEngine(app)



@app.route('/harvest/<grant_id>', methods=['GET'])
def harvest_curated_grants(grant_id):
    grant = models.Grant.objects(pk=grant_id).first()
    pipeline = [
    	{ '$match': {'grant': grant.pk } },
    	{'$group': {'_id': {'$concat': ['$requirement', '_','$status']}, 'total': {'$sum': {'$sum': [1, '$score']}}}}
    ]
    requirements = {}
    mods = []
    positive = 0
    negative = 0

    for doc in models.Vote.objects().aggregate(pipeline):
       print(doc) 
       requirements[doc['_id']] = doc['total']
    
    print(requirements)
    for r in ['correct_category',
   	'category_is_allowed_on_the_platform',
   	'having_a_reasonable_description',
   	'not_being_offensive',
   	'coming_from_a_legitimate_project']:
        if requirements.get(f'{r}_yes', 0) < requirements.get(f'{r}_no', 0):
            mods.append(r)
            negative += 100/5
            print(negative)
            print(positive)
        elif requirements.get(f'{r}_yes', 0) > requirements.get(f'{r}_no', 0):
            positive += 100/5
            print(negative)
            print(positive)
        
    result = 'fail' if negative > positive else 'mods' if len(mods) else 'pending' if positive == 0 and negative == 0 else 'pass'
    confidence = negative if negative > positive else positive
    mod_required = bool(len(mods))
    return jsonify({
     "id": grant.pk,
     "result": result,
     "confidence": confidence,
     "mod_required": mod_required,
     "data": {
         "mods": mods
     }
   })


@app.route('/grant', methods=['GET', 'POST'])
def manage_grants():
    address = request.args.get('address')
    
    if request.method == 'POST' and address:
        payload = request.json
        weight = utils.calculate_gtc_reputation(address)/len(payload['answers']) or 0.001
        grant = models.Grant.objects(pk=payload['grant']).first()
        
        for answer in payload['answers']:
          vote = models.Vote(address=address, grant=grant.pk)
          vote.status=answer['answer']
          vote.requirement=answer['id']
          vote.score=weight
          
          print(vote._data)
          vote.save()

        return jsonify({
          'status': 'ok'
        })

    total_grants = models.Grant.objects.count()
    # grant = models.Grant.objects[random.randint(0, total_grants)]
    
    voted_grants = [ x.grant_id for x in models.Vote.objects(address=address).only('grant').distinct(field="grant") ]

    pipeline = [
        { '$match': {'_id': {'$nin': voted_grants}} },
        {
            '$lookup': {
                'from': 'vote',
                'localField': '_id',
                'foreignField': 'grant',
                'as': 'votes'
        }},
        { '$addFields': {'score': {'$size': "$votes"} } },
        { '$sort': { 'score': 1} },
        { '$sample': { 'size': 3 } }
        # { '$limit': 1 }
    ]

    for grant in models.Grant.objects().aggregate(pipeline):
        return jsonify(grant)

    # return jsonify(grant._data)

@app.route('/harvest')
def harvest_curations():
    pipeline = [
    { 
        '$lookup': {
            'from': 'vote',
            'localField': '_id',
            'foreignField': 'grant',
            'as': 'votes'
    }},
    { '$project': {
        'yes': { 
          '$filter': 
          { 
            'input': "$votes", 
            'as': "vote", 
            'cond': { '$eq': [ "$$vote.status", 'yes' ] } 
          } 
        },
        'no': { 
          '$filter': 
          { 
            'input': "$votes", 
            'as': "vote", 
            'cond': { '$eq': [ "$$vote.status", 'no' ] } 
          } 
        },
        'unsure': { 
          '$filter': 
          { 
            'input': "$votes", 
            'as': "vote", 
            'cond': { '$eq': [ "$$vote.status", 'unsure' ] } 
          } 
        },
        'votes': 1
      }
    },
    { '$addFields': {'yes_total': {'$size': "$yes"}, 'no_total': {'$size': "$no"}, 'unsure_total': {'$size': "$unsure"}, 'total': {'$size': "$votes"},  } },
    { '$project': {
        'yes_total': 1, 
        'no_total': 1, 
        'unsure_total': 1, 
        'total': 1, 
        'status': {'$cond': [{'$eq': ['$total', 0]}, 
                             'pending', 
                             {'$cond': [{'gte': ['$yes_total', '$no_total']}, 'pass', 'fail']}]},
        'score': {'$cond': [{'$eq': ['$total', 0]}, 
                            0, 
                            {'$cond': [
                                {'gte': ['$yes_total', '$no_total']}, 
                                {'$divide': ['$yes_total', '$total']}, 
                                {'$divide': ['$no_total', '$total']}]}]},
      },
    },
    { '$sort': {'total': -1}}
    ]

    

    return jsonify({ 'grants': [{ grant['_id']: grant['status']  } for grant in models.Grant.objects().aggregate(pipeline)]})

if __name__ == '__main__':
    app.run()
