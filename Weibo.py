#!env python3
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta

# preprocessing
# read, rename, dropna
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

# return rows with date in [start, end]
def get_range(start, end):
    return df[(df["start_time"] >= start) & (df["start_time"] <= end)]

# end_time should be rather useless
min_st = df["start_time"][0]
max_st = df["start_time"][df.index.size - 1]

interval = 10  # day
sub_data = []
cur_st = min_st
while cur_st < max_st:
    ret = get_range(cur_st, cur_st + timedelta(days=interval))
    sub_data.append(ret)
    cur_st += timedelta(days=interval)


