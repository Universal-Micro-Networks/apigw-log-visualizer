CREATE DATABASE metabase_db;
\c metabase_db

CREATE USER metabase_user WITH PASSWORD 'bKLFGfj5' CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE metabase_db TO metabase_user;
GRANT CREATE ON SCHEMA public TO metabase_user;

CREATE DATABASE log_analysis_db;
\c log_analysis_db
--ユーザーにDBの権限をまとめて付与
CREATE USER log_analysis_user WITH PASSWORD 'Fq3MdiTt' CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE log_analysis_db TO log_analysis_user;
CREATE SCHEMA log_analysis AUTHORIZATION log_analysis_user;
