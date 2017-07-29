import re

def find_internal_wiki_links(text):
    '''
    Returns the titles and urls of all internal links in a Wikipedia article.

    INPUT
    text : str
      raw text of a Wikipedia article containing internal Wiki links: [[link]]

    OUTPUT
    return : list of tuples
      titles and urls in internal Wiki links
      [(title_1,  url_1), ..., (title_n, url_n)]
    '''
    searchstr = '(\[[^\[\]]*\[.*?\][^\]\[]*\])'
    link_urls = []
    link_titles = []
    link_titles_raw = re.findall(searchstr, text)
    for link_title_raw in link_titles_raw:
        link_title = re.sub('\[\[', '', link_title_raw)#remove brackets
        link_title = re.sub('\]\]', '', link_title)#remove brackets
        link_title = re.sub('\|.+', '', link_title)#remove junk at end
        link_titles.append(link_title)
        link_title = re.sub(' ', '_',  link_title)
        link_url = 'https://en.wikipedia.org/wiki/%s' % (link_title)
        link_urls.append(link_url)
    return list(set(zip(link_titles, link_urls)))
