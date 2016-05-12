--Create final songs feature
BEGIN;
CREATE TEMP VIEW tmp AS
SELECT t1.*, t2.song_init_plays, t2.Language, t2.gender
FROM songs_partial_feature AS t1 JOIN filtered_songs AS t2
USING (song_id);

CREATE TABLE songs_feature AS
SELECT t1.*, t2.age, t2.isHoliday, t2.weekday, t2.date
FROM tmp AS t1 JOIN songs_date AS t2
USING (song_id);
COMMIT;  

CREATE TABLE song_plays_everyday AS
SELECT song_id, date, count(*) AS cnt
FROM filtered_actions_detail
WHERE action_type = 1
GROUP BY song_id, date;

CREATE TABLE data AS
SELECT t1.*, t2.cnt 
FROM songs_feature  AS t1 
LEFT OUTER JOIN song_plays_everyday AS t2 
ON t1.song_id = t2.song_id AND t1."t2.date" = t2.date;
