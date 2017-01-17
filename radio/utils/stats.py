from django.db import connection


def get_song_stats(start, end, radio_id=None):

    sql = """
        WITH plays AS (
           SELECT radio_id, artist, title, count(*) AS count
            FROM radio_play
           WHERE timestamp BETWEEN %s AND %s %RADIO%
        GROUP BY radio_id, artist, title
        )
        SELECT radio_id,
               r.name AS radio_name,
               count(*) AS distinct_count,
               count(*) FILTER (WHERE count = 1) AS single_play_count,
               round(100 * count(*) FILTER (WHERE count = 1) / count(*), 1) AS single_play_perc,
               count(*) FILTER (WHERE count > 1) AS repeated_count,
               round(100 * count(*) FILTER (WHERE count > 1) / count(*), 1) AS repeated_perc,
               avg(count) FILTER (WHERE count > 1) AS avg_repetitions
        FROM plays p
        JOIN radio_radio r ON r.id = p.radio_id
        GROUP BY 1, 2
        ORDER BY r.name
    """

    args = [start, end]

    if radio_id:
        radio_where = "AND radio_id = %s"
        args.append(radio_id)
    else:
        radio_where = ""

    sql = sql.replace('%RADIO%', radio_where)

    with connection.cursor() as cursor:
        cursor.execute(sql, args)
        data = dictfetchall(cursor)

    return data[0] if radio_id else data


def get_artist_stats(start, end, radio_id=None):

    sql = """
        WITH plays AS (
           SELECT radio_id, artist, count(*) AS count
            FROM radio_play
           WHERE timestamp BETWEEN %s AND %s %RADIO%
        GROUP BY radio_id, artist
        )
        SELECT radio_id,
               r.name AS radio_name,
               count(*) AS distinct_count,
               count(*) FILTER (WHERE count = 1) AS single_play_count,
               round(100 * count(*) FILTER (WHERE count = 1) / count(*), 1) AS single_play_perc,
               count(*) FILTER (WHERE count > 1) AS repeated_count,
               round(100 * count(*) FILTER (WHERE count > 1) / count(*), 1) AS repeated_perc,
               avg(count) FILTER (WHERE count > 1) AS avg_repetitions
        FROM plays p
        JOIN radio_radio r ON r.id = p.radio_id
        GROUP BY 1, 2
        ORDER BY r.name
    """

    args = [start, end]

    if radio_id:
        radio_where = "AND radio_id = %s"
        args.append(radio_id)
    else:
        radio_where = ""

    sql = sql.replace('%RADIO%', radio_where)

    with connection.cursor() as cursor:
        cursor.execute(sql, args)
        data = dictfetchall(cursor)

    return data[0] if radio_id else data


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
