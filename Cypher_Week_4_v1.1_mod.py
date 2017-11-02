from pandas import DataFrame
from py2neo import Graph,Node,Relationship
import numpy as np
import json
import os
import time #measure time-efficient


graph = Graph(
    "http://localhost:7474", 
    username="neo4j", 
    password="doramon401"
)

#Be careful!!!
#delect all nodes and relationships
graph.delete_all()

#It can only load one file and save the value in the file one by one
#"fn" is the file path
def load_one_file(fn):
    #load the json file
    #f = file(fn) window
    f = open(fn)
    text = json.load(f)

     #save the doc. node
    document = save_doc(text)
    
    #save sensitive data( 0 == Not Sensitive ; 1 == Sensitive)
    #path=testCollection.gold.json/
    save_sensitive(document,text)
    
    #save the author node relationship
    save_author(document,text)
    
    #save the classification person node relationship
    save_cls_guy(document,text)
        
    #save the person nodes and relationships
    #person who is mentioned and the author will be saved in the same label "PERSON"
    save_mts_guy(document,text)
        
    #save the organization mentioned in doc and relationship
    save_org(document,text)
    
    #save the location nodes and relationships
    save_loc(document,text)
    
    #save the origin organization and relationship
    save_ori(document,text)
    
    #save tag nodes and relationships
    save_tag(document,text)
    
    #save classification and relationships
    save_cls(document,text)
    
    #save contexts and relatiohships
    save_context(document,text)
    
    #save money and relationship
    save_money(document,text)
    
    #save percentages and relationships
    save_percent(document,text)
    
    #save dates and relationships
    save_date(document,text)
    
    #save times and relationsips
    save_time(document,text)

#save the doc. node
#document = save_doc()
def save_doc(text):
    document = Node("DOC",title = text['ARTICLE'][1], ID = text['ARTICLE'][0], 
                    created_date = text['CREATED_DATE'], released_date = text['RELEASED_DATE'], 
                    subject = text['SUBJECT'], words = text['WORDS'], paragraphs = text['PARAGRAPH'],
                    ref = text['REF'], doctype = text['TYPE'])
    graph.merge(document)
    return document

#save the author node relationship
def save_author(document,text):
    for i in np.arange(len(text['AUTHOR'])):
        author = Node("PERSON",name = text['AUTHOR'])
        graph.merge(author, "PERSON", "name")
        graph.merge(Relationship(author,'WRITES',document))
        
#save the classification person node relationship
def save_cls_guy(document,text):
    for i in np.arange(len(text['CLASSIFIED_PERSON'])):
        cls_guy = Node("PERSON",name = text['CLASSIFIED_PERSON'][0], position = text['CLASSIFIED_POSITION'][0])
        graph.merge(cls_guy, "PERSON", "name")
        graph.merge(Relationship(document,('IS CLASSIFIED BY', {"classifiedReason": text["CLASSIFIED_REASON"][0]}),cls_guy))
        
#save the person nodes and relationships
#person who is mentioned and the author will be saved in the same label "PERSON"
def save_mts_guy(document,text):
    for i in np.arange(len(text['PERSON'])):
        mts_guy = Node("PERSON",name = text['PERSON'][i])
        graph.merge(mts_guy, "PERSON", "name")
        graph.merge(Relationship(document,'MENTIONS',mts_guy))
        
#save the organization mentioned in doc and relationship
def save_org(document,text):
    for i in np.arange(len(text['ORGANIZATION'])):
        organization = Node("ORGANIZATION",name = text['ORGANIZATION'][i])
        graph.merge(organization, "ORGANIZATION","name")
        graph.merge(Relationship(document,'MENTIONS',organization))
        
#save the location nodes and relationships
def save_loc(document,text):
    for i in np.arange(len(text['LOCATION'])):
        location = Node("LOCATION",name = text['LOCATION'][i])
        graph.merge(location, "LOCATION","name")
        graph.merge(Relationship(document,'MENTIONS',location))
        
#save the origin organization and relationship
def save_ori(document,text):
    origin = Node("ORGANIZATION",name = text['ORIGIN']
                  #, longtitude = text['LONGITUDE'], latitude = text['LATITUDE']
                 )
    graph.merge(origin)
    graph.merge(Relationship(document,'IS ISSUED BY',origin))
    
    oricity = Node("LOCATION",name = text["ORIGIN_CITY"][0]
                   #, longtitude = text['LONGITUDE'], latitude = text['LATITUDE']
                  )
    graph.merge(oricity, "LOCATION","name")
    graph.merge(Relationship(origin,'IS LOCATED IN',oricity))
    
    oricty = Node("LOCATION",name = text['COUNTRY']
                  #, longtitude = text['LONGITUDE'], latitude = text['LATITUDE']
                 )
    graph.merge(oricty, "LOCATION","name")
    graph.merge(Relationship(oricity,'IS LOCATED IN',oricty))
    graph.merge(Relationship(document,'IS ISSUED IN',oricty))
    
