import sys
import re
import numpy as np
import pandas as pd
from query_wiki_api import *

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

def generate_dist_n_links_from_df(df, dist=1):
    '''
    For each article, get a list of the titles of all internally-linked Wiki articles
    INPUT
    df : pd.DataFrame
      rows: wiki ids, columns: titles, text_raw
    dist : int
      max number of links that must be traversed between articles
      
    OUTPUT
    pd.DataFrame
      rows: wiki ids, columns: titles, dist1_titles (titles of 1-distance links)
    '''
    for n in np.arange(1, dist+1):
        if n == 1:
            out_df = generate_dist_1_links_from_df(df)
        else:
            in_col_name = 'dist%i_titles' % (n-1)
            out_col_name = 'dist%i_titles' % (n)
            out_df.loc[:, out_col_name] = np.nan
            out_df[out_col_name] = out_df[out_col_name].astype(object)
            for wiki_id, title in zip(df.index, df.title):
                tmp_titles = out_df.loc[wiki_id, in_col_name]
                tmp_out_dfs = []
                try:
                    for tmp_title in tmp_titles:
                        try:
                            tmp_df = pd.DataFrame(columns = ['title', 'text_raw'])
                            tmp_dict = query_wiki_api(tmp_title)
                            tmp_wiki_id = list(tmp_dict['query']['pages'].keys())[0]
                            tmp_text_raw = tmp_dict['query']['pages'][tmp_wiki_id]['revisions'][0]['*']
                            tmp_df.loc[tmp_wiki_id] = [tmp_title, tmp_text_raw]
                            tmp_out_df = generate_dist_1_links_from_df(tmp_df)
                            tmp_out_dfs.append(tmp_out_df)
                        except:
                            pass
                    tmp_out_titles = sum([list(tmp_out_df[in_col_name].values[0]) for tmp_out_df in tmp_out_dfs],[])
                    out_df.loc[wiki_id, out_col_name] = tmp_out_titles
                except:
                    pass
    return out_df
