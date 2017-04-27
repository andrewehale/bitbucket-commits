#!/usr/local/bin/python

import json, requests, dateutil.parser, datetime
from collections import defaultdict

username = "user"
password = "password"
baseUrlv1 = "http://bitbucket-server-hostname/rest/api/1.0"
year = 2017

def getAllItems(baseUrl):
	allItems = []
	r = requests.get(baseUrl, auth=(username,password))
	c = r.json()
	if 'values' not in c:
		print c #debug

	allItems.extend(c['values'])
	while not c['isLastPage']:
		r = requests.get("{base}?start={nextPageStart}".format(base=baseUrl, 
			nextPageStart=c['nextPageStart']),
			auth=(username,password))
		c = r.json()
		allItems.extend(c['values'])

	return allItems

def iterateAllCommitsForRepo(key, slug):
	allCommits = getAllItems("{base}/projects/{key}/repos/{slug}/commits".
		format(base=baseUrlv1,key=key,slug=slug))

	for commit in allCommits:
		#print commit
		commitDate = datetime.datetime.fromtimestamp(commit['authorTimestamp']/1000)
		print commitDate
		print commitDate.year
		if commitDate.year == year:			
			name = commit['author']['name']
			d[name] += 1



def iterateRepositoriesForProject(key):
	allRepositories = getAllItems("{base}/projects/{key}/repos".format(base=baseUrlv1,key=key))
	for repository in allRepositories:
		print repository['slug']
		iterateAllCommitsForRepo(key, repository['slug'])

def iterateAllProjects():
	allProjects = getAllItems("{base}/projects".format(base=baseUrlv1))
	for project in allProjects:
		iterateRepositoriesForProject(project['key'])


d = defaultdict(int)
iterateAllProjects()
print d


quit()

	

