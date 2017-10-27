from py2neo import Graph,Node,Relationship
import numpy as np
import json
import os

graph = Graph(
    "http://localhost:7474", 
    username="neo4j", 
    password="doramon401" # Change this to your db password
)

def load_one_file(json):
    """
    Load the input json object into graph database

    Return: nothing

    Key-arguments: 
    json -- json object containing all extracted features
    """  
    
    #save the article/doc. node
    article = Node('ARTICLE',name = json['ARTICLE'][1], ID = json['ARTICLE'][0])
    #save the author node
    if json['AUTHOR'] != []:
        author = Node("PERSON",name = json['AUTHOR'])
        #graph.merge(): carried out by comparing that node with a potential remote equivalent 
        #on the basis of a label and property value. If no remote match is found, a new node is created. 
        graph.merge(article|author)
        graph.merge(Relationship(author,'WRITES',article))
    #save the location nodes
    for i in np.arange(len(json['LOCATION'])):
        location = Node("LOCATION",name = json['LOCATION'][i])
        graph.merge(location)
        graph.merge(Relationship(article,'MENTIONS',location))
    #save the organization nodes
    for j in np.arange(len(json['ORGANIZATION'])):
        organization = Node("ORGANIZATION",name = json['ORGANIZATION'][j])
        graph.merge(organization)
        graph.merge(Relationship(article,'MENTIONS',organization))
    #save the person nodes
    #person who is mentioned and the author will be saved in the same label "PERSON"
    #because author may be mentioned in other doc.
    for k in np.arange(len(json['PERSON'])):
        person = Node("PERSON",name = json['PERSON'][k])
        graph.merge(person)
        graph.merge(Relationship(article,'MENTIONS',person))

def getFileList(p):
    p = str( p )
    if p == "":
        return []
#     For windows
#     p = p.replace( "/","\\")
#     if p[ -1] != "\\":
#         p = p+"\\"
    a = os.listdir( p )
    b = [ x   for x in a if os.path.isfile( p + x ) ]
    return b

def load_files(folderPath):
    fileList = getFileList(folderPath)
    for v in np.arange(len(fileList)):
    #for v in np.arange(9):
        load_one_file(folderPath+fileList[v])

# Implemented by PP: as an interface for views.py to call
def save_to_db(json):
    load_one_file(json)