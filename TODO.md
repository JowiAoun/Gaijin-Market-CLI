Priority:
- Re-design approach to saving items, and if REDIS should be used instead with hash_name
    - First, focus on the most basic operations (buy, sell, get prices, update prices, etc.)
    - When complete, use this package to expand on it
- Add more success & failure codes for user & request functions
- On first connection attempt, throw errors if failed

Improvements:
- Add a tags table, link to asset_id from items_static
  (should be populated along with db_populate_items_static simultaneously)
- Write formal unit tests, and create one which does:
  - Opens an order for an item and cancels the order for the item (add delays and in-between checks)
- Add class docstrings
- Start caching with database
