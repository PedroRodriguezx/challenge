SELECT
    c.id,
    c.name,
    c.iso3_code,
    COALESCE(MAX(CASE WHEN g.year = 2019 THEN g.value / 1e9 END), 0) AS "2019",
    COALESCE(MAX(CASE WHEN g.year = 2020 THEN g.value / 1e9 END), 0) AS "2020",
    COALESCE(MAX(CASE WHEN g.year = 2021 THEN g.value / 1e9 END), 0) AS "2021",
    COALESCE(MAX(CASE WHEN g.year = 2022 THEN g.value / 1e9 END), 0) AS "2022",
    COALESCE(MAX(CASE WHEN g.year = 2023 THEN g.value / 1e9 END), 0) AS "2023"
FROM
    country c
LEFT JOIN
    gdp g ON c.id = g.country_id
WHERE
    g.year BETWEEN 2019 AND 2023
GROUP BY
    c.id, c.name, c.iso3_code
ORDER BY
    c.id;
