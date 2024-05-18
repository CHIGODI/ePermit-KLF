-- prepares a MySQL server for the ePermit app

CREATE DATABASE IF NOT EXISTS epermit_dev_db;

CREATE USER IF NOT EXISTS 'epermit_dev' @'localhost' IDENTIFIED BY 'epermit_pwd';

GRANT ALL PRIVILEGES ON `epermit_dev_db`.* TO 'epermit_dev' @'localhost';

GRANT SELECT ON `performance_schema`.* TO 'epermit_dev' @'localhost';

FLUSH PRIVILEGES;