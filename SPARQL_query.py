# Guided Reference: https://janakiev.com/blog/wikidata-mayors/

import requests
import pandas as pd
from collections import OrderedDict

"""
Notes:
    - war (Q198)
    - participant (P710)
    - United States of America (Q30)

    - Example war: Gulf War (Q37643)
        - instance of : war
        - start time : 2 August 1990
        - end time : 28 Februrary 1991
        - participant : ...
        - (*No death information*)
        
    - Example war: Vietnam War (Q8740)
        - (same fields as above)
        - number of deaths : 1,291,425
                           : 4,211,459
"""

url = 'https://query.wikidata.org/sparql'

## This query selects all events that are an instance of war
# query = """
# SELECT 
  # ?event ?eventLabel
# WHERE {
  # ?event wdt:P31/wdt:P279* wd:Q198.
  # SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
# }
# """

# This query selects all events that are an instance of war, AND that the event participant is United States
# query = """
# SELECT 
  # ?event ?eventLabel ?startDate ?endDate
# WHERE {
  # ?event wdt:P31/wdt:P279* wd:Q198.
  # ?event wdt:P710 wd:Q30.
  # ?event wdt:P580 ?startDate.
  # ?event wdt:P582 ?endDate.
  # SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
# }
# """

## This query selects all events that are an instance of war, AND all the participants
query = """
SELECT 
  ?event ?eventLabel ?startDate ?endDate ?participants
WHERE {
  ?event wdt:P31/wdt:P279* wd:Q198.
  ?event wdt:P710 ?participants.
  ?event wdt:P580 ?startDate.
  ?event wdt:P582 ?endDate.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
"""

r = requests.get(url, params = {'format': 'json', 'query': query})
# print(r.text)
data = r.json()
# print(data)

wars = []
for item in data['results']['bindings']:
    wars.append(OrderedDict({
        'war_Qid': item['event']['value'].split('/')[-1],
        'warLabel': item['eventLabel']['value'],
        'startDate': item['startDate']['value'],
        'endDate': item['endDate']['value'],
        'participants': item['participants']['value']
        }))

df = pd.DataFrame(wars)
print(df)
# df.to_csv('./ALL_wars_AND_participants.tsv', sep='\t')





## Example from online guide: https://janakiev.com/blog/wikidata-mayors/

# query = """
# SELECT 
  # ?countryLabel ?population ?area ?medianIncome ?age
# WHERE {
  # ?country wdt:P463 wd:Q458.
  # OPTIONAL { ?country wdt:P1082 ?population }
  # OPTIONAL { ?country wdt:P2046 ?area }
  # OPTIONAL { ?country wdt:P3529 ?medianIncome }
  # OPTIONAL { ?country wdt:P571 ?inception. 
    # BIND(year(now()) - year(?inception) AS ?age)
  # }
  # SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
# }
# """
# r = requests.get(url, params = {'format': 'json', 'query': query})
# data = r.json()
# print(data)


# countries = []
# for item in data['results']['bindings']:
    # countries.append(OrderedDict({
        # 'country': item['countryLabel']['value'],
        # 'population': item['population']['value'],
        # 'area': item['area']['value'] 
            # if 'area' in item else None,
        # 'medianIncome': item['medianIncome']['value'] 
            # if 'medianIncome' in item else None,
        # 'age': item['age']['value'] 
            # if 'age' in item else None}))

# df = pd.DataFrame(countries)
# df.set_index('country', inplace=True)
# df = df.astype({'population': float, 'area': float, 'medianIncome': float, 'age': float})
# print(df.head())
