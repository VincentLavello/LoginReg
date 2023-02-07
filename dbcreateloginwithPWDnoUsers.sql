
DROP DATABASE IF EXISTS LoginReg;
DROP TABLE IF EXISTS LoginReg.Users;
CREATE DATABASE LoginReg;
USE LoginReg;
CREATE TABLE Users (
user_id int NOT NULL AUTO_INCREMENT, 
first_name VARCHAR(45),
last_name VARCHAR(45),
email VARCHAR(60),
pwd VARCHAR(120),
created_at DATETIME,
updated_at DATETIME,
PRIMARY KEY(user_id)
);
DROP TABLE IF EXISTS LoginReg.user_notes;
CREATE TABLE LoginReg.user_notes (
user_id INT NOT NULL PRIMARY KEY, 
memo MEDIUMTEXT,
INDEX User_id_idx (User_id ASC),
CONSTRAINT User_id FOREIGN KEY (User_id)
REFERENCES LoginReg.Users(User_id)
ON DELETE CASCADE
);