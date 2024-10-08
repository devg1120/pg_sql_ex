
--ラーメンの種類
CREATE TABLE RAMEN (
    ramen_id INT PRIMARY KEY,
    name   VARCHAR(50) NOT NULL
);

CREATE TABLE RAMEN_PRICE (
    ramen_id INT PRIMARY KEY,
    price  INT,
    FOREIGN KEY (ramen_id) REFERENCES RAMEN(ramen_id)
);

--トッピング
CREATE TABLE TOPPING (
    --topping_id INT PRIMARY KEY,
    topping_id SERIAL PRIMARY KEY,
    name   VARCHAR(50) NOT NULL,
    size   VARCHAR(50),
    country  VARCHAR(50)
);

CREATE TABLE TOPPING_PRICE (
    topping_id INT PRIMARY KEY,
    price  INT,
    FOREIGN KEY (topping_id) REFERENCES TOPPING(topping_id)
);

--麺の種類
CREATE TABLE TYPE_OF_NOODLE (
    topping_id INT PRIMARY KEY,
    name   VARCHAR(50) NOT NULL
);

--麺の硬さ
CREATE TABLE NOODLE_HARDNESS (
    topping_id INT PRIMARY KEY,
    name   VARCHAR(50) NOT NULL
);

--スープの濃さ
CREATE TABLE SOUP_THICKNESS (
    topping_id INT PRIMARY KEY,
    name   VARCHAR(50) NOT NULL
);

--油の量
CREATE TABLE AMOUNT_OF_OIL (
    topping_id INT PRIMARY KEY,
    name   VARCHAR(50) NOT NULL
);

--油の量
CREATE TABLE SEX (
    sex_id INT PRIMARY KEY,
    name   VARCHAR(50) NOT NULL
);

--顧客
CREATE TABLE CUSTOMER  (
    customer_id SERIAL PRIMARY KEY ,
   --oeder_id integer NOT NULL DEFAULT nextval('seq_table_id_seq'::regclass),
    customer_name   VARCHAR(50) NOT NULL,
    customer_age  INT NOT NULL,
    customer_sex INT,
    FOREIGN KEY (customer_sex) REFERENCES SEX(sex_id)
);


--注文
CREATE TABLE ORDER_LIST (
    order_id BIGSERIAL PRIMARY KEY ,  -- YYYYMMDD$$$
    uuid    UUID,
    ulid    TEXT,
    customer_id INT,
    ramen_id INT,
    fee INT,
    --day TIME,
    day TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
    FOREIGN KEY (ramen_id)    REFERENCES RAMEN(ramen_id)
);

--注文 トッピング
CREATE TABLE ORDER_TOPPING (
    order_id BIGSERIAL ,
    topping_id INT,
    FOREIGN KEY (order_id) REFERENCES ORDER_LIST(order_id),
    FOREIGN KEY (topping_id) REFERENCES TOPPING(topping_id)
);


CREATE SEQUENCE test_sequence
  start 100
  increment 1;

--
CREATE TABLE SQ_TEST (
    --id INT PRIMARY KEY,
    id SERIAL PRIMARY KEY,
    name   VARCHAR(50) NOT NULL,
    value INT
);
