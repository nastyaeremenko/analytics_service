from clickhouse_driver import Client

from constants import CH_TABLE_NAME


def create_db():
    client1 = Client('clickhouse-node1')
    init_node(client1, 'shard1', 'shard2')
    client2 = Client('clickhouse-node3')
    init_node(client2, 'shard2', 'shard1')


def init_node(client: Client, shard1: str, shard2: str):
    client.execute("CREATE DATABASE IF NOT EXISTS analytics;")
    client.execute("CREATE DATABASE IF NOT EXISTS shard;")
    client.execute("CREATE DATABASE IF NOT EXISTS replica;")
    path1 = f'/clickhouse/tables/{shard1}/{CH_TABLE_NAME}'
    client.execute(f"""
        CREATE TABLE IF NOT EXISTS shard.{CH_TABLE_NAME} (
            user_uuid String,
            movie_uuid String,
            movie_progress UInt64,
            movie_length UInt64,
            event_time DateTime
        ) Engine=ReplicatedMergeTree(%(path)s, 'replica_1')
        PARTITION BY toYYYYMMDD(event_time)
        ORDER BY movie_uuid;
        """, {'table': 'shard.movie_view',
              'path': path1}
    )
    path2 = f'/clickhouse/tables/{shard2}/{CH_TABLE_NAME}'
    client.execute(f"""
        CREATE TABLE IF NOT EXISTS replica.{CH_TABLE_NAME} (
            user_uuid String,
            movie_uuid String,
            movie_progress UInt64,
            movie_length UInt64,
            event_time DateTime
        ) Engine=ReplicatedMergeTree(%(path)s, 'replica_2')
        PARTITION BY toYYYYMMDD(event_time)
        ORDER BY movie_uuid;
        """, {'table': 'replica.movie_view',
              'path': path2}
    )
    client.execute(f"""
        CREATE TABLE IF NOT EXISTS analytics.{CH_TABLE_NAME} (
            user_uuid String,
            movie_uuid String,
            movie_progress UInt64,
            movie_length UInt64,
            event_time DateTime
        ) ENGINE = Distributed('company_cluster', '', {CH_TABLE_NAME}, rand());
        """, {'table_full': 'analytics.movie_view',
              'table': 'movie_view'}
    )


if __name__ == '__main__':
    create_db()
