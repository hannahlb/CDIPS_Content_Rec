
def merge_Wiki_pages(root):
    import os, sys
    import pandas as pd
    import numpy as np
    sys.path.insert(0, 'scripts')
    from WikiPage import WikiPage
    
    # Initialize dataframe with first page:
    # Note that root[0] is skipped.
    df=WikiPage(root[1]).data  
    # Append rest of pages
    for page_index in range(2,len(root)):
        page = WikiPage(root[page_index])
        df=df.append(page.data)
    
    df=df.set_index('id')
    return(df)
