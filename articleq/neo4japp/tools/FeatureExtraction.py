import gzip #read file in gzip format
import time #measure time-efficient
import nltk #used for Tokenization
nltk.download('punkt')
import nltk.tag.stanford as st #use StanfordNERTagger to give a tag to each word
import re #Regular Expression
import inspect, os
import json 
import bs4 as bs #change html text to readable text
from itertools import groupby

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__)) # Use to refer the current project dir

LOCATION_ALL=[]
ORGANIZATION_ALL=[]

def extract_feature(file_name, html_data):
    """
    The function extracted all possible features from .html document and return json object back

    Return: json object that contains all extracted features

    Keyword arguments:
    file_name -- name of an html file
    html_data -- string containing html data
    """
    
    start_total_time = time.time()
    # covert raw html to readable text
    html_soup = bs.BeautifulSoup(html_data,features='lxml')
    readable_text = html_soup.get_text()
            
    # get Title and Author
    TITLE = str(html_soup.pre).split('\n')[0][5:]
    AUTHOR1 = str(html_soup.pre).split('\n')[-2][:].upper()
    AUTHOR2 = str(html_soup.pre).split('\n')[-1][:-6].upper()
    if AUTHOR2.isalpha()==True:
        if (AUTHOR1.isalpha()==False) or (AUTHOR1=='COMMENT'): AUTHOR=AUTHOR2
        else: AUTHOR=[AUTHOR1, AUTHOR2]
    else: AUTHOR=[]
            
    #Standord NER
    tagger=st.StanfordNERTagger(
        model_filename = PROJECT_PATH + '/stanford-ner-2017-06-09/classifiers/english.muc.7class.distsim.crf.ser.gz',
        path_to_jar = PROJECT_PATH +  '/stanford-ner-2017-06-09/stanford-ner.jar'
    )            
    start=time.time()
    tokens=nltk.word_tokenize(readable_text)
    tags=tagger.tag(tokens)
            
    # get file create time and document's publication date
    # CREATETIME=folder_dir[-7:]
    SUBJECT=get_subject(readable_text)    
    ARTICLE=[]
    ARTICLE.append(file_name)
    ARTICLE.append(TITLE)
    DOCTIME=[]
    PERSON=[]
    ORGANIZATION=[]
    LOCATION=[]
    MONEY=[]
    PERCENT=[]
    DATE=[]
    TIME=[]
            
    # Uniform format
    for tag, chunk in groupby(tags, lambda x:x[1]):
        feature=tag , " ".join(w for w, t in chunk)  
        if feature[0]=='PERSON':
            PERSON.append(feature[1])
        elif feature[0]=='ORGANIZATION':
            a=remove_org(feature[1])
            ORGANIZATION.append(a)
            ORGANIZATION_ALL.append(a)
        elif feature[0]=='LOCATION':   
            a=remove_loc(feature[1])
            LOCATION.append(a)
            LOCATION_ALL.append(a)
        elif feature[0]=='MONEY':   
            MONEY.append(feature[1]) 
        elif feature[0]=='PERCENT':   
            PERCENT.append(feature[1])                     
        elif feature[0]=='DATE':
            DATE.append(feature[1])
        elif feature[0]=='TIME':   
            TIME.append(feature[1])

    # Get publication time
    for D in DATE:
        if D in SUBJECT: DOCTIME.append(D)
    DOCTIME=list(set(DOCTIME)) 
            
    #Create Json export file
    export_json = {
                        'ARTICLE':'',
                        'AUTHOR':'',
                        'SUBJECT':'',
                        'CREATE TIME':'',
                        'PUBLICATION TIME':'',
                        'PERSON':'',
                        'ORGANIZATION':'',
                        'LOCATION':'',
                        'MONEY':'',
                        'PERCENT':'',
                        'DATE':'',
                        'TIME':''
    } 
    export_json["ARTICLE"]=ARTICLE
    export_json["AUTHOR"]=AUTHOR
    export_json["SUBJECT"]=SUBJECT
#     export_json["CREATE TIME"]=CREATETIME
    export_json["PUBLICATION TIME"]=DOCTIME
    export_json["PERSON"]=PERSON
    export_json["ORGANIZATION"]=ORGANIZATION
    export_json["LOCATION"]=LOCATION
    export_json["MONEY"]=MONEY
    export_json["PERCENT"]=PERCENT
    export_json["DATE"]=DATE
    export_json["TIME"]=TIME
      
    end_total_time = str(time.time() - start_total_time)
    print("\nTotal time is " + end_total_time + " sec. to finish the job")
    
    # Return JSON object
    return export_json

#get subject
def get_subject(readable_text):
    SUBJECT=''
    o=readable_text.split('\n')
    q=['REF', 'Ref', '¶1.', ' ¶1', 'ANT', 'BEI', 'BAM', 'BRA', 'DAK', 'SUM', 'Ope']
    for a in o:
        if a[:9]=="SUBJECT: ":
            i=o.index(a)
            SUBJECT=a[10:]
            for j in range(1,10):
                p=o[i+j][:3]
                if p in q[:]: break
                else: SUBJECT=SUBJECT+o[i+j]
    SUBJECT=SUBJECT.strip()
    return SUBJECT
    
#uniform organization format
def remove_org(org):
    if org.split(' ')[0]==("the" or "The"): org=org[4:]
    return org

#uniform location format
def remove_loc(loc):
    for i in loc.split(' '):
        if (i.isupper()==True) and (len(loc)>2): loc=loc.lower().title()
    a=loc.split(' ')[-1]
    if a=="Province": loc=loc[:-10]
    if a=="City": loc=loc[:-6]
    loc1=['U.S.', 'U.S', 'The U.S.', 'Untied States of America', 'US', 'United States of America', 
          'Unites States', 'America']
    loc2=['U.K.', 'U.K', 'UK', 'United Kindom']
    if loc in loc1: loc="United States"
    if loc in loc2: loc="United Kingdom"
    if loc=="A.U.": loc='African Union'
    return loc

#show duplicated and sorted feature values
def all_remove(feature):
    all_remove=sorted(sorted(set(feature),key=feature.index))
    return all_remove
    