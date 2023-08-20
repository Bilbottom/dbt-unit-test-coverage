/*
This is a short-term solution to generate the coverage metrics.

This will be converted into a pure-Python solution in the future, but
while this project is in its infancy, this is a quick and easy approach.

The dialect is SQLite.
*/


/*
The dbt models in the project and their CTEs.
*/
CREATE TABLE models(
    model_name TEXT NOT NULL COLLATE NOCASE,
    cte_name TEXT NOT NULL COLLATE NOCASE,
    cte_type TEXT NOT NULL COLLATE NOCASE,

    CONSTRAINT pk_models PRIMARY KEY (model_name, cte_name)
);
/*
The unit tests in the project and which CTE they test.
*/
CREATE TABLE tests(
    model_name TEXT NOT NULL COLLATE NOCASE,
    cte_name TEXT COLLATE NOCASE
);


/*
The models in the dbt project with a flag to indicate whether they are
covered by a unit test.
*/
CREATE VIEW coverage_flags AS
    SELECT
        models.model_name,
        models.cte_name,
        (tests.model_name IS NOT NULL) AS coverage_flag
    FROM models
        LEFT JOIN tests
            ON  models.model_name = tests.model_name
            AND models.cte_name = COALESCE(tests.cte_name, 'final') COLLATE NOCASE
    WHERE models.cte_type != 'import'
;


/*
The rolled-up coverage metrics for the dbt project.
*/
CREATE VIEW coverage_report AS
        SELECT
            model_name,
            COUNT(*) AS ctes,
            SUM(1 - coverage_flag) AS miss,
            100.0 * SUM(coverage_flag) / COUNT(*) AS cover,
            GROUP_CONCAT(cte_name, ', ') FILTER(WHERE coverage_flag = 0) AS missing
        FROM coverage_flags
        GROUP BY model_name
    UNION
        SELECT
            'TOTAL' AS model_name,
            COUNT(*) AS ctes,
            SUM(1 - coverage_flag) AS miss,
            100.0 * SUM(coverage_flag) / COUNT(*) AS cover,
            NULL AS missing
        FROM coverage_flags

    ORDER BY model_name
;
