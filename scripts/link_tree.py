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
        link_title = re.sub('\|.+', '', link_title_raw)#remove junk at end
        link_title = re.sub('\#.+', '', link_title)#remove junk at end
        link_title = re.sub('\[\[', '', link_title)#remove brackets
        link_title = re.sub('\]\]', '', link_title)#remove brackets
        if remove_non_articles:
            if link_type_from_title(link_title) != 'article':
                continue
        link_titles.append(link_title)
        link_title = re.sub(' ', '_',  link_title)
        link_url = 'https://en.wikipedia.org/wiki/%s' % (link_title)
        link_urls.append(link_url)
    return list(set(zip(link_titles, link_urls)))

def link_type_from_title(title):
    if 'Category:' in title:
        return 'category'
    elif 'Portal:' in title:
        return 'portal'
    elif 'List of' in title:
        return 'list'
    elif 'File:' in title:
        return 'file'
    elif 'Image:' in title:
        return 'image'
    else:
        return 'article'

def generate_dist_1_links_from_df(df):
    '''
    For each article, get a list of the titles of all internally-linked Wiki articles
    INPUT
    df : pd.DataFrame
      rows: wiki ids, columns: titles, text_raw
      
    OUTPUT
    pd.DataFrame
      rows: wiki ids, columns: titles, dist1_titles (titles of 1-distance links)
    '''
    out_df = pd.DataFrame(columns = ['title', 'dist1_titles'])
    for idx in df.index:
        text = df.text_raw.loc[idx]
        title = df.title.loc[idx]
        dist1_links = np.array(find_wiki_links(text))
        try:
            dist1_titles = list(dist1_links[:,0])
            out_df.loc[idx] = [title, dist1_titles]
        except:
            out_df.loc[idx] = [title, np.nan]
    return out_df
