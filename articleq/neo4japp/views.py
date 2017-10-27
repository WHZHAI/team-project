# Create your views here.
from __future__ import absolute_import

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import matplotlib as plt
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pylab import *
import io
from io import *
from .tools import FeatureExtraction, GraphDBController, QueryProcessor
import codecs

def index(request):
    return render(request, 'neo4japp/index.html')

def query(request):
    return render(request, 'neo4japp/query.html')

def upload(request):
    return render(request, 'neo4japp/upload.html')

def upload_done(request):
    if request.method == "POST":
        files = request.FILES.getlist('myfiles')
        list_files = [] # hold the data that show in upload_done page
        for a_file in files:
            data = codecs.decode(a_file.read(), 'utf-8') # Decode the json data from utf-8 to normal html string
            json = FeatureExtraction.extract_feature(a_file.name, data)
            GraphDBController.save_to_db(json)
            list_files.append({'file_name': a_file.name, 'json': json})
    return render(request, 'neo4japp/upload_done.html', {'list_files': list_files})

def result(request):
    query = request.POST['query']

    """
    Send the 'raw' query to QueryProcessor.
    Get the processed data back, where the processed data have 2 properties,
        - process_data[0] = type of the visualization (eg. text, list, matplotlib graph)  
        - process_data[1] = data returned from the database, the format is depended on types of query
    Each type of data will be handled differently as below.
    """
    process_data = QueryProcessor.process_query(query)

    if process_data[0] == "list":
        return render(request, 'neo4japp/result.html', {'query': query, 'type':process_data[0], 'data': process_data[1]})

    elif process_data[0] == "matplotlib":
        # Save image to static/image/result.png
        static = 'static'
        image_dir = 'image'
        file_name = 'result.png'
        create_dir = static + '/' + image_dir
        if not os.path.exists(create_dir): # Create the dir if there is no dir
            os.makedirs(create_dir)
        file_path = create_dir + '/' + file_name
        plt.savefig(file_path, transparent=True)
        file_path = image_dir + '/' + file_name # Return the static picture path back to result page
        return render(request, 'neo4japp/result.html', {'query': query, 'type': "image", 'data': file_path})
    
    else:
        return render(request, 'neo4japp/result.html', {'query': query, 'data': docs})
