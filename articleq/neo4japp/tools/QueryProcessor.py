from articleq import db
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def process_query(query):
    """
    Process raw query by processing them according to defined query pattern
    (Current version just used fixed query)
    
    Return: depending on the type of visualization, but have this format in common
        element[0] -- type of result
        elemetn[1] -- data 

    Keyword arguments:
    query -- raw query from user, may or may not be according to the pattern
    """
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
        return ["matplotlib"]
    # else: