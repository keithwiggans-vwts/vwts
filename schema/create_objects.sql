/*
We'll use geometry for spatial storage.
The accuracy we give up with geography will be made up with the speed of geometry.
Also, not many queries will be looking at finding all entities in the world or within multiple nations.
Those queries should work with geometry well enough anyway.
*/

-- extensions

CREATE EXTENSION IF NOT EXISTS postgis;

-- Create schemas

CREATE SCHEMA IF NOT EXISTS secure;

-- Create tables

DROP TABLE IF EXISTS entity;
CREATE TABLE entity (
  entity_id SERIAL PRIMARY KEY,
  entity_parent_id INTEGER NULL,
  entity_type_id INTEGER NOT NULL,
  entity_isic_id INTEGER NOT NULL,
  entity VARCHAR(255) NOT NULL,
  geom GEOMETRY
);
/* ISIC Codes
 https://ilostat.ilo.org/methods/concepts-and-definitions/classification-economic-activities/
 https://api.isic-archive.com/api/docs/swagger/
*/

DROP TABLE IF EXISTS subscription;
CREATE TABLE subscription (
  subscription_id SERIAL PRIMARY KEY,
  entity_id INTEGER REFERENCES entity(entity_id),
  subscription_level_id INTEGER REFERENCES subscription_level(subscription_level_id),
  subscription_duration_id INTEGER  REFERENCES subscription_duration(subscription_duration_id),
  subscription_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  subscription_end TIMESTAMP
);

DROP TABLE IF EXISTS subscription_level;
CREATE TABLE subscription_level (
  subscription_level_id SERIAL PRIMARY KEY,
  subscription_level VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS subscription_duration;
CREATE TABLE subscription_duration (
  subscription_duration_id SERIAL PRIMARY KEY,
  subscription_duration INTEGER NOT NULL,
  subscription_period VARCHAR(255) NOT NULL -- MONTH/YEAR/LIFE
);

DROP TABLE IF EXISTS donation;
CREATE TABLE donation (
  donation_id SERIAL PRIMARY KEY,
  donation_note VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS secure.contact;
CREATE TABLE pii.contact (
  contact_id SERIAL PRIMARY KEY,
  entity_id INTEGER REFERENCES entity(entity_id),
  contact VARCHAR(255) NULL,
  post_address_1 VARCHAR(255) NULL,
  post_address_2 VARCHAR(255) NULL,
  post_address_3 VARCHAR(255) NULL,
  post_address_4 VARCHAR(255) NULL,
  post_address_5 VARCHAR(255) NULL,
  voice VARCHAR(255) NULL,
  email VARCHAR(255) NULL,
  msg VARCHAR(255) NULL,
  use_post_address BOOLEAN NULL DEFAULT 0,
  use_voice BOOLEAN NULL DEFAULT 0,
  use_email BOOLEAN NULL DEFAULT 0,
  use_msg BOOLEAN NULL DEFAULT 0,
  preferred BOOLEAN NULL DEFAULT 0,
  active BOOLEAN NULL DEFAULT 1,
);

DROP TABLE IF EXISTS secure.order;
CREATE TABLE pii.order (
  order_id SERIAL PRIMARY KEY,
  entity_id INTEGER REFERENCES entity(entity_id),
  subscription_id INTEGER REFERENCES subscription(subscription_id),
  donation_id INTEGER REFERENCES donation(donation_id),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total_amount DECIMAL(10,2) NOT NULL,
  currency CHAR(3) NOT NULL DEFAULT 'USD',  -- Can be adjusted based on your supported currencies
  payment_status VARCHAR(255) NOT NULL,  -- (e.g., pending, success, failed)
  payment_method VARCHAR(255),  -- (e.g., Visa, Mastercard, other generic identifier)
  payment_token VARCHAR(255),  -- Optional, for storing tokenized payment information
);


CREATE TABLE waste_stream (
  waste_stream_id SERIAL PRIMARY KEY,
  business_id INTEGER NOT NULL REFERENCES business(business_id),
  waste_type VARCHAR(255) NOT NULL,
  annual_quantity INTEGER NOT NULL,
  units VARCHAR(255), -- Can be weight (lbs, tons), volume (gallons, cubic yards), etc.
  collection_frequency VARCHAR(255), -- Daily, Weekly, Bi-weekly, etc. 
  special_handling_instructions TEXT
);

-- Optional table for associating waste streams with specific materials

CREATE TABLE waste_stream_material (
  waste_stream_id INTEGER NOT NULL REFERENCES waste_stream(waste_stream_id),
  material_name VARCHAR(255) NOT NULL,
  percentage INTEGER NOT NULL,
  PRIMARY KEY (waste_stream_id, material_name)
);
