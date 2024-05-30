-- prepares a MySQL server for the ePermit app

CREATE DATABASE IF NOT EXISTS epermit_dev_db;

CREATE USER IF NOT EXISTS 'epermit_dev' @'localhost' IDENTIFIED BY 'epermit_pwd';

GRANT ALL PRIVILEGES ON `epermit_dev_db`.* TO 'epermit_dev' @'localhost';

GRANT SELECT ON `performance_schema`.* TO 'epermit_dev' @'localhost';

FLUSH PRIVILEGES;


use epermit_dev_db;


DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS users (
    `id` VARCHAR(60) NOT NULL PRIMARY KEY,
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    email VARCHAR(128) NOT NULL UNIQUE,
    password VARCHAR(512) NOT NULL,
    first_name VARCHAR(60),
    last_name VARCHAR(60),
    ID_number INTEGER,
    gender VARCHAR(20),
    designation VARCHAR(60),
    phone_number VARCHAR(20),
    role VARCHAR(6),
    UNIQUE (id)
);

DROP TABLE IF EXISTS `categories`;


-- Create the categories table based on the model
CREATE TABLE IF NOT EXISTS categories (
    `id` varchar(60) NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activity_code VARCHAR(8) PRIMARY KEY,
    category_name VARCHAR(128) NOT NULL,
    description VARCHAR(256),
    fee FLOAT NOT NULL,
    fire_fee FLOAT NOT NULL,
    INDEX (id)
);

