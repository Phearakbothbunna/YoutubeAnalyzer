'''
Aggregations we have:
    avg, max, min views across entire platform
    avg rating by category
    total comments & rating by category
    avg video length by category 
    top uploaders based on views 
    most commented videos 
    most viewed videos
    most viewed videos in each category 
    avg views on each video per category

'''

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


def calculate_avg_length_by_category(collection):
    return collection.aggregate([
        {"$group": {
            "_id": "$category",
            "avgLength": {"$avg": "$length"}
        }}
    ])


def top_uploader_by_views(collection):
    return collection.aggregate([
        {"$group": {
            "_id": "$uploader",
            "totalViews": {"$sum": "$views"}
        }},
        {"$sort": {"totalViews": -1}},
        {"$limit": 1}
    ])


def top_commented_videos(collection):
    return collection.aggregate([
        {"$sort": {"comments": -1}},
        {"$limit": 5},
        {"$project": {"videoID": 1, "uploader": 1, "category": 1, "comments": 1}}
    ])


def most_viewed_videos(collection, top_n=5):
    return collection.aggregate([
        {"$sort": {"views": -1}},
        {"$limit": top_n},
        {"$project": {"videoID": 1, "views": 1, "uploader": 1, "category": 1}}
    ])


def most_viewed_video_in_each_category(collection):
    return collection.aggregate([
        {"$sort": {"views": -1}},
        {"$group": {
            "_id": "$category",       
            "videoID": {"$first": "$videoID"},
            "uploader": {"$first": "$uploader"},
            "views": {"$first": "$views"},
            "rate": {"$first": "$rate"},
            "comments": {"$first": "$comments"}
        }}
    ])


def avg_views_per_video_by_category(collection):
    return collection.aggregate([
        {"$group": {
            "_id": "$category",
            "avgViews": {"$avg": "$views"}
        }}
    ])
