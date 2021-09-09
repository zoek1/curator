from mongoengine import *
import datetime 
from enum import Enum

class Project(EmbeddedDocument):
    projectGithub = StringField()
    projectMembers = ListField(StringField(max_length=30))
    bannerImage = StringField()
    twitterHandle = StringField(max_length=30)
    keywords = ListField(StringField(max_length=30))
    endDate = DateTimeField(null=True)


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


class Status(Enum):
    YES = 'yes'
    UNSURE = 'unsure'
    NO = 'no'


class Requirement(Enum):
    CORRECT_CATEGORY = 'correct_category'
    CATEGORY_ALLOWED = 'category_is_allowed_on_the_platform' 
    REASONABLE_DESCRIPTION = 'having_a_reasonable_description'
    NO_OFFENSIVE = 'not_being_offensive'
    LEGITIMATE_PROJECT = 'coming_from_a_legitimate_project'
    

class Vote(Document):
    address = StringField(required=True, max_length=100)
    grant =  ReferenceField(Grant)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    requirements = EmbeddedDocumentField(Metadata)
    status = EnumField(Status, default=Status.UNSURE)
    requirement = EnumField(Requirement)
    score = FloatField()

    meta = {
        'indexes': [
            {'fields': ('address', 'grant', 'requirement'), 'unique': True}
        ]
    }
