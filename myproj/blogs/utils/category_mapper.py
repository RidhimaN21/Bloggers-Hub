def detect_category(title, content=""):
    text = f"{title} {content}".lower()
    
    category_map = {
        "artificial intelligence": "AI",
        "machine learning": "ML",
        "data science": "Data Science",
        "education": "Education",
        "technology": "Technology",
        "health": "Health",
        "finance": "Finance",
        "sports": "Sports",
        "travel": "Travel",
    }

    for keyword, category in category_map.items():
        if keyword in text:
            return category

    return "General"
