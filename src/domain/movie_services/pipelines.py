def movie_rating_pipeline(movie_id: str) -> list:
    return [
        {
            "$match": {"movie_uuid": movie_id}
        },
        {
            "$project": {
                "movie_uuid": 1,
                "id": 1,
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
                "id": {"$first": "$_id"},
                "like": {"$sum": "$equal10"},
                "dislike": {"$sum": "$equal0"},
                "rating": {"$avg": "$rating"}
            }
        }
    ]


def review_rating_pipeline(movie_id: str, sorting: dict) -> list:
    pipeline = [
        {
            "$match": {"movie_uuid": movie_id}
        },
        {
            "$lookup": {
                "from": "rating",
                "localField": "_id",
                "foreignField": "review_id",
                "pipeline": [
                    {
                        "$project": {
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
                            "like": {"$sum": "$equal10"},
                            "dislike": {"$sum": "$equal0"},
                        }
                    }
                ],
                "as": "ratings"
            }
        }
    ]
    if sorting['sort_field']:
        order = 1 if sorting['sort_order'] else -1
        pipeline.append({"$sort": {sorting['sort_field']: order}})
    return pipeline