-- Create the categories table based on the model
-- Insert activity codes and descriptions
INSERT INTO categories (id, created_at, updated_at, activity_code, category_name, description, fee, fire_fee) VALUES
('6090e5d1-cc0b-4b0d-8e6f-f8c8a2f5b8db', '2024-05-24 15:30:00', '2024-05-24 15:30:01', '0111', 'Growing of cereals (except rice), leguminous crops and oil seeds', 'Agriculture and farming activities', 1000.0, 200.0),
('90a6c6fb-0d6f-443e-a5bf-8b401e617f35', '2024-05-24 15:30:02', '2024-05-24 15:30:03', '0141', 'Raising of cattle and buffaloes', 'Livestock farming activities', 1500.0, 300.0),
('febc59d7-3f85-4b17-8248-eb4c7e8a8dd6', '2024-05-24 15:30:04', '2024-05-24 15:30:05', '0311', 'Marine fishing', 'Fishing activities in marine waters', 2000.0, 400.0),
('8a37b4e1-c437-4f40-931e-35417d78e034', '2024-05-24 15:30:06', '2024-05-24 15:30:07', '0321', 'Marine aquaculture', 'Farming of aquatic organisms in marine waters', 2500.0, 500.0),
('57f1b2cc-d04d-45f0-8346-5c5e8e37b049', '2024-05-24 15:30:08', '2024-05-24 15:30:09', '0510', 'Mining of hard coal', 'Extraction of coal from underground or surface mining', 3000.0, 600.0),
('60bbd5f1-2681-477b-9d43-057ed51d4b25', '2024-05-24 15:30:10', '2024-05-24 15:30:11', '0710', 'Mining of iron ores', 'Extraction of iron ores from mining activities', 3500.0, 700.0),
('af7df0e1-9d8c-448b-92cf-7fc9c4fd2041', '2024-05-24 15:30:12', '2024-05-24 15:30:13', '0891', 'Mining of chemical and fertilizer minerals', 'Extraction of minerals used for chemicals and fertilizers', 4000.0, 800.0),
('6d79e2e8-cd0e-42b8-a07b-4ef64e4423ff', '2024-05-24 15:30:14', '2024-05-24 15:30:15', '0990', 'Support activities for other mining and quarrying', 'Services related to mining and quarrying', 4500.0, 900.0),
('3e8ec4a2-c5aa-49f0-b114-2892b23c4c0e', '2024-05-24 15:30:16', '2024-05-24 15:30:17', '1010', 'Processing and preserving of meat', 'Meat processing and preservation activities', 5000.0, 1000.0),
('b759f9b9-6b83-4892-b9e4-2d9fcfda90b5', '2024-05-24 15:30:18', '2024-05-24 15:30:19', '1072', 'Manufacture of sugar', 'Production and manufacturing of sugar', 5500.0, 1100.0),
('04ad06f7-7d6e-4b6d-bcba-0076565fe3d7', '2024-05-24 15:30:20', '2024-05-24 15:30:21', '1410', 'Manufacture of wearing apparel, except fur apparel', 'Production of clothing and garments', 6000.0, 1200.0),
('72c2eecd-888f-4b8d-8e4e-c7af7a77f42a', '2024-05-24 15:30:22', '2024-05-24 15:30:23', '1701', 'Manufacture of pulp, paper, and paperboard', 'Production of paper and paper products', 6500.0, 1300.0),
('896122b0-6762-46eb-a011-6a6542a9e3cf', '2024-05-24 15:30:24', '2024-05-24 15:30:25', '3510', 'Electric power generation, transmission, and distribution', 'Generation and distribution of electricity', 7000.0, 1400.0),
('d360a8ec-0344-45da-863e-593c5bb9d168', '2024-05-24 15:30:26', '2024-05-24 15:30:27', '3520', 'Manufacture of gas; distribution of gaseous fuels through mains', 'Production and distribution of gas', 7500.0, 1500.0),
('d203e971-d9e3-47e2-8ff3-0b1403b7dd7c', '2024-05-24 15:30:28', '2024-05-24 15:30:29', '3530', 'Steam and air conditioning supply', 'Provision of steam and air conditioning', 8000.0, 1600.0),
('d4c314d5-0c38-4b59-b5e2-3acdb16f2b45', '2024-05-24 15:30:30', '2024-05-24 15:30:31', '3600', 'Water collection, treatment, and supply', 'Water supply and treatment services', 8500.0, 1700.0),
('5e5b6195-af19-4bc5-ba0a-d3f267cb1971', '2024-05-24 15:30:32', '2024-05-24 15:30:33', '3700', 'Sewerage', 'Sewerage and wastewater management services', 9000.0, 1800.0),
('c253a854-2a48-4cbf-aad2-85992d87b3bf', '2024-05-24 15:30:34', '2024-05-24 15:30:35', '3811', 'Collection of non-hazardous waste', 'Collection and management of non-hazardous waste', 9500.0, 1900.0),
('16b9788e-299b-4a27-943f-7325e8b5c975', '2024-05-24 15:30:36', '2024-05-24 15:30:37', '3900', 'Remediation activities and other waste management services', 'Environmental remediation and waste management', 10000.0, 2000.0),
('dbf700a1-674b-4d43-af34-61dbdf84aa94', '2024-05-24 15:30:38', '2024-05-24 15:30:39', '4110', 'Development of building projects', 'Real estate development and construction', 10500.0, 2100.0),
('c0c86e3d-1355-4c0e-a5a1-95ab96fb6fd4', '2024-05-24 15:30:40', '2024-05-24 15:30:41', '4210', 'Construction of roads and railways', 'Infrastructure construction activities', 11000.0, 2200.0),
('03a54c1c-62b0-4d6b-bd20-5182d0e02bc4', '2024-05-24 15:30:42', '2024-05-24 15:30:43', '4311', 'Demolition', 'Demolition and site preparation services', 11500.0, 2300.0),
('fac3f69f-147f-4cc3-a588-aa54df39431f', '2024-05-24 15:30:44', '2024-05-24 15:30:45', '4390', 'Other specialized construction activities', 'Specialized construction services', 12000.0, 2400.0),
('d5825b58-9ae2-4cb9-a5ec-2b3b6d1e91d3', '2024-05-24 15:30:46', '2024-05-24 15:30:47', '4510', 'Sale of motor vehicles', 'Retail sale of motor vehicles', 12500.0, 2500.0),
('f24081b1-0a88-42d5-a4e4-eb49b2f5c330', '2024-05-24 15:30:48', '2024-05-24 15:30:49', '4520', 'Maintenance and repair of motor vehicles', 'Vehicle maintenance and repair services', 13000.0, 2600.0),
('e89e54f2-e1b0-47a9-8c7e-872b62e250ee', '2024-05-24 15:30:50', '2024-05-24 15:30:51', '4711', 'Retail sale in non-specialized stores with food, beverages or tobacco predominating', 'Retail services in general stores', 1.0, 1.0),
('c469049e-5dc8-4222-91cc-319dbbdf38b9', '2024-05-24 15:30:52', '2024-05-24 15:30:53', '4791', 'Retail sale via mail order houses or via Internet', 'Online and mail order retail sales', 14000.0, 2800.0),
('f03536f7-c54d-4978-a5b3-51d98615a6ed', '2024-05-24 15:30:54', '2024-05-24 15:30:55', '4911', 'Passenger rail transport, interurban', 'Interurban passenger rail services', 14500.0, 2900.0),
('bfd527c0-0cc2-4a1a-80d5-1e98de39061d', '2024-05-24 15:30:56', '2024-05-24 15:30:57', '5011', 'Sea and coastal passenger water transport', 'Passenger transport via sea and coastal waters', 15000.0, 3000.0),
('c87d218d-6b3b-45f3-877b-f47de42ac6fa', '2024-05-24 15:30:58', '2024-05-24 15:30:59', '5110', 'Passenger air transport', 'Air passenger transport services', 15500.0, 3100.0),
('dd27e905-cf1a-4e1d-98f7-9ab20f6f22ac', '2024-05-24 15:31:00', '2024-05-24 15:31:01', '5221', 'Service activities incidental to land transportation', 'Support services for land transportation', 16000.0, 3200.0),
('d835100b-c71a-4cf7-8df2-c71cfa78b21e', '2024-05-24 15:31:02', '2024-05-24 15:31:03', '5510', 'Short term accommodation activities', 'Short-term lodging services', 16500.0, 3300.0),
('d31cfdf5-5bcf-4489-8d39-3ab16d27a2e9', '2024-05-24 15:31:04', '2024-05-24 15:31:05', '5610', 'Restaurants and mobile food service activities', 'Restaurant and food service operations', 17000.0, 3400.0),
('c024fcf1-e59a-4298-af8e-66b586ad9e34', '2024-05-24 15:31:06', '2024-05-24 15:31:07', '5629', 'Other food service activities', 'Miscellaneous food service activities', 17500.0, 3500.0),
('bd6bf5b7-4d6c-44f1-8d9b-352bd6bf5b74', '2024-05-24 15:31:08', '2024-05-24 15:31:09', '5630', 'Beverage serving activities', 'Beverage service operations', 18000.0, 3600.0),
('aba1ee33-67d1-4f63-95fc-66dd9f0054b7', '2024-05-24 15:31:10', '2024-05-24 15:31:11', '5811', 'Book publishing', 'Publishing of books and related media', 18500.0, 3700.0),
('bdc54c2c-eb3d-45d4-aad4-fbd143d3e0b4', '2024-05-24 15:31:12', '2024-05-24 15:31:13', '5911', 'Motion picture, video and television programme production activities', 'Production of films and television programs', 19000.0, 3800.0),
('3baf2b1b-af82-4a24-800b-9f1fe8ad98db', '2024-05-24 15:31:14', '2024-05-24 15:31:15', '6110', 'Wired telecommunications activities', 'Wired telecommunications services', 19500.0, 3900.0),
('56e7a158-11e4-4be3-8943-9189b2a1f573', '2024-05-24 15:31:16', '2024-05-24 15:31:17', '6312', 'Web portals', 'Operation of web portals and related services', 20000.0, 4000.0),
('d8b21dbd-161f-4d63-9881-e4db97c586f0', '2024-05-24 15:31:18', '2024-05-24 15:31:19', '6411', 'Central banking', 'Central banking operations and services', 20500.0, 4100.0),
('7c4f9d46-833d-42bb-b8e9-2924d02531f2', '2024-05-24 15:31:20', '2024-05-24 15:31:21', '6511', 'Life insurance', 'Life insurance services', 21000.0, 4200.0),
('40b788b1-b678-4ae0-9a9a-af0c5b8270a7', '2024-05-24 15:31:22', '2024-05-24 15:31:23', '6611', 'Administration of financial markets', 'Financial market administration services', 21500.0, 4300.0),
('af3cb2a2-2e7e-4e7e-ae59-435d475b6fd2', '2024-05-24 15:31:24', '2024-05-24 15:31:25', '6810', 'Real estate activities with own or leased property', 'Real estate management and leasing', 22000.0, 4400.0),
('2e1ec055-6bb5-4d91-b58b-12239d7a6895', '2024-05-24 15:31:26', '2024-05-24 15:31:27', '6910', 'Legal activities', 'Legal services and activities', 22500.0, 4500.0),
('3b8d13ff-7d68-48cd-b33e-03af57e4e05f', '2024-05-24 15:31:28', '2024-05-24 15:31:29', '7020', 'Management consultancy activities', 'Business and management consultancy services', 23000.0, 4600.0),
('d7d7c63f-2f7e-4a79-9871-b45643763b21', '2024-05-24 15:31:30', '2024-05-24 15:31:31', '7210', 'Research and experimental development on natural sciences and engineering', 'R&D in natural sciences and engineering', 23500.0, 4700.0),
('f258364f-8659-45e1-b9d2-b0988a5b7220', '2024-05-24 15:31:32', '2024-05-24 15:31:33', '7410', 'Specialized design activities', 'Specialized design services', 24000.0, 4800.0),
('a25da9b4-6be4-47d7-8281-2c6a100cc879', '2024-05-24 15:31:34', '2024-05-24 15:31:35', '7710', 'Renting and leasing of motor vehicles', 'Vehicle rental and leasing services', 24500.0, 4900.0),
('e4d49385-5fd9-4ef1-815c-275981622360', '2024-05-24 15:31:36', '2024-05-24 15:31:37', '7911', 'Travel agency activities', 'Travel agency and tour operator services', 25000.0, 5000.0),
('a9b5bb88-f93c-4db6-91b4-ff03a0a43f2d', '2024-05-24 15:31:38', '2024-05-24 15:31:39', '8010', 'Private security activities', 'Private security services', 25500.0, 5100.0),
('eb6e9dd3-4002-4e89-89d2-e8d90ef0521a', '2024-05-24 15:31:40', '2024-05-24 15:31:41', '8211', 'Combined office administrative service activities', 'Office administrative services', 26000.0, 5200.0),
('3c5c7b22-d6fb-4683-879c-d45dd9da818b', '2024-05-24 15:31:42', '2024-05-24 15:31:43', '8510', 'Pre-primary education', 'Pre-primary educational services', 26500.0, 530);



