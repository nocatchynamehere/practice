list_products = [
    {"name": "apple", "price": 1.2},
    {"name": "banana", "price": 0.5},
    {"name": "cherry", "price": 2.0}
]

def discount_products(products, discount):
    percent_discount = 1 - (discount / 100)

    for i in products:
        i["price"] = i["price"] * percent_discount
    
    print(products)

discount_products(list_products, 10)
