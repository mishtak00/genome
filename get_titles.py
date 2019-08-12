import requests
import csv

base_url = 'https://app.dimensions.ai/api/'
uni = 'University of Rochester'

def initialize_session():

	login = {
		'username': '',
		'password': ''
	}

	print('\nInitializing session...\n')

	resp = requests.post(base_url + 'auth.json', json=login)
	resp.raise_for_status()

	header = {
		'Authorization': 'JWT ' + resp.json()['token']
	}

	print('Session in progress...\n')

	return header

def title_count(header):

	query = 'search publications where research_orgs.name="{}" and FOR.name="0604 Genetics" return publications[doi]'.format(uni)

	response = requests.post(
		base_url + 'dsl.json',
		data=query.encode(),
		headers=header)
	
	return response.json()['_stats']['total_count']


def query_titles(header, skip):

	query = 'search publications where research_orgs.name="{}" and FOR.name="0604 Genetics" return publications[title] limit 1000 skip {}'.format(uni, str(skip))

	response = requests.post(
		base_url + 'dsl.json',
		data=query.encode(),
		headers=header)
	
	return response.json()['publications']



with open(uni+'_titles_FOR.txt', 'w', encoding='utf-8') as titles:

	header = initialize_session()

	title_count = title_count(header)

	for skip in range(0, title_count, 1000):

		titles_queried = query_titles(header, skip)

		for row in titles_queried:

			title = row['title'] + '\n'

			print(title)

			titles.write(title)