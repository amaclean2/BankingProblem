from commodities import qty_to_make_products
import math as m

def add_qty_to_make_products(resource, product, qty):
    qty_resource = qty_to_make_products[resource]

    if product not in list(qty_resource):
        qty_resource[product] = qty
    
    elif qty_resource[product] != qty:
        qty_resource[product] = qty

    total = 0
    for product_name, local_qty in qty_resource.items():
        if product_name != "total":
            total += local_qty

    qty_resource["total"] = total

def round_qties(qt, digit=2):
    return m.floor(qt * 10**digit) / 10**digit

cannot_be_made = [
    "type_three",
    "type_four"
]