# api/crud.py
from .database import get_connection

def get_top_objects(limit=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT detected_object_class, COUNT(*) as count
        FROM staging.fct_image_detections
        GROUP BY detected_object_class
        ORDER BY count DESC
        LIMIT %s;
    """, (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"detected_object_class": r[0], "count": r[1]} for r in rows]

def get_channel_activity(channel_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DATE(message_time), COUNT(*)
        FROM staging.fct_messages
        WHERE channel = %s
        GROUP BY DATE(message_time)
        ORDER BY DATE(message_time);
    """, (channel_name,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"date": str(r[0]), "count": r[1]} for r in rows]

def search_messages(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT message_id, channel, message, views
        FROM staging.fct_messages
        WHERE message ILIKE %s
        LIMIT 50;
    """, (f"%{query}%",))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"message_id": r[0], "channel": r[1], "message": r[2], "views": r[3]} for r in rows]
