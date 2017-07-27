def get_topic_model(tfidf,corpus,dictionary,num_topics,model):

    # Num topics, is the dimensionality.
    # We reduce the dimension from words to a given number of topics
    topic_model = model(tfidf[corpus], id2word=dictionary, num_topics=num_topics)
    
    # To see topics uncomment:
    #for topic in topic_model.print_topics(5):
        #print('Topic: {}'.format(topic[0]))
        #print(str(topic).replace(' + ', '\n')) 
        #print('') 
    return topic_model
