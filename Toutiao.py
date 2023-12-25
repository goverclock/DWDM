import pandas as pd
from datetime import datetime as dt

# preprocessing
# read, rename, dropna

df = pd.read_csv("data/Douyin_2020Coron.csv")
df = df.rename(
    columns={
        "date": "start_time",
        "Coron-Related ( 1 yes, 0 not ) ": "is_related",
    }
)
df = df[["start_time", "title", "rank", "words_list", "is_related"]]
dt_format = "%Y-%m-%d"
df["start_time"] = df["start_time"].str.replace("/", "-")
df["start_time"] = pd.to_datetime(df["start_time"], format=dt_format)
df['is_related'].fillna(0, inplace=True)
df = df.dropna()  # x rows valid data

df = df.sort_values(by="start_time")
df = df.reset_index().drop("index", axis=1)

related = df[df["is_related"] != 0]
print(related)
print(df)


def get_range(start, end):
    return df[(df["start_time"] > start) & (df["end_time"] <= end)]
