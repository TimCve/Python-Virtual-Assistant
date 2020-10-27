import requests
import mwparserfromhell

from Assistant.Base.tts import sayAsync

def makeQuery(query):
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': query,
            'prop': 'revisions',
            'rvprop': 'content',
        }
    ).json()

    page = next(iter(response['query']['pages'].values()))
    try:
        wikicode = page['revisions'][0]['*']
    except KeyError:
        return "appologies, no wiki page found for " + query

    parsedWikicode = mwparserfromhell.parse(wikicode)

    infoRecieved = parsedWikicode.strip_code()

    if infoRecieved.split(" ")[0] == "REDIRECT" or infoRecieved.split(" ")[0] == "Redirect":
        return makeQuery(infoRecieved.split(" ", 1)[1])

    result = list(filter(lambda x : x != '', infoRecieved.split('\n\n')))[1]
    
    print(result)
    sayAsync(result)