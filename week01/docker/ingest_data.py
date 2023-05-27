#!/usr/bin/env python
# coding: utf:-8

import argparse
import os

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    parquet_name = 'output.parquet'

    os.system(f'wget {url} -O {parquet_name}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    df = pd.read_parquet(parquet_name, engine='fastparquet')

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest Parquet data to Postgres')

    #user, pass, host, port, db name, table name, url
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help=' dbfor postgres')
    parser.add_argument('--table_name', help='name of the table to write the results')
    parser.add_argument('--url', help='url of the parquet file')

    args = parser.parse_args()

    main(args)