import csv
import json
from client import RestClient
from bs4 import BeautifulSoup

# You can download this file from here https://cdn.dataforseo.com/v3/examples/python/python_Client.zip
client = RestClient("user_name", "pw")

# Function to read keywords from CSV file
def read_keywords_from_csv(file_path):
    keywords = []
    with open(file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            keywords.append(row['keyword'])
    return keywords

# Read keywords from the CSV file
keywords = read_keywords_from_csv('keywords.csv')

# Iterate over each keyword and send request to the API
for keyword in keywords:
    post_data = dict()
    post_data[len(post_data)] = dict(
        language_code="en",
        location_code=2840,
        keyword=keyword,
        device="mobile",
        os="ios"
    )

    # POST /v3/serp/google/organic/live/html
    response = client.post("/v3/serp/google/organic/live/html", post_data)

    # Check response and save to JSON file
    if response["status_code"] == 20000:
        # Prettify the HTML content
        if 'html' in response['tasks'][0]['result'][0]:
            soup = BeautifulSoup(response['tasks'][0]['result'][0]['html'], 'html.parser')
            response['tasks'][0]['result'][0]['html'] = soup.prettify()

        file_name = f'response_{keyword}.json'
        with open(file_name, 'w') as json_file:
            json.dump(response, json_file, indent=4, ensure_ascii=False)
    else:
        print("error. Code: %d Message: %s for keyword: %s" % (response["status_code"], response["status_message"], keyword))
