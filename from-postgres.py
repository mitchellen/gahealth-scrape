import pandas as pd
import psycopg2
t_host = "localhost" # either "localhost", a domain name, or an IP address.
t_port = "5432" # default postgres port
t_dbname = "cityscrape"
t_user = "scrape"
t_pw = "password"
db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)

df = pd.read_sql_query("SELECT * FROM rest_scores",con=db_conn)
df.head()
