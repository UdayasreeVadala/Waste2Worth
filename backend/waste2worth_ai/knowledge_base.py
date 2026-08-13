WASTE_KNOWLEDGE = {
    "tomato": {
        "display_name": "Tomato waste",
        "category": "Organic waste",
        "properties": ["high moisture", "biodegradable", "low dry matter"],
        "suitable_uses": ["anaerobic_digestion", "composting"],
        "limitations": ["Spoilage makes it unsuitable for human consumption."],
    },
    "onion": {
        "display_name": "Onion waste",
        "category": "Organic waste",
        "properties": ["high moisture", "biodegradable", "strong sulfur aroma"],
        "suitable_uses": ["composting", "anaerobic_digestion"],
        "limitations": ["Strong aroma may need managed handling and aeration."],
    },
    "potato": {
        "display_name": "Potato waste",
        "category": "Organic waste",
        "properties": ["starchy", "biodegradable", "high moisture"],
        "suitable_uses": ["anaerobic_digestion", "composting"],
        "limitations": ["Spoiled loads may have fungal contamination."],
    },
    "banana": {
        "display_name": "Banana waste",
        "category": "Organic waste",
        "properties": ["sugar rich", "high moisture", "biodegradable"],
        "suitable_uses": ["anaerobic_digestion", "composting"],
        "limitations": ["Rind and stalk need size reduction for fast processing."],
    },
    "mango": {
        "display_name": "Mango waste",
        "category": "Organic waste",
        "properties": ["sugar rich", "high moisture", "biodegradable"],
        "suitable_uses": ["anaerobic_digestion", "composting"],
        "limitations": ["Stone content reduces composting digestibility."],
    },
    "citrus": {
        "display_name": "Citrus waste",
        "category": "Organic waste",
        "properties": ["high moisture", "acidic", "biodegradable"],
        "suitable_uses": ["composting", "anaerobic_digestion"],
        "limitations": ["Acidic oils may slow microbial activity at high load."],
    },
    "grain": {
        "display_name": "Grain waste",
        "category": "Organic waste",
        "properties": ["starchy", "dry matter", "nutrient rich"],
        "suitable_uses": ["composting", "anaerobic_digestion", "biochar"],
        "limitations": ["Check for spoilage before routing."],
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
    "crop": {
        "display_name": "Crop residue",
        "category": "Agricultural organic waste",
        "properties": ["dry matter", "biodegradable", "voluminous"],
        "suitable_uses": ["composting", "biochar", "anaerobic_digestion"],
        "limitations": ["Dry material may need moisture addition for rapid composting."],
    },
    "organic": {
        "display_name": "Organic waste",
        "category": "Organic waste",
        "properties": ["biodegradable", "variable moisture"],
        "suitable_uses": ["composting", "anaerobic_digestion", "vermicomposting"],
        "limitations": ["Verify composition before final routing."],
    },
    "other": {
        "display_name": "Organic waste",
        "category": "Organic waste",
        "properties": ["biodegradable"],
        "suitable_uses": ["composting", "anaerobic_digestion"],
        "limitations": ["Waste composition should be verified before final routing."],
    },
}


PROCESSING_ROUTES = {
    "anaerobic_digestion": {
        "label": "Anaerobic digestion",
        "buyer_keywords": ["biogas", "anaerobic", "digestion", "energy"],
        "fit_properties": ["high moisture", "sugar rich", "starchy"],
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
        "label": "Biochar production",
        "buyer_keywords": ["biochar", "pyrolysis"],
        "fit_properties": ["dry", "dry matter", "woody"],
    },
}