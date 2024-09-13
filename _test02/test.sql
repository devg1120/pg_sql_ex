CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
);
 
CREATE TABLE posts (
    id INT PRIMARY KEY,
    user_id INT,
    title VARCHAR(200) NOT NULL,
    body TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
