#!env python3
import pandas as pd
import jieba
import gensim
from datetime import datetime as dt
from datetime import timedelta
from gensim import corpora
from gensim.corpora.dictionary import Dictionary

df = pd.read_csv(
    "data/stopwords.txt", encoding="GBK", header=None, on_bad_lines="skip", sep="\r\n"
)
stopwords = df[0].tolist()
stopset = {w for w in stopwords}


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
        raw = jieba.lcut(t)
        clean = []
        for r in raw:
            if r not in ["肺炎", "疫情", "新冠", "病毒", " ", "武汉"] and r not in stopset:
                clean.append(r)
        common_text.append(clean)
    common_dict = corpora.Dictionary(common_text)
    common_corpus = [common_dict.doc2bow(text) for text in common_text]
    print("building lda")
    lda = gensim.models.LdaModel(
        eval_every=1,
        alpha="auto",
        eta="auto",
        corpus=common_corpus,
        id2word=common_dict,
        num_topics=10,
        passes=80,
    )
    print("lda done")
    return (lda, common_dict)


df, related = read_data()

# lda model
lda, common_dict = get_lda(related["title"].to_list())

# topics

# split data by date range
# end_time should be rather useless
min_st = df["start_time"][0]
max_st = df["start_time"][df.index.size - 1]
interval = 15  # day
cur_st = min_st
x_v = []
split_data = []
while cur_st < max_st:
    ret = get_range(cur_st, cur_st + timedelta(days=interval), related)
    cur_st += timedelta(days=interval)
    if ret.index.size == 0:
        continue
    split_data.append(ret)
    x_v.append(cur_st)

# process split data
lda_topics = lda.show_topics(num_topics=-1, num_words=4)


# hot for a (topic, data range)
def get_count(topic_ind, split):
    tot_hot = 0
    for sc in split["searchCount"]:
        tot_hot += sc

    test_text_ind = []
    titles = split["title"]
    for z in titles.items():
        test_text_ind.append((z[0], jieba.lcut(z[1])))
    test_corpus = [common_dict.doc2bow(text[1]) for text in test_text_ind]
    test_topic_distribution = lda[test_corpus]

    topic_docs = []
    topic_hot = 0
    for i, doc_topics in enumerate(test_topic_distribution):
        test_doc = test_text_ind[i][1]
        ind = test_text_ind[i][0]
        sorted_topics = sorted(
            doc_topics, key=lambda x: -x[1]
        )  # sort topics by relevance
        most_relevant_topic = sorted_topics[0]  # id, relevance
        relevance = most_relevant_topic[1]
        if most_relevant_topic[0] == topic_ind and relevance > 0.7:
            topic_docs.append(test_doc)
            topic_hot += split["searchCount"][ind]
    return len(topic_docs), int((topic_hot * 100) / tot_hot), int(topic_hot / 10000)


# x_v = [x for x in range(0, len(split_data))]
y_v = []
for topic_ind in range(0, len(lda_topics)):
    print(f"Topic {topic_ind}: {lda_topics[topic_ind][1]}")
    cur_v = []
    for sd in split_data:
        cnt, hot_relative, hot_tot = get_count(topic_ind, sd)
        # print(cnt, int(hot), end="\t")
        print(hot_tot, end="\t")
        cur_v.append(hot_tot)
    print()
    y_v.append(cur_v)

from line_chart import plot_line_chart

legend = ["dr" + str(x) for x in x_v]
legends = []
for i in range(0, len(lda_topics)):
    legends.append(lda_topics[i][1])

cur_st = min_st
plot_line_chart(x_v, y_v, legend_labels=legends)
