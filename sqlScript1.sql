--Filter out users with just ONE action
--and users with no play actions
BEGIN;

CREATE TEMP VIEW tmp AS
SELECT user_id, COUNT(*) AS cnt 
FROM mars_tianchi_user_actions 
GROUP BY user_id;

CREATE TABLE filtered_actions AS
SELECT * FROM mars_tianchi_user_actions
WHERE user_id NOT IN
(SELECT user_id FROM tmp WHERE cnt = 1)
AND user_id IN
(SELECT DISTINCT user_id FROM mars_tianchi_user_actions WHERE action_type = 1);

COMMIT;

--Filter out songs not in filtered_actions
CREATE TABLE filtered_songs AS 
SELECT * FROM mars_tianchi_songs 
WHERE song_id IN 
(SELECT DISTINCT song_id FROM filtered_actions);

--DS is not exact. Totally 224 records that gmt_create doesn't match DS (one day delayed).
CREATE VIEW filtered_actions_detail AS
SELECT user_id, song_id, action_type, gmt_create,
strftime('%m', gmt_create, 'unixepoch', 'localtime') AS month,
strftime('%d', gmt_create, 'unixepoch', 'localtime') AS day,
strftime('%w', gmt_create, 'unixepoch', 'localtime') AS weekday,
strftime('%Y%m%d', gmt_create, 'unixepoch', 'localtime') AS date
FROM filtered_actions;

--Sums of songs' plays, downloads and collects for each month
CREATE VIEW songs_action_counts_per_month AS
SELECT song_id, month, action_type, count(*) AS cnt
FROM filtered_actions_detail
GROUP BY song_id, month, action_type;

--Sums of songs' plays, downloads and collects for each weekday
CREATE VIEW songs_action_counts_per_weekday AS
SELECT song_id, weekday, action_type, count(*) AS cnt
FROM filtered_actions_detail
GROUP BY song_id, weekday, action_type;
