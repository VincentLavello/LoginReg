
USE REST;
CREATE TABLE IF NOT EXISTS Users (
user_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(45),
last_name VARCHAR(45),
email VARCHAR(60),
created_at DATETIME,
updated_at DATETIME
);
CREATE TABLE IF NOT EXISTS REST.user_notes (
user_id INT NOT NULL PRIMARY KEY, 
memo MEDIUMTEXT,
INDEX User_id_idx (User_id ASC),
CONSTRAINT User_id FOREIGN KEY (User_id)
REFERENCES REST.Users(User_id)
ON DELETE CASCADE
);
INSERT INTO users (first_name, last_name, email, created_at) 
values("Vince", "Lavello", "VincentLavello@gmail.com", Now());
INSERT INTO users (first_name, last_name, email, created_at) 
values("Sharon", "Lavello", "SharonLavello@icloud.com", Now());
INSERT INTO users (first_name, last_name, email, created_at) 
values("Michael", "Lavello", "MichaelLavello714@gmail.com", Now());
INSERT INTO users (first_name, last_name, email, created_at) 
values("Brandon", "Lavello", "Blavello@icloud.com", Now());
INSERT INTO users (first_name, last_name, email, created_at) 
values("Wayne", "Dojo", "wayne@codingdojo.com", Now());
INSERT INTO users (first_name, last_name, email, created_at) 
values("Armin", "Dojo", "Armin@codingdojo.com", Now());
INSERT INTO users (first_name, last_name, email, created_at) 
values("Alex", "Dojo", "Alex@codingdojo.com", Now());
INSERT INTO users (first_name, last_name, email, created_at) 
values("Donavon", "Sensei-Ninja-Dojo", "Donavon@codingdojo.com", Now());
INSERT INTO users (first_name, last_name, email, created_at) 
values("Carlos", "Dojo", "Carlos@codingdojo.com", Now());
INSERT INTO users (first_name, last_name, email, created_at) 
values("Clair", "Ninja-Dojo", "Clair@codingdojo.com", Now());