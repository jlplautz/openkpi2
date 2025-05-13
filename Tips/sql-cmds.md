psql -U your_username -d your_database
SELECT * FROM your_table ORDER BY id DESC LIMIT 1;
SELECT * FROM your_table ORDER BY created_at DESC LIMIT 1;
kpidata-# \d "LTE_eNB_Load"
                                           Table "public.LTE_eNB_Load"
    Column     |            Type             | Collation | Nullable |
 Default
---------------+-----------------------------+-----------+----------+--------------------------------------------
 id            | integer                     |           | not null | nextval('"LTE_eNB_Load_id_seq"'::regclass)
 create_at     | timestamp without time zone |           |          |
 manage_object | text                        |           |          |
 M8018C6       | integer                     |           |          |
 M8018C4       | integer                     |           |          |
 M8018C8       | integer                     |           |          |
 M8018C5       | integer                     |           |          |
 M8018C0       | integer                     |           |          |
 M8018C9       | integer                     |           |          |
 M8018C7       | integer                     |           |          |
 M8018C11      | integer                     |           |          |
 M8018C10      | integer                     |           |          |
 M8018C1       | integer                     |           |          |
Indexes:    "LTE_eNB_Load_pkey" PRIMARY KEY, btree (id)



kpidata=# SELECT * FROM "LTE_S1AP" ORDER BY id DESC LIMIT 1;
 id  |      create_at      |  manage_object  | M8000C41 | M8000C30 | M8000C42 | M8000C33 | M8000C7 | M8000C38 | M8000C36 | M8000C
00C43 | M8000C45 | M8000C24 | M8000C11 | M8000C6 | M8000C26 | M8000C46 | M8000C32 | M8000C44 | M8000C37 | M8000C39 | M8000C40 | M
 | M8000C8 | M8000C13 | M8000C16 | M8000C14
-----+---------------------+-----------------+----------+----------+----------+----------+---------+----------+----------+-------
------+----------+----------+----------+---------+----------+----------+----------+----------+----------+----------+----------+--
-+---------+----------+----------+----------
 338 | 2025-05-06 17:30:00 | NE-MRBTS-690503 |        0 |       83 |        0 |        0 |       0 |        6 |        0 |
    0 |        0 |        0 |     3041 |       0 |        0 |        0 |        0 |        0 |        1 |        0 |        0 |
 |       0 |        0 |        0 |        0
(1 row)

kpidata=# SELECT * FROM "LTE_eNB_Load" ORDER BY id DESC LIMIT 1;
 id  |      create_at      |  manage_object  | M8018C6 | M8018C4 | M8018C8 | M8018C5 | M8018C0 | M8018C9 | M8018C7 | M8018C11 | M
-----+---------------------+-----------------+---------+---------+---------+---------+---------+---------+---------+----------+--
 338 | 2025-05-06 17:30:00 | NE-MRBTS-690503 |       0 |       0 |    1801 |       0 |       2 |     900 |       0 |        0 |
(1 row)

