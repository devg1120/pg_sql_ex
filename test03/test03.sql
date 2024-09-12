CREATE TABLE departments (
    id VARCHAR(31) PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE employees (
    id VARCHAR(31) PRIMARY KEY,
    department_id VARCHAR(31) NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE body_measurements (
    id VARCHAR(31) PRIMARY KEY,
    height INTEGER,
    weight INTEGER
);

CREATE TABLE users (
    id VARCHAR(31) PRIMARY KEY,
    name TEXT NOT NULL,
    body_measurement_id VARCHAR(31) NOT NULL UNIQUE,
    FOREIGN KEY (body_measurement_id) REFERENCES body_measurements(id)
);



CREATE TABLE user_groups (
    id VARCHAR(31) PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE user_user_group_relations (
    user_id VARCHAR(31) NOT NULL,
    user_group_id VARCHAR(31) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (user_group_id) REFERENCES user_groups(id)
);

