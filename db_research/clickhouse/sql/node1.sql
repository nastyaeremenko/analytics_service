CREATE DATABASE analytics;

CREATE DATABASE shard;

CREATE DATABASE replica;

CREATE TABLE shard.movie_view (id UInt64, user_uuid String, movie_uuid String, movie_progress UInt64, movie_length UInt64, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/movie_view', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY id;

CREATE TABLE replica.movie_view (id UInt64, user_uuid String, movie_uuid String, movie_progress UInt64, movie_length UInt64, event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/movie_view', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY id;

CREATE TABLE analytics.movie_view (id UInt64, user_uuid String, movie_uuid String, movie_progress UInt64, movie_length UInt64, event_time DateTime) ENGINE = Distributed('company_cluster', '',movie_view, rand());