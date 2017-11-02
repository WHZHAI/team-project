from __future__ import print_function, division
from articleq import db
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import json

from pandas import DataFrame
from py2neo import Graph,Node,Relationship
import os
import time #measure time-efficient
import py2neo
from collections import Counter

graph = Graph(
    "http://localhost:7474", 
    username="neo4j", 
    password="doramon401"
)

def create_graph_title(states):
    # concate the states
    title = ""
    for s in states:
        title += s["phrase"] + " "
    return title

def get_y_label(states):
    return states[1]["phrase"] + " " + states[2]["phrase"]

def process_query(query, json_text):
    """
    Process raw query by processing them according to defined query pattern
    (Current version just used fixed query)
    
    Return: depending on the type of visualization, but have this format in common
        element[0] -- type of result
        elemetn[1] -- data 

    Keyword arguments:
    query -- raw query from user, may or may not be according to the pattern
    """

    # show the number of document written by each person
    # show the number of document mentions each person

    # Processs dynamic query 
    if (json_text != ""):
        states = json.loads(json_text)
        # type: bar graph (the number of)
        if states[1]["phrase"] == "the number of":
            label_1 = states[2]["db_name"]
            relation = states[3]["db_name"]
            label_2 = states[5]["db_name"]
            print("label_1: ", label_1, "\nrelation: ", relation, "\nlabel_2: ", label_2)
            title = create_graph_title(states[1:])
            print("graph_title: ", title)
        search_result = dynamic_query_type_1(label_1, relation, label_2)

        # render graph
        fig = plt.figure(1, figsize = (10,6))
        ax = fig.add_subplot(1,1,1)
        ax.cla()
        data = np.array(search_result)
        if len(data) > 25:
            data = data[0:25,:]
        ax.bar(np.arange(len(data[:, 0])), data[:, 1].astype(int))
        ax.set_title(title)
        ax.set_xlabel(label_2)
        ax.set_xticks(np.arange(len(data[:, 0])))
        ax.set_xticklabels(data[:, 0])
        ax.set_ylabel(get_y_label(states))
        fig.autofmt_xdate(bottom=0.2, rotation=70, ha='right')
        fig.tight_layout()
        return ["matplotlib", plt]
    # Process fix query
    else:
        if query == "list all article names":
            articles = []
            for a in db.get_articles():
                articles.append(a['name'])
            return ["list", articles]
        elif query == "number of articles written by each author":
            # query data from db
            authors = []
            for a in db.get_article_num_by_author():
                a_t = [a['name'], a['total_article']]
                authors.append(a_t)
            # create graph from result
            data = np.array(authors)
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            ax.bar(np.arange(len(data[:, 0])), data[:, 1].astype(int))
            ax.set_xlabel('Author')
            ax.set_xticks(np.arange(len(data[:, 0])))
            ax.set_xticklabels(data[:, 0])
            ax.set_ylabel('Total Articles')
            fig.autofmt_xdate(bottom=0.2, rotation=70, ha='right')
            return ["matplotlib", plt]
        else:
            #  incorrect syntax
            return ["incorrect syntax", query]


#specify organization x>when
def match_issued_by(organization):
    q = '''
    MATCH (doc:DOC)-[r:`IS ISSUED BY`]->(org:ORGANIZATION) 
    WHERE org.name =~ '.*''' + organization + '.*' + "'" 
    return q

#specify when x>
def match_created_date(start_date, end_date):
    q = '''
    MATCH (doc:DOC)
    WHERE "''' + start_date + '''" < doc.created_date < "''' + end_date + '"'
    return q

def match_released_date(start_date, end_date):
    q = '''
    MATCH (doc:DOC)
    WHERE "''' + start_date + '''" < doc.released_date < "''' + end_date + '"'
    return q

#specify sensitive data
def match_sensitive_date():
    q = '''
    MATCH(doc:DOC)-[i:`IS REVIEWED AS`]->(sen:SENSITIVITY { value: "sensitive" })'''
    return q

#specify non-sensitive data
def match_non_sensitive_date():
    q = '''
    MATCH(doc:DOC)-[i:`IS REVIEWED AS`]->(sen:SENSITIVITY { value: "not sensitive" })'''
    return q
#show all organization
def match_organization():
    q = '''
    MATCH (doc:DOC)-[r:`IS ISSUED BY`]->(org:ORGANIZATION)'''
    return q
#show all authors
def match_author():
    q = '''
    MATCH (p:PERSON)-[r:WRITES]->(doc)'''
    return q


#show all authors
def match_person(relation):
    if relation == "write":
        q = '''
        MATCH (p:PERSON)-[r:WRITES]->(doc)'''
    elif relation == "":
        q = '''
        MATCH (p:PERSON)-[r:WRITES]->(doc)'''    
    return q

def dynamic_q_backward(label_1, relation, label_2):
    q = 'MATCH (' + label_2 + ':' + label_2 + ')-[:`' + relation + '`]->(' + label_1 + ':' + label_1 + ') '
    if label_2 == "DOC":
        q += 'RETURN ' + label_2 + '.ID as x, count(' + label_1 + ') as y '
    else:
        q += 'RETURN ' + label_2 + '.name as x, count(' + label_1 + ') as y '
    q += 'ORDER BY y DESC '
    return q

def dynamic_q_forward(label_1, relation, label_2):
    q = 'MATCH (' + label_1 + ':' + label_1 + ')-[:`' + relation + '`]->(' + label_2 + ':' + label_2 + ') '
    if label_2 == "DOC":
        q += 'RETURN ' + label_2 + '.ID as x, count(' + label_1 + ') as y '
    else:
        q += 'RETURN ' + label_2 + '.name as x, count(' + label_1 + ') as y '
    q += 'ORDER BY y DESC '
    return q

def return_q(return_array):
    return_q = '''
    RETURN '''   
    
    for i in range(len(return_array)):
        if i != len(return_array)-1:
            return_q = return_q + return_array[i] + ', '
        else:
            return_q = return_q + return_array[i]
    return return_q

def yield_x(q):
    result = graph.run(q)
    for record in result:
        yield {'x': record['x']}

def yield_x_y(q):
    result = graph.run(q)
    for record in result:
        yield {'x': record['x'], 'y': record['y']}

def yield_x_y_z(q):
    result = graph.run(q)
    for record in result:
        yield {'x': record['x'], 'y': record['y'], 'z': record['z']}

#Dynamic Query Type 1
def dynamic_query_type_1(label_1, relation, label_2, start_date = "", end_date = ""):
    q = dynamic_q_forward(label_1, relation, label_2)  
    search_result = []
    print("forward: ", q)
    for each in yield_x_y(q):
        each_record = [each['x'], each['y']]
        search_result.append(each_record)
    
    if len(search_result) == 0:
        q = dynamic_q_backward(label_1, relation, label_2)  
        for each in yield_x_y(q):
            each_record = [each['x'], each['y']]
            search_result.append(each_record)
    print("backward: ", q)
    return search_result