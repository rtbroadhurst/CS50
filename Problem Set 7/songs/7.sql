-- Returns the average energy of songs that are by Drake
SELECT AVG(energy) AS avg_energy FROM songs WHERE artist_id IN (SELECT id FROM artists WHERE name = 'Drake');
