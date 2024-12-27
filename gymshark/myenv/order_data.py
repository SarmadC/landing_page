from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import random

# Load data
products_df = pd.read_csv('utf8_file.csv')
customer_df = pd.read_csv('customer.csv')

def generate_order_data(num_orders):
    current_date = datetime.now()
    orders = []
    for i in range(num_orders):
        order_id = f"ORD-{i+1:06d}"
        
        # Select a random customer and get their shipping information
        customer = customer_df.sample().iloc[0]
        customer_id = customer['customer_id']
        shipping_address = customer['address']
        shipping_city = customer['city']
        shipping_state = customer['state']
        shipping_postal_code = customer['postal_code']
        
        order_date = current_date - timedelta(days=random.randint(0, 365))
        num_items = random.randint(1, 5)
        order_items = []
        total_amount = 0
        for _ in range(num_items):
            product = products_df.sample().iloc[0]
            quantity = random.randint(1, 3)
            price = product['current_price']
            item_total = quantity * price
            total_amount += item_total
            order_items.append({
                'product_id': product['product_id'],
                'quantity': quantity,
                'price': price,
                'item_total': item_total
            })
        discount = round(random.uniform(0, 0.2) * total_amount, 2)
        final_amount = total_amount - discount
        shipping_method = random.choice(['Standard', 'Express', 'Next Day'])
        shipping_cost = round(random.uniform(5, 20), 2)
        orders.append({
            'order_id': order_id,
            'customer_id': customer_id,
            'order_date': order_date,
            'items': order_items,
            'total_amount': total_amount,
            'discount': discount,
            'final_amount': final_amount,
            'shipping_method': shipping_method,
            'shipping_cost': shipping_cost,
            'shipping_address': shipping_address,
            'shipping_city': shipping_city,
            'shipping_state': shipping_state,
            'shipping_postal_code': shipping_postal_code
        })
    return orders

# Generate order data
num_orders = 1000
order_data = generate_order_data(num_orders)

# Convert to DataFrame
orders_df = pd.DataFrame(order_data)

# Extract order items into a separate DataFrame
order_items_df = pd.DataFrame([
    dict(order_id=order['order_id'], **item)
    for order in order_data
    for item in order['items']
])

# Remove 'items' column from orders_df as it's now in order_items_df
orders_df = orders_df.drop('items', axis=1)

# Save to CSV
orders_df.to_csv('orders.csv', index=False)
order_items_df.to_csv('order_items.csv', index=False)

print("Orders data saved to 'orders.csv'")
print("Order items data saved to 'order_items.csv'")
print(orders_df.head())
print(order_items_df.head())