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
    'db': 'grants'
}

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

db = MongoEngine(app)


@app.route('/grant', methods=['GET', 'POST'])
def manage_grants():
    address = request.args.get('address')
    
    if request.method == 'POST' and address:
        payload = request.json
        weight = utils.calculate_gtc_reputation(address)/len(payload['answers'])
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


if __name__ == '__main__':
    app.run()
