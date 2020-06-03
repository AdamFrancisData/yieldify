# CREATE TABLE

log_table_create = ("""
    CREATE TABLE IF NOT EXISTS logs
    (log_id SERIAL PRIMARY KEY,
    date date NOT NULL,
    time time NOT NULL,
    user_id varchar,
    url varchar,
    ip varchar NULL,
    user_agent_family varchar NULL,
    os_family varchar NULL,
    device_family varchar NULL,
    device_brand varchar NULL,
    device_model varchar NULL,
    country varchar NULL,
    city varchar NULL)
""")



log_table_insert = ("""
    INSERT INTO logs
    (date, time, hash, url, ip, user_agent_family, os_family, device_family, device_brand,device_model,country,city)
    VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s );
""")

create_table_queries = [log_table_create]

top_five_countries_query = ("""
    SELECT 
        country,
        COUNT(*) as cnt_events
    FROM 
        logs
    WHERE 
        country IS NOT NULL
    GROUP BY 
        country
    ORDER BY cnt_events DESC
    LIMIT
    5;
""")

top_five_cites_query = ("""
    SELECT 
        city,
        COUNT(*) as cnt_events
    FROM 
        logs
    WHERE 
        city IS NOT NULL
    GROUP BY 
        city
    ORDER BY cnt_events DESC
    LIMIT
    5;
""")

top_five_browsers_query = ("""
SELECT
    user_agent_family, 
    COUNT(DISTINCT(user_id)) as cnt 
FROM
    logs 
WHERE 
    user_agent_family IS NOT NULL 
GROUP BY  
    user_agent_family 
ORDER BY 
    cnt desc 
LIMIT 
    5;
""")

top_five_os_query = ("""
SELECT
    os_family, 
    COUNT(DISTINCT(user_id)) as cnt 
FROM
    logs 
WHERE 
    os_family IS NOT NULL 
GROUP BY  
    os_family 
ORDER BY 
    cnt desc 
LIMIT 
    5;
""")

query_list = [top_five_countries_query, top_five_cites_query, top_five_browsers_query, top_five_os_query]
query_name_list = ['Top 5 Countries based on number of events',
                   'Top 5 Cities based on number of events',
                   'Top 5 Browsers based on number of unique users',
                   'Top 5 Operating systems based on number of unique users']

brower_with_params = '''SELECT
user_agent_family, 
COUNT(DISTINCT(user_id)) as cnt 
FROM
logs 
WHERE 
user_agent_family IS NOT NULL 
{}
GROUP BY  
user_agent_family 
ORDER BY 
cnt desc 
LIMIT 
5;'''

os_with_params = '''
SELECT
    os_family, 
    COUNT(DISTINCT(user_id)) as cnt 
FROM
    logs 
WHERE 
    os_family IS NOT NULL 
{}
GROUP BY  
    os_family 
ORDER BY 
    cnt desc 
LIMIT 
    5;
'''

device_with_params = '''SELECT
device_family, 
COUNT(DISTINCT(user_id)) as cnt 
FROM
logs 
WHERE 
device_family IS NOT NULL 
{}
GROUP BY  
device_family 
ORDER BY 
cnt desc 
LIMIT 
5;'''
