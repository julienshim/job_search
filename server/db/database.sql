DROP DATABASE IF EXISTS job_search;

CREATE DATABASE IF NOT EXISTS job_search;

\c job_search;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS company;

CREATE TABLE IF NOT EXISTS company(
    company_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id_short VARCHAR(155) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    company_url VARCHAR(255) NOT NULL,
    company_locations_string VARCHAR(255), 
    company_careers_page VARCHAR(255),
    company_locations_tags VARCHAR(255)
)

\COPY company(
    company_id_short,
    company_name,
    company_url,
    company_locations_string,
    company_careers_page,
    company_locations_tags
) FROM '/Users/julienshim/Developer/job_search/csv/seed.csv'
DELIMITER ','
CSV HEADER;