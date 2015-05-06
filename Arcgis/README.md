This is our team repository

    A project simulating the traffic in a certain city.

The whole project contains four parts including the 

frontend, backend, middleware and simulation unit.

    Frontend is the user interface containing several

parts like selecting the configuration, start button,

pause button, as well as stop button. Besides this, 

the road-block and traffic accident can be added through

the interface.

    Backend, is a web server. It receives the request 

from the frontend and collecting response from middleware.

Backend is based on web.py, a light server of python.

    Middleware...

    some updates

    Simulation...


======================= Additional NOTE ================================

 how to get our project online on github

 TIPS:
1, sudo apt-get install git

       git config --global user.email "nisxiya@yeah.net"

       git config --global user.name "nisxiya"

2, sudo apt-get install ssh

3, ssh-keygen -t rsa -C "your email addr"

4, attach ~/.ssh/id_rsa.pub's content to your github personal account.
       Account Settings -> SSH keys.

5, cd to your home directory and find a proper place to store the Arcgis project online.
       cd ~/home/workplace
       git clone git@github.com:hustjf/Arcgis.git

6, Enjoy the project :D.


some necessary packages for running the project.
These packages may be installed in the following way.


1, web.py 

sudo apt-get install python-setuptools      # to get easy_install tools.

sudo easy_install web.py

2, pika

sudo easy_install pika

3, pymongo

3.1 
sudo apt-get install mongodb

config to allow remote access.
sudo vim /etc/mongodb.conf 

bind_ip = 0.0.0.0
port = 27017
auth = true

save and exit.

sudo service mongodb restart

3.2 
sudo easy_install pymongo

4, rabbitmq
sudo apt-get install rabbitmq-server

5, networkx
sudo easy_install networkx


6. simplejson
sudo apt-get install python-simplejson

7. xlrd   (this is for reading and writing excel)
sudo easy_install xlrd


===================================== About the document of the project =====================

The following is to store the the documents of our project, including the resorces and daily log as well as the weekly log

Addr: git@code.csdn.net:nisxiya/traffic_simulation_project_document.git

please send your personal csdn account to me before you fork this project.

come on!


