def matsim2np(matsim):
    """
    Converts a gensim matsim object into a numpy array.

    Input:
    matsim, gensim matsim object.

    Output:
    np_sims, numpy array, shape=number_of_documents x number_of_documents
    Contains similarity scores between two documents.

    Notes:
    The ordering of the columns, files refers to the initial ordering (before the matrix transformation by lsi, lda, etc).
    Each cell in the numpy array is the similarity score between two documents.

    """
    import numpy as np
    #matsim to np matrix
    
    num_docs=len(matsim)
    docs=np.arange(0,num_docs)
    np_sims=np.zeros((num_docs,num_docs))
    for doc_index,sims in zip(docs,matsim):
        for other_doc, score in sims:
            np_sims[doc_index][other_doc]=score
    
    return np_sims
