# Get started

Go to a directory of you choice and clone this repository:

```
git clone https://github.com/johanlundberg/neo4j-django-tutorial.git
cd neo4j-django-tutorial
```

Create virtualenv inside the repository and activate it:

```
virtualenv articleqenv
source articleqenv/bin/activate
```

Install the packages that you need.

```
pip install -r requirements.txt
```

##### Neo4j
###### Alt 1. With Docker

If you have Docker installed just run the below command to start a Neo4j server.
```
docker run -p=7474:7474 -p=7687:7687 --volume=path/to/tutorial/neo4j/data:/data --volume=path/to/tutorial/neo4j/logs:/logs neo4j:latest
```
This tutorial was last tested with Neo4j 3.1.1 which you will get if you replace the latest tag with 3.1.1.

###### Alt 2. Download Neo4j
Download the latest Neo4j Community Edition from http://www.neo4j.org/download/.

Untar it anywhere and start it:

```
tar xvfz /path/to/neo4j-community-3.x.z-unix.tar.gz
cd neo4j-community-3.x.z-unix
bin/neo4j start
```

###### After Neo4j is started
Go to http://localhost:7474 in your favorite browser and update the default password. 

##### Wrapping up and starting the app
Edit articleq/articleq/setting.py, change the password to the one that has been updated.

Then, run following code.

```
python neo4jtut/manage.py migrate
python neo4jtut/manage.py bootstrap
python neo4jtut/manage.py runserver
```

Go to http://localhost:8000 in your favorite browser to see the tutorial app.



