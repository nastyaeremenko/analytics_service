def movie_rating_pipeline(movie_id: str) -> list:
    return [
        {
            "$match": {"movie_uuid": movie_id}
        },
        {
            "$project": {
                "movie_uuid": 1,
                "rating": 1,
                "equal0": {
                    "$cond": [{"$eq": ["$rating", 0]}, 1, 0]
                },
                "equal10": {
                    "$cond": [{"$eq": ["$rating", 10]}, 1, 0]
                }
            }
        },
        {
            "$group": {
                "_id": "$movie_uuid",
                "movie_uuid": {"$first": "$movie_uuid"},
                "like": {"$sum": "$equal10"},
                "dislike": {"$sum": "$equal0"},
                "rating": {"$avg": "$rating"}
            }
        }
    ]
