# Get started

Go to a directory of you choice and clone this repository:

```
git clone https://github.com/panpan2557/ArticleQ.git
cd articleq
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
###### Download Neo4j
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
python articleq/manage.py migrate
python articleq/manage.py bootstrap
python articleq/manage.py runserver
```

Go to http://localhost:8000 in your favorite browser to see the tutorial app.



