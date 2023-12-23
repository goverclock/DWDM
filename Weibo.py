#!env python3
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta


# preprocessing, read, rename, dropna
def read_data():
    df = pd.read_csv("data/Weibo_2020Coron.csv")
    df = df.rename(
        columns={
            "Unnamed: 0": "end_time",
            "Unnamed: 1": "start_time",
            "Coron-Related ( 1 yes, 0 not ) ": "is_related",
        }
    )
    df = df[["start_time", "end_time", "title", "searchCount", "is_related"]]
    df["is_related"].fillna(0, inplace=True)
    dt_format = "  %Y-%m-%d %H:%M:%S"
    df["start_time"] = pd.to_datetime(df["start_time"], format=dt_format)
    df["end_time"] = pd.to_datetime(df["end_time"], format=dt_format)
    df = df.dropna()  # 9840 rows valid data
    df = df.sort_values(by="start_time")
    df = df.reset_index().drop("index", axis=1)
    # rows related to coron
    related = df[df["is_related"] != 0]  # 3322 rows
    return (df, related)


# return rows with date in [start, end]
def get_range(start, end, df):
    return df[(df["start_time"] >= start) & (df["start_time"] <= end)]


def get_lda(titles):
    common_text = []
    for t in titles:
        common_text.append(jieba.lcut(t))
    common_dict = corpora.Dictionary(common_text)
    common_corpus = [common_dict.doc2bow(text) for text in common_text]
    print("lda")
    lda = gensim.models.LdaModel(
        corpus=common_corpus, id2word=common_dict, num_topics=10, passes=100
    )
    print("lda done")
    return (lda, common_dict)


df, related = read_data()

# lda model
lda, common_dict = get_lda(related["title"].to_list())

# topics
for topic in lda.show_topics(num_topics=10, num_words=5):
    print(topic[0], topic[1])

# split data by date range
# end_time should be rather useless
min_st = df["start_time"][0]
max_st = df["start_time"][df.index.size - 1]
interval = 10  # day
cur_st = min_st
split_data = []
while cur_st < max_st:
    ret = get_range(cur_st, cur_st + timedelta(days=interval), related)
    cur_st += timedelta(days=interval)
    if ret.index.size == 0:
        continue
    split_data.append(ret)


# process split data
lda_topics = lda.show_topics(num_topics=10, num_words=5)

titles = split_data[4]["title"]
test_text = []
for t in titles:
    test_text.append(jieba.lcut(t))

test_corpus = [common_dict.doc2bow(text) for text in test_text]

test_topic_distribution = lda[test_corpus]

topic_ind = 8
topic_docs = []
for i, doc_topics in enumerate(test_topic_distribution):
    test_doc = test_text[i]
    sorted_topics = sorted(doc_topics, key=lambda x: -x[1])  # sort topics by relevance
    most_relevant_topic = sorted_topics[0]  # id, relevance
    if most_relevant_topic[0] == topic_ind:
        topic_docs.append(test_doc)
    # print(f"doc={test_doc}, most rt={most_relevant_topic}")
    # print(f"Document {i} = '{test_doc}'")
    # for topic, relevance in sorted_topics:
    #     print(f"Topic {topic}: {relevance:.3f} = {lda_topics[topic][1]}")

for t in topic_docs:
    print(t)

print(lda_topics[topic_ind][1])
