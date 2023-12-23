from collections import Counter
from gensim import corpora
from gensim.models import LdaModel
from gensim import models
from gensim import similarities
import jieba
import pandas as pd
import spacy

# 加载spaCy的中文模型
nlp = spacy.load("zh_core_web_md")

# data=pd.read_excel("D:\\期末作业数据/Weibo_2020Coron.xlsx")
# # 假设titles是热搜标题的列表
#
# titles =data[data['Coron-Related ( 1 yes, 0 not ) ']==1.0]
#
# titles=titles["title"]
# title=""
# for i in  titles:
#     i=i+','
#     title+=i;
#
#
# doc = nlp(title)
# # 遍历每个标题
# tokens=[]
# for token in doc:
#     if token.pos_=="NOUN":
#         tokens.append(token.text)
# noun_frequencies = Counter(tokens)
#
#     # 找出前10个最常见的名词
# top_nouns = noun_frequencies.most_common(100)
# print(top_nouns)
#
# # 输出：
# # 武汉卫健委通报不明原因肺炎
# # 专家组
# # 现场调查
#
#
# # for ent in doc.ents:
# #     print(f"Entity: {ent.text}, Label: {ent.label_}")
#
# # 提取人名、地名、机构名
# persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON" ]
# locations = [ent.text for ent in doc.ents if (ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_ == "FAC")]
# organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
#
# print(f"Title: {title}")
# print("Persons:", persons)
# print("Locations:", locations)
# print("Organizations:", organizations)
# print("\n" + "="*50 + "\n")
#
# texts = [list(map(str, jieba.tokenize(doc))) for doc in titles]
#
#
# # 创建字典和语料库
# dictionary = corpora.Dictionary(texts)
# corpus = [dictionary.doc2bow(text) for text in texts]
#
# # 使用 LDA 模型
# lda_model = LdaModel(corpus, num_topics=1, id2word=dictionary, passes=15)
#
# # 打印主题
# topics = lda_model.print_topics(num_words=5)
# for idx, topic in enumerate(topics):
#     print(f"主题 {idx+1}: {topic}")
# #!env python3




import pandas as pd
from datetime import datetime as dt, datetime, timedelta

# preprocessing
# read, rename, dropna
df=pd.read_excel("D:\\期末作业数据/Weibo_2020Coron.xlsx")
# df = pd.read_csv("data/Douyin_2020Coron.csv")
new_columns=['end_time','start_time','title_en','title','searchCount','is_related']
df.columns=new_columns
# df = df[["start_time", "title", "rank","words_list"]]
df["is_related"].fillna(0, inplace=True)
dt_format = "%Y-%m-%d %H:%M:%S"
# df["start_time"] = df["start_time"].str.replace('/', '-')

df["start_time"] = pd.to_datetime(df["start_time"], format=dt_format)
df["end_time"] = pd.to_datetime(df["end_time"], format=dt_format)
df = df.dropna()  # x rows valid data
df = df.sort_values(by="start_time")
df = df.reset_index().drop('index', axis=1)

related = df[df["is_related"] != 0]
print(related)

def get_range(start, end):
    return related[(related['start_time'] > start) & (related['end_time'] <= end)]
from datetime import datetime, timedelta

start_time=datetime(2019,10,28,0,0,0)
end_time = datetime(2020, 4, 9,0,0,0)

# 计算日期范围的总天数
total_days = (end_time - start_time).days

# 计算每个部分的天数
days_per_section = total_days // 10

# 分割日期范围
date_sections = [start_time + timedelta(days=i * days_per_section) for i in range(10)]
for section_start_date, section_end_date in zip(date_sections, date_sections[1:]):
    print(f"From {section_start_date.strftime('%Y-%m-%d %H:%M:%S')} to {section_end_date.strftime('%Y-%m-%d %H:%M:%S')}")
    related_part=get_range(section_start_date,section_end_date)
    titles=related_part['title']
    title = ""
    for i in titles:
        i = i + '。'
        title += i;

    doc = nlp(title)
    # 遍历每个标题
    tokens = []
    for token in doc:
        if token.pos_ == "NOUN":
            tokens.append(token.text)
    noun_frequencies = Counter(tokens)

    # 找出前10个最常见的名词
    top_nouns = noun_frequencies.most_common(5)
    print(top_nouns)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    locations = [ent.text for ent in doc.ents if (ent.label_=="GPE")]#ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_ == "FAC"
    organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]

    location_counts = Counter(locations)

    # 获取最高频的五个地理位置
    top_ten_locations = location_counts.most_common(10)

    print("Persons:", persons)
    print("Locations:", top_ten_locations)
    print("Organizations:", organizations)



# 合并相同 'start_time' 和 'end_time' 的 'searchCount' 列值
# result = related.groupby(['start_time', 'end_time','title','is_related'], as_index=False)['searchCount'].sum()
# result.to_csv("Weibo.csv",index=False)

# 将其他列的值保留一个（如果其他列的值相同的话）