#save tag nodes and relationships
def save_tag(document,text):
    for i in np.arange(len(text['TAGS'])):
        tag = Node("TAG",name = text['TAGS'][i])
        graph.merge(tag, "TAG","name")
        graph.merge(Relationship(document,'TAGS',tag))
        
#save classification and relationships
def save_cls(document,text):
    cls = Node("CLASSIFICATION",name = text['CLASSIFICATION'])
    graph.merge(cls,"CLASSIFICATION","name")
    graph.merge(Relationship(document,'IS CLASSIFIED AS',cls))
    
#save contexts and relatiohships
def save_context(document,text):
    for i in np.arange(len(text['CONTEXT'])):
        context = Node("CONTEXT",name = text['CONTEXT'][i])
        graph.merge(context, "CONTEXT","name")
        graph.merge(Relationship(document,'MENTIONS MANY TIMES',context))
        
#save money and relationships
def save_money(document,text):
    for i in np.arange(len(text['MONEY'])):
        money = Node("MONEY",name = text['MONEY'][i])
        graph.merge(money, "MONEY","name")
        graph.merge(Relationship(document,'MENTIONS',money))
        
#save percentages and relationships
def save_percent(document,text):
    for i in np.arange(len(text['PERCENT'])):
        percent = Node("PERCENTAGE",name = text['PERCENT'][i])
        graph.merge(percent, "PERCENTAGE","name")
        graph.merge(Relationship(document,'MENTIONS',percent))
        
#save dates and relationships
def save_date(document,text):
    for i in np.arange(len(text['DATE'])):
        date = Node("DATE",name = text['DATE'][i])
        graph.merge(date, "DATE","name")
        graph.merge(Relationship(document,'MENTIONS',date))
        
#save times and relationsips
def save_time(document,text):
    for i in np.arange(len(text['TIME'])):
        time = Node("TIME",name = text['TIME'][i])
        graph.merge(time,"TIME","name")
        graph.merge(Relationship(document,'MENTIONS',time))
        
# Team version
# ===================
#save sensitive data( 0 == Not Sensitive ; 1 == Sensitive)
#path=testCollection.gold.json/
# def save_sensitive(document,text):
#     #fileList = getFileList("testCollection.gold.json/")
    
#     a = os.listdir('testCollection.gold.json')
    
#     #for i in np.arange(len(fileList)):
#     #for i in np.arange(len(a)):
#     for each in a:
#         if each == text['ARTICLE'][0]+".json":
#                 #f = file("testCollection.gold.json/"+fileList[i])
#                 f = open("testCollection.gold.json/"+each)
#                 t = json.load(f)
#                 if t["SENSITIVE_DATA"] == "0":
#                     sensitive = Node("SENSITIVITY",value = "not sensitive")
#                 else:
#                     sensitive = Node("SENSITIVITY",value = "sensitive")
#                 graph.merge(sensitive)
#                 graph.merge(Relationship(document,'IS REVIEWED AS',sensitive))

#save sensitive data( 0 == Not Sensitive ; 1 == Sensitive)
def save_sensitive(document,text):
    if text["SENSITIVITY"][0] == "0":
        sensitive = Node("SENSITIVITY",value = "not sensitive")
    else:
        sensitive = Node("SENSITIVITY",value = "sensitive")
    graph.merge(sensitive,"SENSITIVITY","value")
    graph.merge(Relationship(document,'IS REVIEWED AS',sensitive))

#To get the list of file name of json files in a folder
def getFileList(p):
    start_total_time=time.time()
    p = str( p )
    if p == "":
        return []
    a = os.listdir( p )
    for each in a:
        if each[-5:] == '.json':
            load_one_file(p+'/'+each)
            #print(p+'/'+each)
            print('imported', each)
    end_total_time=str(time.time()-start_total_time)
    print("\nTotal time is "+end_total_time+" sec. to finish the job")
    return "import completed !"

def load_files(folderPath):
    fileList = getFileList(folderPath)
    for v in np.arange(len(fileList)):
    #for v in np.arange(2):
        load_one_file(folderPath+fileList[v])

#Be careful!!!
#delect all nodes and relationships
#graph.delete_all()
load_files('/root/ArticleQ/json')

# query = """
#         MATCH (doc:DOC)-[r:`IS ISSUED BY`]->(:ORGANIZATION { name:"Embassy Madrid" }) 
#         WHERE "2009-01-20 00:00" < doc.created_date < "2009-01-29 00:00"
#         RETURN DISTINCT doc.title;
#         """

# query2 = "MATCH (p:PERSON)-[r:WRITES]->(doc) RETURN p.name,count(doc);"
# count = graph.run(query2)
# for i in count:
#     print(i)

# In[ ]:



