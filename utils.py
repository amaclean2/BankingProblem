prices = {
    "land": 1,
    "wheat": 1,
    "bread": 1,
    "strawberry": 1
}

qty_to_make_products = {
    "land": {
        "total": 0
    },
    "wheat": {
        "total": 0
    },
    "bread": {
        "total": 0
    },
    "strawberry": {
        "total": 0
    }
}

def add_qty_to_make_products(resource, product, qty):
    qty_resource = qty_to_make_products[resource]

    if product not in list(qty_resource):
        qty_resource[product] = qty
    
    elif qty_resource[product] != qty:
        qty_resource[product] = qty

    total = 0
    for product_name, qty in qty_resource.items():
        total += qty

    qty_resource["total"] = total