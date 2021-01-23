#!/usr/bin/env python

import pandas as pd


df = pd.read_table("./table_reversable.tsv", encoding="shift-jis")
df_tmp = df.copy()
df_tmp[["in_0", "in_1"]] = df[["in_1", "in_0"]]

df = pd.concat([df, df_tmp]).reset_index(drop=True)
df["in"] = df["in_0"] + df["in_1"]
df = df.drop(columns=["in_0", "in_1"])

df_norev = pd.read_table("./table_noreverse.tsv", encoding="shift-jis")
df = pd.concat([df, df_norev]).reset_index(drop=True)[["in", "out"]]

df.to_csv("../朱雀配列.tsv", sep="\t", index=None, header=None, encoding="shift-jis")

print(df)
