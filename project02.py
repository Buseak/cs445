from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.lm import MLE, KneserNeyInterpolated
from nltk.lm.preprocessing import padded_everygram_pipeline
from gensim.models import Word2Vec
import statistics

stopwords_tr = []
f = open("stopwords_tr.txt", mode='r')
for word in f:
    word = word.rstrip("\n")
    stopwords_tr.append(word)


def doc_tokenized(docs):
    doc_tokenize = []
    for doc in docs:
        doc_tokenize += [list(map(str.lower, word_tokenize(sent)))
                         for sent in sent_tokenize(doc)]
    return (doc_tokenize)


# The function will create the word cloud and save it in the provided output file in png format.
def create_WordCloud(docs, dimension, wordcloud_outputfile, mode="TF", stopwords=False):
    dimension = dimension * 100

    if mode == "TF":
        # use_idf is False
        vectorizer = TfidfVectorizer(use_idf=False)
        vectors_sparse = vectorizer.fit_transform(docs)
        features = vectorizer.get_feature_names()

        vecs = vectors_sparse.todok()
        vecs = dict(vecs.items())


        a = list(vecs.keys())
        b = list(vecs.items())
        c = {}
        for i in range(len(a)):
            if c.get(a[i][1]) is None:
                c[a[i][1]] = 0
            if c.get(a[i][1]) is not None:
                c[a[i][1]] += b[i][1]

        vocab_dict = {}
        if stopwords==True:
            for key in c:
                if features[key] not in stopwords_tr:
                    vocab_dict[features[key]] = c[key]
        else:
            for key in c:
                vocab_dict[features[key]] = c[key]

        wc = WordCloud(background_color="white", width=dimension, height=dimension, max_words=len(features),
                       relative_scaling=0.5,
                       normalize_plurals=False).generate_from_frequencies(vocab_dict)
        if stopwords==True:
            plt.title("TF - Stopwords removed")
        else:
            plt.title("TF - Stopwords included")
        plt.imshow(wc)
        plt.savefig(wordcloud_outputfile)
        plt.show()

    elif mode == "TFIDF":
        # use_idf is True
        vectorizer = TfidfVectorizer(use_idf=True)
        vectors_sparse = vectorizer.fit_transform(docs)
        features = vectorizer.get_feature_names()

        vecs = vectors_sparse.todok()
        vecs = dict(vecs.items())


        a = list(vecs.keys())
        b = list(vecs.items())
        c = {}
        for i in range(len(a)):
            if c.get(a[i][1]) is None:
                c[a[i][1]] = 0
            if c.get(a[i][1]) is not None:
                c[a[i][1]] += b[i][1]

        vocab_dict = {}
        if stopwords == True: #remove stopwords
            for key in c:
                if features[key] not in stopwords_tr:
                    vocab_dict[features[key]] = c[key]
        else:
            for key in c:
                vocab_dict[features[key]] = c[key]

        wc = WordCloud(background_color="white", width=dimension, height=dimension, max_words=len(features),
                       relative_scaling=0.5,
                       normalize_plurals=False).generate_from_frequencies(vocab_dict)
        if stopwords==True:
            plt.title("TFIDF - Stopwords removed")
        else:
            plt.title("TFIDF - Stopwords included")
        plt.imshow(wc)
        plt.savefig(wordcloud_outputfile)
        plt.show()


def create_ZipfsPlot(docs, zips_outputfile):
    vectorizer = CountVectorizer()
    vectors_sparse = vectorizer.fit_transform(docs)
    features = vectorizer.get_feature_names()

    vecs = vectors_sparse.todok()
    vecs = dict(vecs.items())

    vecs_keys = list(vecs.keys())
    vecs_items = list(vecs.items())
    cumulative_dict = {}
    for i in range(len(vecs_keys)):
        if cumulative_dict.get(vecs_keys[i][1]) is None:
            cumulative_dict[vecs_keys[i][1]] = 0
        if cumulative_dict.get(vecs_keys[i][1]) is not None:
            cumulative_dict[vecs_keys[i][1]] += vecs_items[i][1]

    vocab_dict = {}
    for key in cumulative_dict:
        if features[key] not in stopwords_tr:
            vocab_dict[features[key]] = cumulative_dict[key]

    sorted_vocab_dict = sorted(vocab_dict.items(), key=lambda x: x[1], reverse=True)

    ranks = range(1, len(sorted_vocab_dict) + 1)
    freqs = [freq for (feature, freq) in sorted_vocab_dict]

    fig = plt.figure(figsize=(8, 8))
    plt.loglog(ranks, freqs)
    plt.xlabel('log(rank)')
    plt.ylabel('log(freq)')
    plt.title("Zipf's Plot")
    plt.savefig(zips_outputfile)
    plt.show()


