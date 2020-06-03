#!/usr/bin/env python
# This product includes GeoLite2 data created by MaxMind, available from
# https://dev.maxmind.com/geoip/geoip2/geolite2/

import pandas as pd
import argparse
import psycopg2
import os
import shutil
import glob
from ua_parser import user_agent_parser as uap
import geoip2.database
from sql_queries import query_list, query_name_list
from sqlalchemy import create_engine

reader = geoip2.database.Reader('./GeoLite2-City_20200526/GeoLite2-City.mmdb')
pd.options.mode.chained_assignment = None  # default='warn'


def stdout_process(cur):
    """Returns questions for assessment from postgres db
    Parameters:
        cur (psycopg2.cursor()): yieldifydb database cursor
    Returns:
        Tuple('country', 'city')
    """
    for index, query in enumerate(query_list, start=0):
        print('\n')
        print(query_name_list[index] + ': ')
        cur.execute(query)
        result = cur.fetchall()
        for i in result:
            print(i)


def get_country_city(row):
    """For each ip address by row, returns a tuple with country city as values
    Parameters:
        row (row object): row to process
    Returns:
        Tuple('country', 'city')
    """
    try:
        if reader.city(row):
            return reader.city(row).country.name, reader.city(row).city.name
        else:
            return 'N/A'
    except ValueError:
        return None


def process_input(datafile, archive_path, database):
    """Reads files into a dataframe and extract and add country, city & user agent parsing.
        Write data frame to Postgres DB.
    Parameters:
        datafile (str): data file to ingest and process
        archive_path (str): full filepath drop location for processed file(s)
    Returns:
        None
        Side effect: write to Postgres DB
    """
    df = pd.read_csv(datafile, compression='gzip', names=['date', 'time', 'user_id', 'url', 'ip', 'user_agent'],
                     header=None, sep='\t')

    df = df[:1000]
    df['parsed'] = df['user_agent'].apply(lambda x: uap.Parse(x))
    df_parsed = (pd.json_normalize(df['parsed']))
    df_parsed[['country', 'city']] = pd.DataFrame(df['ip'].apply(lambda x: get_country_city(x)).to_list())

    # combine data frames
    df_combined = df.join(df_parsed)

    # normalise column names
    df_combined.columns = df_combined.columns.str.replace(".", "_")
    # print(df_combined)

    log_df = df_combined[['date', 'time', 'user_id', 'url', 'ip', 'user_agent_family', 'os_family',
                          'device_family', 'device_brand', 'device_model', 'country', 'city']]

    # log_df = df_combined[['date', 'time', 'hash',  'country', 'city']]

    engine = create_engine(f'postgresql+psycopg2://localhost:5432/{database}')
    log_df.to_sql('logs', con=engine, if_exists='append', chunksize=10000, index=False)

    shutil.move(datafile, archive_path)
    print('\n')
    print(f'"{datafile}"   >>>   ./archive')

    return None


def process_data(conn, filepath, archivepath, database):
    """Reads all files nested under filepath processing all gzip files found.
    Parameters:
        conn (psycopg2.connect()): connection to the yieldifydb database
        filepath (str): full filepath of the file(s) to be processed
        archivepath (str): full filepath drop location for processed file(s)
    Returns:
        None
        Side effect: Name of files processed to CLI
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.gz'))
        for file in files:
            all_files.append(os.path.abspath(file))

    # get total number of files found
    num_files = len(all_files)
    print('{} file(s) found in {}'.format(num_files, filepath))

    if all_files:
        # iterate over files and process
        for i, datafile in enumerate(all_files, 1):
            process_input(datafile, archivepath,database)
            print('{}/{} files processed.'.format(i, num_files))

        conn.commit()

    return None


def main():
    """Function used to load the extracted and transformed data from the gzip file(s) into a PostgreSQL database
        Usage: python etl.py
    """
    parser = argparse.ArgumentParser(description='Optional arguments to customise input process')
    parser.add_argument("--directory", default="data/", type=str, help="Directory which hosts .gz files to process.")
    parser.add_argument("--archive", default="archive/", type=str, help="Archive folder for processed file(s).")
    parser.add_argument("--database", default="yieldifydb",choices=["yieldifydb", "yieldifydb_test"],
                        type=str, help="Database to use.")
    args = parser.parse_args()
    file_path = args.directory
    data_base = args.database
    archive_path = args.archive

    conn = psycopg2.connect("host=127.0.0.1 dbname=yieldifydb")
    cur = conn.cursor()

    process_data(conn, file_path, archive_path, data_base)
    stdout_process(cur)
    conn.close()


if __name__ == "__main__":
    main()
