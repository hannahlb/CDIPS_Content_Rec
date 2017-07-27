
def get_similarity_matrix(article_ids,corpus,num_best,num_sims):
    """
    Gets a matrix with the similar articles for each article id.
    
    Arguments:
    article_ids: list, list of article ids
    corpus: corpus for gensim
    num_best: num_best parameter in gensim:
            If num_best is set, queries return only the num_best most similar documents, always leaving out documents for which the similarity is 0. If the input vector itself only has features with zero values (=the sparse representation is empty), the returned list will always be empty.
    num_sims: number of similar articles to save in array

    Output:
    matsim: matrix of similar articles in gensim format
    similarity_matrix: matrix of similar articles:
        columns=(article_id,similar_articles,scores), 
            similar_articles is a list of other article ids (ordered by degree of similarity)
            scores is a list of similarity scores for each other article id.
            The closer to 1, the more similar. 
    """
    from gensim import similarities
    from collections import defaultdict


    matsim=similarities.MatrixSimilarity(corpus,num_best=num_best)
    similarity_matrix=defaultdict(list)
    # the output is saved now in the "similarity_matrix" array
    for article_id, sims in zip(article_ids, matsim):
        similarity_matrix[article_id].append([]) #this contains list or similar articles
        similarity_matrix[article_id].append([]) #this will contains score list
        for other_id, score in sims[1:num_sims+1]:
            similarity_matrix[article_id][0].append(article_ids[other_id])
            similarity_matrix[article_id][1].append(score)
    
    return similarity_matrix,matsim


def get_similarity_matrix_sparse(article_ids,corpus,num_best,num_sims):
    """
    Gets a matrix with the similar articles for each article id.
    
    Arguments:
    article_ids: list, list of article ids
    corpus: corpus for gensim
    num_best: num_best parameter in gensim:
            If num_best is set, queries return only the num_best most similar documents, always leaving out documents for which the similarity is 0. If the input vector itself only has features with zero values (=the sparse representation is empty), the returned list will always be empty.
    num_sims: number of similar articles to save in array

    Output:
    matsim: matrix of similar articles in gensim format
    similarity_matrix: matrix of similar articles:
        columns=(article_id,similar_articles,scores), 
            similar_articles is a list of other article ids (ordered by degree of similarity)
            scores is a list of similarity scores for each other article id.
            The closer to 1, the more similar. 
    """
    from gensim import similarities
    from collections import defaultdict


    matsim=similarities.SparseMatrixSimilarity(corpus,num_best=num_best,num_features=10)
    similarity_matrix=defaultdict(list)
    # the output is saved now in the "similarity_matrix" array
    for article_id, sims in zip(article_ids, matsim):
        similarity_matrix[article_id].append([]) #this contains list or similar articles
        similarity_matrix[article_id].append([]) #this will contains score list
        for other_id, score in sims[1:num_sims+1]:
            similarity_matrix[article_id][0].append(article_ids[other_id])
            similarity_matrix[article_id][1].append(score)
    
    return similarity_matrix,matsim

