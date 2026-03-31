-- 12. Titles of all of movies in which both Jennifer Lawrence and Bradley Cooper starred
SELECT movies.title
FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE people.name IN ('Jennifer Lawrence', 'Bradley Cooper')
GROUP BY movies.id
HAVING COUNT(DISTINCT people.name) = 2;
