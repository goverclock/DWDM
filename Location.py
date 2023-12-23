from collections import Counter

import pandas as pd
from datetime import datetime as dt, datetime, timedelta

import spacy


nlp = spacy.load("zh_core_web_md")
df=pd.read_excel("./Weibo_2020Coron.csv")
# df = pd.read_csv("data/Douyin_2020Coron.csv")
new_columns=['end_time','start_time','title_en','title','searchCount','is_related']
df.columns=new_columns
# df = df[["start_time", "title", "rank","words_list"]]
df["is_related"].fillna(0, inplace=True)
dt_format = " %Y-%m-%d %H:%M:%S"


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
# pd.set_option("display.max_rows",None)
# pd.set_option("display.max_columns",None)
# print(related[(related['searchCount']>=3000000 )& ((related['start_time']<=datetime(2020,1,22,0,0,0) )
#               | ( related['end_time']>=datetime(2020,2,8,0,0,0)))])
# 计算日期范围的总天数
total_days = (end_time - start_time).days

# 计算每个部分的天数
days_per_section = total_days // 82

# 分割日期范围
date_sections = [start_time + timedelta(days=i * days_per_section) for i in range(82)]
for section_start_date, section_end_date in zip(date_sections, date_sections[1:]):
    print(f"From {section_start_date.strftime('%Y-%m-%d %H:%M:%S')} to {section_end_date.strftime('%Y-%m-%d %H:%M:%S')}")
    related_part=get_range(section_start_date,section_end_date)
    titles=related_part['title']
    title = ""
    for i in titles:
        i = i + '。'
        title += i;
#序列标注
    doc = nlp(title)
    # 遍历每个标题
    tokens = []
    for token in doc:
        if token.pos_ == "NOUN":
            tokens.append(token.text)
    noun_frequencies = Counter(tokens)

    # 找出前10个最常见的名词
    top_nouns = noun_frequencies.most_common(5)
    # print(top_nouns)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    locations = [ent.text for ent in doc.ents if (ent.label_=="GPE")]#ent.label_ == "LOC" or ent.label_ == "GPE" or ent.label_ == "FAC"
    organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]

    location_counts = Counter(locations)

    # 获取最高频的五个地理位置
    top_ten_locations = location_counts.most_common(10)

    # print("Persons:", persons)
    print("Locations:", top_ten_locations)
    # print("Organizations:", organizations)