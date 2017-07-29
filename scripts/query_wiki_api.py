import re
import json
import urllib.request

def query_wiki_api(title):
    '''
    Use the title to query the Media Wiki API.

    INPUT
    title : str
      title of Wiki article
    
    OUTPUT
    return : json
    '''
    base_query = 'https://en.wikipedia.org/w/api.php?action=query&titles= &prop=revisions&rvprop=content&format=json'
    query = re.sub(' ', title, base_query)
    query = re.sub(' ', '%20', query)
    result = urllib.request.urlopen(query).read()
    article_dict = json.loads(test_result)
    return article_dict

def get_text_from_wiki_api(title):
    '''
    Extracts the article text from Media Wiki API query

    INPUT
    title : str
      title of Wiki article
    
    OUTPUT
    return : str
      raw article text
    '''
    article_dict = query_wiki_api(title)
    wiki_id = list(article_dict['query']['pages'].keys())[0]
    return article_dict['query']['pages'][wiki_id]['revisions'][0]['*']
