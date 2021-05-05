# Information Retreival System

Installation
1] Elastic Search- conda install -c conda-forge elasticsearch 
2]Microsoft Visual Studio for Flask-
3]Tesseract OCR-conda install -c conda-forge tesseract


Code-> 


1] Index12.py contains pdf to text conversion along with bulk indexing it into elastic search.
2]Flask framework is used for backend and front end is made using HTML,CSS.
Flask folder contains module1.py which has the backend code.
There are two html files. one.html and two.html 

Data-> There is Pdf files IRC

Index12.py-
1]Individual pdf files are converted to jpg images using online converted.Then saved in the computer.
Relevant pages are selected named as page_0,page_1....
For IRC-> relevant pages are page_0 to page_10
For Morth relevant pages are page_3 to page_848
2] Tesseract OCR is used to extract text from images.For each image(page) ,one text file is generated. Corresponding text files are saved.

Text files are saved in folders IRCnew3 and Morthnew. They are named as demofile1,demofile2....

3]Mappings for elastic search are made .Index some36 is created for those mappings.For every text file paragraphs are extracted and indexed into elastic search as documents.  For IRC it is done for demofile1 to demofile10.For Morth it is done for demofile3 to demofile848

ID is stored as filename/pageno/paragraph no. First index for IRC .Then for Morth

4]Search is performed on the user interface.


Flask runs on  http://127.0.0.1:8000/

