# Create your views here.
from __future__ import absolute_import

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Movie, Person
from neo4jtut import db
import matplotlib as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pylab import *
import io
from io import *


class MovieDetailView(DetailView):

    model = Movie


class MovieListView(ListView):

    model = Movie


class PersonDetailView(DetailView):

    model = Person


class PersonListView(ListView):

    model = Person


def index(request):
    return render(request, 'neo4japp/index.html')

def query(request):
    return render(request, 'neo4japp/query.html')

def result(request):
    query = request.POST['query']
    print(query)
    # process query: display text or graph
    # return [type, data] where type = 0 is text and type = 1 is graph
    process_data = process_query(query)
    if process_data[0] == "list":
        print("before render: ", process_data[1])
        return render(request, 'neo4japp/result.html', {'query': query, 'type':process_data[0], 'data': process_data[1]})
    elif process_data[0] == "png":
        canvas = process_data[1]
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)
        # png_output = StringIO.StringIO()
        # canvas.print_png(png_output)
        # data = png_output.getvalue().encode('base64')
        # html = '<img src="data:image/png;base64,{}">'.format(urllib.quote(data.rstrip('\n')))
        return response
        # print(canvas)
        # return render(request, 'neo4japp/result.html', {'query': query, 'type': "canvas", 'data': html}, content_type='text/html')
    else:
        return render(request, 'neo4japp/result.html', {'query': query, 'data': docs})

def process_query(query):
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

        data = np.array(authors)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        print("author:\n", data[:, 0], "\ntotal:\n", data[:,1].astype(int))
        ax.bar(np.arange(len(data[:, 0])), data[:, 1].astype(int))
        ax.set_xlabel('Author')
        ax.set_xticks(np.arange(len(data[:, 0])))
        ax.set_xticklabels(data[:, 0])
        ax.set_ylabel('Total Articles')
        fig.autofmt_xdate(bottom=0.2, rotation=70, ha='right')
        canvas = FigureCanvas(fig)
        # response = HttpResponse(content_type='image/png')
        # canvas.print_png(response)
        return ["png", canvas]
    # else:
