WASTE_KNOWLEDGE = {
    "tomato": {
        "display_name": "Tomato waste",
        "category": "Organic waste",
        "properties": ["high moisture", "biodegradable", "low dry matter"],
        "suitable_uses": ["anaerobic_digestion", "composting"],
        "limitations": ["Spoilage makes it unsuitable for human consumption."],
    },
    "vegetable": {
        "display_name": "Vegetable waste",
        "category": "Organic waste",
        "properties": ["biodegradable", "nutrient rich", "variable moisture"],
        "suitable_uses": ["composting", "anaerobic_digestion", "vermicomposting"],
        "limitations": ["Mixed loads should be checked for plastic or packaging contamination."],
    },
    "fruit": {
        "display_name": "Fruit waste",
        "category": "Organic waste",
        "properties": ["high moisture", "biodegradable", "sugar rich"],
        "suitable_uses": ["anaerobic_digestion", "composting"],
        "limitations": ["Very wet loads may need bulking material for composting."],
    },
    "food": {
        "display_name": "Food waste",
        "category": "Organic waste",
        "properties": ["mixed organic material", "biodegradable"],
        "suitable_uses": ["anaerobic_digestion", "composting"],
        "limitations": ["Contamination and local handling rules must be checked."],
    },
}


PROCESSING_ROUTES = {
    "anaerobic_digestion": {
        "label": "Anaerobic digestion",
        "buyer_keywords": ["biogas", "anaerobic", "digestion", "energy"],
        "fit_properties": ["high moisture", "sugar rich", "biodegradable"],
    },
    "composting": {
        "label": "Composting",
        "buyer_keywords": ["compost", "organic processor"],
        "fit_properties": ["biodegradable", "nutrient rich"],
    },
    "vermicomposting": {
        "label": "Vermicomposting",
        "buyer_keywords": ["vermicompost", "worm"],
        "fit_properties": ["nutrient rich", "biodegradable"],
    },
    "biochar": {
        "label": "Biochar",
        "buyer_keywords": ["biochar", "pyrolysis"],
        "fit_properties": ["dry", "woody"],
    },
}

