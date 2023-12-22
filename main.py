from collections import Counter
from gensim import corpora
from gensim.models import LdaModel
from gensim import models
from gensim import similarities
import jieba
import pandas as pd
import spacy

# 加载spaCy的中文模型
nlp = spacy.load("zh_core_web_lg")

data=pd.read_excel("D:\\期末作业数据/Weibo_2020Coron.xlsx")
# 假设titles是热搜标题的列表
print(data.columns)
titles =data[data['Coron-Related ( 1 yes, 0 not ) ']==1.0]
print(titles)
titles=titles["title"]
title=""
for i in  titles:
    i=i+','
    title+=i;


doc = nlp(title)
# 遍历每个标题
tokens=[]
for token in doc:
    if token.pos_=="NOUN":
        tokens.append(token.text)
noun_frequencies = Counter(tokens)

    # 找出前10个最常见的名词
top_nouns = noun_frequencies.most_common(100)
print(top_nouns)

# 输出：
# 武汉卫健委通报不明原因肺炎
# 专家组
# 现场调查


for ent in doc.ents:
    print(f"Entity: {ent.text}, Label: {ent.label_}")

# 提取人名、地名、机构名
persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON" ]
locations = [ent.text for ent in doc.ents if (ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_ == "FAC")]
organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]

print(f"Title: {title}")
print("Persons:", persons)
print("Locations:", locations)
print("Organizations:", organizations)
print("\n" + "="*50 + "\n")

texts = [list(map(str, jieba.tokenize(doc))) for doc in titles]


# 创建字典和语料库
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# 使用 LDA 模型
lda_model = LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15)

# 打印主题
topics = lda_model.print_topics(num_words=5)
for topic in topics:
    print(topic)    i=i+','
    title+=i;


doc = nlp(title)
# 遍历每个标题
tokens=[]
for token in doc:
    if token.pos_=="NOUN":
        tokens.append(token.text)
noun_frequencies = Counter(tokens)

    # 找出前10个最常见的名词
top_nouns = noun_frequencies.most_common(100)
print(top_nouns)

# 输出：
# 武汉卫健委通报不明原因肺炎
# 专家组
# 现场调查


for ent in doc.ents:
    print(f"Entity: {ent.text}, Label: {ent.label_}")

# 提取人名、地名、机构名
persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON" ]
locations = [ent.text for ent in doc.ents if (ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_ == "FAC")]
organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]

print(f"Title: {title}")
print("Persons:", persons)
print("Locations:", locations)
print("Organizations:", organizations)
print("\n" + "="*50 + "\n")

texts = [list(map(str, jieba.tokenize(doc))) for doc in titles]


# 创建字典和语料库
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# 使用 LDA 模型
lda_model = LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15)

# 打印主题
topics = lda_model.print_topics(num_words=5)
for topic in topics:
    print(topic)