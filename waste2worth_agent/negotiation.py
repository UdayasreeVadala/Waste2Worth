def evaluate_offer(offer, supplier_rules):
    if not offer:
        return False

    price_ok = offer["total_price"] >= supplier_rules.minimum_total_price
    pickup_ok = (not supplier_rules.requires_pickup) or offer["pickup_included"]
    return price_ok and pickup_ok


def build_counter_offer(supplier_rules):
    return {
        "total_price": supplier_rules.minimum_total_price,
        "pickup_included": supplier_rules.requires_pickup,
    }
