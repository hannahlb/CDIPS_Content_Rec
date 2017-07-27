def matsim2np(matsim):
    import numpy as np
    #matsim to np matrix
    
    num_docs=len(matsim)
    docs=np.arange(0,num_docs)
    np_sims=np.zeros((num_docs,num_docs))
    for doc_index,sims in zip(docs,matsim):
        for other_doc, score in sims:
            np_sims[doc_index][other_doc]=score
    
    return np_sims
