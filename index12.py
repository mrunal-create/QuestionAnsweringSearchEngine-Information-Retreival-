#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
  
# Path of the pdf 
PDF_file = 'D:\lnt\IRC.pdf'


 
''' 
Part #1 : Converting PDF to images 
I converted the pdf to jpg images by using converter online.Then saved the images in a directory in the computer.
Only the relevant pages were kept. Page 9 to page 18 were relevant pages.These 10 pages were named as page_0,page_1...page_10
for Morth pdf relevant pages were page 19 to page 864. 
'''
  
  

''' 
Part #2 - Recognizing text from the images using OCR 
For every page text is extracted and stored in a text file.
'''
pytesseract.pytesseract.tesseract_cmd = 'C:/Users/admin/AppData/Local/Tesseract-OCR/tesseract.exe'
#image_counter=21
# Variable to get count of total number of pages 
#filelimit = image_counter-1
for i in range(9,19):             # loop runs from 9 to 19.For page 9 to page 18 which are 10 relevant pages.
    outfile = "D:/lnt/Text/IRC/out"+str(i)+".txt"
    f = open(outfile, "a") 
    filename = "page_"+str(i)+".jpg"
    text = str(((pytesseract.image_to_string(Image.open(filename))))) 
  
    # The recognized text is stored in variable text 
    # Any string processing may be applied on text 
    # Here, basic formatting has been done: 
    # In many PDFs, at line ending, if a word can't 
    # be written fully, a 'hyphen' is added. 
    # The rest of the word is written in the next line 
    # Eg: This is a sample text this word here GeeksF- 
    # orGeeks is half on first line, remaining on next. 
    # To remove this, we replace every '-\n' to ''. 
    text = text.replace('-\n', '')     
  
    # Finally, write the processed text to the file. 
    f.write(text) 
f.close()


# In[18]:


import json
import csv
from time import sleep
from datetime import datetime

# use the elasticsearch client's helpers class for _bulk API
from elasticsearch import Elasticsearch, helpers
es= Elasticsearch("localhost:9200")

#es.indices.delete(index='some34')
body1={                                                                     #specify the mappings for elastic search

  "settings": {
    "analysis": {
      "filter": {
       
         "english_stemmere": {    
          "type":       "stemmer",
          "language":   "english"
        },

        "my_stop": {
                    "type":       "stop",
                    "stopwords":  "_english_"
                }
         
        

         
        },
        
      "analyzer": {
        "mycustomized_lowercase_stemmed": {
          "tokenizer": "standard",
          "filter": ["lowercase","my_stop","english_stemmere"
            
            ]
          
        },
            "autocomplete_search": {
          "tokenizer": "standard",
                "filter":["lowercase","my_stop","english_stemmere"]
        
        }
      }

      }},







 'mappings':
        {
           
            "numeric_detection": "true",
             "date_detection": "true",

            "dynamic_templates": [
      {
        "named_analyzers": {  #for automatically picking up analyzer for any field with text
          "match_mapping_type": "string",
          "match": "*",
          "mapping": {
            "type": "text",
            "analyzer": "mycustomized_lowercase_stemmed",
            "search_analyzer": "autocomplete_search"
          }
        }
      }],
          
'properties': {

    

     "text" : {
          "type" : "text",
          "analyzer": "mycustomized_lowercase_stemmed" ,
             "search_analyzer": "autocomplete_search",
         #"search_analyzer": "standard",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
   
      
      
               
        
     }
        }
        } 





response=es.indices.create(index='some36',ignore=400,body=body1)
v=es.indices.exists(index="some36")
print(v)


# In[20]:


#bulk indexing.every page is individually indexed.
from elasticsearch import helpers  
 #The below is for IRC.
#For Morth you would have to change value of variable 'pages',for loop initial counter and filename in  _id.
#IRC indexing.  Same has to be performed for Morth indexing.
#filename="morth"
pages=10   # there are 10 relevant pages.  For Morth pdf pages =848
for i in range(1,pages+1):    #for morth pdf counter starts from 3
    with open("D:/lnt/IRCnew3/demofile"+str(i)+".txt", "r") as input:    #change path for morth text files accordingly
        input_ = input.read().split("\n\n")
        actions = [
  {
    "_index": "some36",
   
    "_id": "IRC"+"/"+str(i)+"/"+str(j),     #In "_id"  ,Specify filename as "Morth" for Morth indexing      #i specifies page no and j specifies paragraph number
    "_source": {
        "text":input_[j]
        }
  }
  for j in range(0, len(input_))
]
        response=helpers.bulk(es, actions)
        print ("helpers.bulk() RESPONSE:",response)
        print ("helpers.bulk() RESPONSE:", json.dumps(response, indent=4))    
        print("INDEXING COMPLETE")     


        

            
    


# In[21]:


from elasticsearch import Elasticsearch
es= Elasticsearch("localhost:9200")
print("SEARCHING:SEARCH RESULTS") 
rest=es.search(index="some36", body={"query": {"match": {'text':'Curing'}}})#search query
print(rest)


# In[ ]:




