import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_messy_data(n_rows=5000):
    stores = ['Outdoor Living', 'Home Essentials', 'Green Garden', 'Urban Nest', 'Wilderness Supply']
    categories = ['Furniture', 'Cooking', 'Gardening', 'Tents', 'Lighting']
    
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(n_rows):
        order_id = f"ORD-{1000 + i}"
        #Random missing dates
        date = (start_date + timedelta(days=random.randint(0, 1000))).strftime('%Y-%m-%d') if random.random() > 0.02 else None
        
        #Duplicate Product Naming
        prod_name = "Folding Chair" if random.random() > 0.1 else "Foldable Chair"
        
        data.append({
            "order_id": order_id,
            "order_date": date,
            "customer_email": f"user{random.randint(1,500)}@example.com",
            "product_name": prod_name,
            "category": random.choice(categories),
            "quantity": random.randint(1, 5),
            "price": round(random.uniform(20, 200), 2),
            "store_name": random.choice(stores)
        })
    
    df = pd.DataFrame(data)
    
    # Duplicate Rows
    duplicates = df.sample(n=50)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    df.to_csv("daily_orders.csv", index=False)
    print("Messy data generated: daily_orders.csv")

generate_messy_data()
