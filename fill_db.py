import os

from peewee import *
from playhouse.db_url import connect

# Connect to the database URL defined in the environment, falling
# back to a local Sqlite database if no database URL is specified.
db = connect(os.environ.get('DATABASE_URL') or 'sqlite:///default.db')

# db_url = os.environ.get('DATABASE_URL').split('//')[1]
# user, rest = db_url.split(':')
# password, rest = rest.split('@')
# db_name = rest.split('/')[1]
# db = MySQLDatabase(db_name, user=user, password=password, charset='utf8mb4')

# https://docs.google.com/spreadsheets/d/1F-hADJqjvD2_n-g9rLd8AGbmeKUnMb9h49fmUxx0rYo/edit#gid=276135992

class BaseModel(Model):
    class Meta:
        database = db

class Category(BaseModel):
    type = CharField(unique=True)
    class Meta:
        db_table = 'cat_type'

class Source(BaseModel):
    ForeignKeyField(Category, related_name='type_id', null=True)
    nr = IntegerField()
    year = IntegerField()
    week = IntegerField()
    date = DateTimeField()
    url = CharField()
    class Meta:
        db_table = 'db_source'

class Item(BaseModel):
    source = ForeignKeyField(Source, null=True)
    item_number = IntegerField()
    item_description = CharField()
    subject = CharField(1000)
    unit = CharField()
    item_url = CharField()
    class Meta:
        db_table = 'db_item'

class Act(BaseModel):
    item = ForeignKeyField(Item, null=True)
    act_number = IntegerField(null=True)
    type = CharField()
    subject = CharField(1000)
    content_url = CharField(unique = True)
    content = TextField()
    
    class Meta:
        db_table = 'db_act'

try:
    db.create_tables([Category, Source, Item, Act])
except ProgrammingError:
    db.rollback()

# test = Act(subject='bla', content='blabla', content_url = 'http://web.zagreb.hr/sjednice/2013/Sjednice_2013.nsf/DRJ?OpenAgent&31.%20listopada%202016.%20-%204.studenog%202016')
# test.save()

# test2 = Act(subject='bla2', content='blabla2', content_url = 'http://web.zagreb.hr/sjednice/2013/Sjednice_2013.nsf/DRJ?OpenAgent&31.%20listopada%202016.%20-%204.studenog%202016') 
# test2.save()


# for cat in Category.select():
#     print(cat.type, cat.created_ts)

# for act in Act.select():
#     print(act.subject, act.content, act.content_url)

for type_description in ['akti_gradonacelnika', 'dnevni_red_skupstine', 'pitanja_odgovori', 'dnevni_red_radna_tijela']:
    try:
        new_type = Category(type=type_description)
        new_type.save()
    except IntegrityError:
        db.rollback()

import pickle

with open('./skupstina2.pkl', 'rb') as f:
    subjects = pickle.load(f)
    for subject in subjects:
        for act in subject['details']['acts']:
            # print(len(act['title']), len(act['text']), len(act['url']))
            try:
                content = act['text']
                # content = content.replace('\xB2', '2')
                # print(content)
                new_act = Act(subject=act['title'], content=content, content_url=act['url'], type='')
                new_act.save()
                print('wrote')
            except IntegrityError as e:
                print(e)
                db.rollback()
                continue
            
            
            
