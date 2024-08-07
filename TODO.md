Next issue:
- Deal with null tokens, and clear terminal after set-token
- Change settings to BaseModel with own methods to CRUD settings data

Priority:
- Implement all basic commands
- Define most efficient and scalable way of dealing with null token
- Re-design approach to saving items, and if REDIS should be used instead with hash_name
    - First, focus on the most basic operations (buy, sell, get prices, update prices, etc.)
    - When complete, use this package to expand on it
- Add more success & failure codes for user & request functions
- On first connection attempt, throw errors if failed
- Improve command embeddings

Improvements:
- Add a tags table, link to asset_id from items_static
  (should be populated along with db_populate_items_static simultaneously)
- Write formal unit tests, and create one which does:
  - Opens an order for an item and cancels the order for the item (add delays and in-between checks)
- Default value for functions (get_items_static_data, get_items_variable_data)
- Add class docstrings
- Add colours
- Put duplicated code in helper util directory
- Start caching with database
