def calculate_view_statistics(collection):
    return collection.aggregate([
        {"$group": {
            "_id": None,
            "avgViews": {"$avg": "$views"},
            "maxViews": {"$max": "$views"},
            "minViews": {"$min": "$views"}
        }}
    ])

def calculate_avg_rating_by_category(collection):
    return collection.aggregate([
        {"$group": {
            "_id": "$category",
            "avgRating": {"$avg": "$rate"}
        }}
    ])

def calculate_total_comments_and_ratings_by_category(collection):
    return collection.aggregate([
        {"$group": {
            "_id": "$category",
            "totalComments": {"$sum": "$comments"},
            "totalRatings": {"$sum": "$ratings"}
        }}
    ])
