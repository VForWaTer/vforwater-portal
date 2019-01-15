import pandas as pd
import numpy as np
import psycopg2
df = pd.DataFrame(np.random.randn(1000), columns=['a'])
dates = pd.date_range('2015-01-01 00:00:00', periods=df.shape[0], freq='5MIN').tolist()
df.insert(loc=0, column='date', value=pd.to_datetime(dates))
insert_query = "INSERT INTO tbl_data(meta_id, tstamp, value) VALUES"
for meta_n in range(10):
	for n in range(len(df)):
	    data = " ({}, TIMESTAMP '{}', {}),".format(meta_n+1, df.iloc[n,0], df.iloc[n,1])
	    #data = "(%d, %s, %s)", (1, df.iloc[n,0].tolist(), df.iloc[n,1].tolist())
	    insert_query += str(data)
insert_query = insert_query[:-1]+';'

conn = psycopg2.connect("host='localhost' dbname='vfw_start' user='testuser' password='test'")
cur = conn.cursor()
cur.execute(insert_query)
conn.commit()