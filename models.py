from mongoengine import *
import datetime 


class Project(EmbeddedDocument):
    projectGithub = StringField()
    projectMembers = ListField(StringField(max_length=30))
    bannerImage = StringField()
    twitterHandle = StringField(max_length=30)
    keywords = ListField(StringField(max_length=30))
    endDate = DateTimeField()


class Metadata(EmbeddedDocument):
    name = StringField(required=True)
    description = StringField(required=True)
    image = StringField(required=True)
    properties = EmbeddedDocumentField(Project) 


class Grant(Document):
    grant_id = IntField(required=True, primary_key=True)
    owner = StringField(required=True, max_length=100)
    payee = StringField(max_length=100)
    metaPtr = StringField()
    metadata = EmbeddedDocumentField(Metadata)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)


class Vote(Document):
    address = StringField(required=True, max_length=100)
    grant =  ReferenceField(Grant)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)


