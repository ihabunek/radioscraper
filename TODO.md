TODO
====

* Check out nondeterministic ICU collations:
  https://stackoverflow.com/questions/11005036/does-postgresql-support-accent-insensitive-collations/11007216#11007216
* Store the normalized name in `ArtistName` model instead of calculating it
  every time in the query. That way we can get rid of `upper_iunaccent`
  indices.
* Same with the letter used to group by letter in `ArtistListByLetterView`.
* Store monthy stats in the database to avoid having to calculate them in stats
  views every time.
