CREATE TABLE items_inventory (
    asset_id INT PRIMARY KEY,
    class_ids JSON,
    count INT
);

CREATE TABLE items_static (
    asset_id INT PRIMARY KEY,
    name VARCHAR(80),
    hash_name VARCHAR(80)
);

CREATE TABLE items_variable (
    asset_id INT PRIMARY KEY,
    price_buy FLOAT,
    price_sell FLOAT,
    quantity_buy INT,
    quantity_sell INT,
    profit FLOAT, roi INT,
    timestamp TIMESTAMP
);