def create_HeapsPlot(docs, heaps_outputfile):
    def extractDigits(lst):
        return [[el] for el in lst]

    docs_list = extractDigits(docs)

    vocab_list = []
    vocab_list_len = []
    doc_len = []
    doc_count = 0
    for i in docs_list:


        vectorizer = CountVectorizer()
        if len(i[0]) >= 1:

            vectors_sparse = vectorizer.fit_transform(i)
            features = vectorizer.get_feature_names()

            vecs = vectors_sparse.todok()
            values = list(vecs.values())
            word_count = 0
            feature_list = []
            for val in values:
                word_count += val

            if doc_count != 0 and len(docs_list[doc_count - 1][0]) > 0:
                doc_len.append((doc_len[doc_count - 1]) + word_count)

            else:
                if doc_count == 0:
                    doc_len.append(word_count)
                else:
                    doc_len.append(doc_len[doc_count - 2] + word_count)

            if len(vocab_list) == 0:
                vocab_list.append(features)
                vocab_list_len.append(len(features))


            else:

                for feature in features:
                    for vocab in vocab_list[docs_list.index(i) - 1]:
                        if feature == vocab:
                            if feature in features:
                                feature_index = features.index(feature)
                                features.pop(feature_index)


                feature_list.append(features + vocab_list[doc_count - 1])
                if len(feature_list) > 0:
                    vocab_list.append(feature_list[0])
                    vocab_list_len.append(len(feature_list[0]))

        else:
            doc_len.append(doc_len[doc_count - 1])
            vocab_list.append(vocab_list[doc_count - 1])
            vocab_list_len.append(vocab_list_len[doc_count - 1])
            # doc_len.append(0)
            # vocab_list_len.append(len(vocab_list[docs_list.index(i) - 1]))

        if (doc_count == 2000):


            figure = plt.figure(figsize=(8, 8))
            plt.plot(doc_len, vocab_list_len)
            plt.xlabel("term occurences")
            plt.ylabel("vocabulary size")
            plt.title("Heap's law")
            plt.savefig(heaps_outputfile)
            plt.show()

        doc_count += 1


    figure = plt.figure(figsize=(8, 8))
    doc_len.sort()
    plt.plot(doc_len, vocab_list_len)
    plt.xlabel("term occurences")
    plt.ylabel("vocabulary size")
    plt.title("Heap's law")
    plt.savefig(heaps_outputfile)
    plt.show()


    '''''
    figure = plt.figure(figsize=(8, 8))
    plt.scatter(vocab_list_len, doc_len)
    plt.savefig(heaps_outputfile)
    plt.show()
    '''''


def create_LanguageModel(docs, model_type, ngram):
    doc_tokenize = doc_tokenized(docs)

    # doc_tokenize += [list(map(str.lower, word_tokenize(sent)))
    #                 for sent in sent_tokenize(docs[0])]

    # print(doc_tokenize)
    train_data, padded_vocab = padded_everygram_pipeline(ngram, doc_tokenize)
    # print(list(padded_vocab))
    if model_type == "MLE":
        model = MLE(ngram)
        model.fit(train_data, padded_vocab)

        return model

    elif model_type == "KneserNeyInterpolated":
        model = KneserNeyInterpolated(ngram, discount=0.1)
        model.fit(train_data, padded_vocab)
        return model


def generate_sentence(model, text):
    ngram = model.order

    sentences = []

    for i in range(5):
        txt = text
        next_word = model.generate(text_seed=[txt])
        if next_word == '<s>' and next_word != '\"' and next_word != '.':
            next_word = model.generate(text_seed=[txt])

        word = next_word
        sentence = txt + ' ' + next_word + ' '
        word_count = 2
        while word != '</s>':

            word = model.generate(text_seed=[next_word])
            if word != '<s>' and word != '\"' and word != '..':
                if word != '</s>':
                    sentence += word + ' '
                else:
                    continue

                txt = next_word
                next_word = word
            elif word == '<s>':
                continue
        sentences.append(sentence)
        word_count += 1

    sentence_tokenize = doc_tokenized(sentences)

    test_data, _ = padded_everygram_pipeline(ngram, sentence_tokenize)

    perps = []
    for i, test in enumerate(test_data):
        perps.append(model.perplexity(test))

    max_prp = max(perps)
    max_prp_index = perps.index(max_prp)

    return sentences[max_prp_index], max(perps)


def create_WordVectors(docs, dimension, model_type, window_size):
    doc_tokenize = doc_tokenized(docs)
    if model_type == 'cbow':
        sg = 0
        wv = Word2Vec(doc_tokenize, size=dimension, sg=sg, window=window_size)

        return wv

    else:
        sg = 1  # skipgram
        wv = Word2Vec(doc_tokenize, size=dimension, sg=sg, window=window_size)

        return wv


def use_WordRelationship(WE, example_tuple_list, example_tuple_test):
    vocabulary = list(WE.wv.vocab)

    len_example = len(example_tuple_list)
    avg_dist_list = []
    for pair in example_tuple_list:
        pair_index = example_tuple_list.index(pair)

        if (pair[0] not in vocabulary) or (pair[1] not in vocabulary):
            example_tuple_list.pop(pair_index)
        if len_example == 0:
            print("Sorry, this operation cannot be performed!")
            return None
        if pair[0] in vocabulary and pair[1] in vocabulary:
            dist_list = list(WE[pair[0]] - WE[pair[1]])
            avg_dist = statistics.mean(dist_list)
            avg_dist_list.append(avg_dist)

    if len(avg_dist_list) == 0:
        print("Sorry, this operation cannot be performed!")
        return None

    avg_dist = statistics.mean(avg_dist_list)
    if example_tuple_test[0] in vocabulary:
        dist_added = WE[example_tuple_test[0]] + avg_dist
        similar_words = list(WE.similar_by_vector(dist_added))

        indexx = 0
        for v, r in similar_words:
            if v == example_tuple_test[0]:
                similar_words.pop(indexx)
            indexx += 1
        print(similar_words[:5])
    else:
        print("Sorry, this operation cannot be performed!")
        return None
