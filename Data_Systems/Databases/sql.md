
# Select
## The PADS (pivot)
Query an alphabetically ordered list of all names in OCCUPATIONS, immediately followed by the first letter of each profession as a parenthetical (i.e.: enclosed in parentheses). For example: AnActorName(A), ADoctorName(D), AProfessorName(P), and ASingerName(S).

Query the number of ocurrences of each occupation in OCCUPATIONS. Sort the occurrences in ascending order, and output them in the following format:

"There are a total of [occupation_count] [occupation]s."

where [occupation_count] is the number of occurrences of an occupation in OCCUPATIONS and [occupation] is the lowercase occupation name. If more than one Occupation has the same [occupation_count], they should be ordered alphabetically.

OCCUPATIONS:
| Column     | Type   |
| ---------- | ------ |
| Name       | String |
| Occupation | String |

```sql
SELECT 
  CONCAT(o.Name, '(', SUBSTRING(o.Occupation,1,1), ')')
FROM OCCUPATIONS as o ORDER BY o.Name;
SELECT CONCAT("There are a total of ", count(Occupation), " ", LOWER(Occupation) , "s.")
FROM OCCUPATIONS GROUP BY Occupation ORDER BY count(Occupation), Occupation;
```

## New Companies
Given the table schemas below, write a query to print the company_code, founder name, total number of lead managers, total number of senior managers, total number of managers, and total number of employees. Order your output by ascending company_code.

Note:

The tables may contain duplicate records.
The company_code is string, so the sorting should not be numeric. For example, if the company_codes are C_1, C_2, and C_10, then the ascending company_codes will be C_1, C_10, and C_2.

Company:
| Column       | Type   |
| ------------ | ------ |
| company_code | String |
| founder      | String |

And then you have tables with the hierarchy in them, but they all have `company_code` and a code for the person, e.g.
Lead_Manager:
| Column            | Type   |
| ----------------- | ------ |
| company_code      | String |
| lead_manager_code | String |

Table (code field) format for remaining tables are:
- Senior_Manager (senior_manager_code)
- Manager (manager_code)
- Employee (employee_code)

```sql
SELECT c.company_code, max(c.founder), count(distinct(lm.lead_manager_code)), count(distinct(sm.senior_manager_code)), count(distinct(mm.manager_code)), count(distinct(em.employee_code))
FROM Company as c 
JOIN Lead_Manager as lm on lm.company_code=c.company_code
JOIN Senior_Manager as sm on sm.company_code=c.company_code
JOIN Manager as mm on mm.company_code=c.company_code
JOIN Employee as em on em.company_code=c.company_code
GROUP BY c.company_code
ORDER BY c.company_code;
```

## Weather Station Observation
A median is defined as a number separating the higher half of a data set from the lower half. Query the median of the Northern Latitudes (LAT_N) from STATION and round your answer to  decimal places.

STATION:
| Column | Type   |
| ------ | ------ |
| ID     | NUMBER |
| CITY   | String |
| STATE  | String |
| LAT_N  | String |
| LONG_W | String |

```sql
SELECT ROUND(LAT_N,4) FROM STATION
ORDER BY LAT_N
LIMIT 1 OFFSET 249
```

## Top Earners
We define an employee's total earnings to be their monthly salary x months  worked, and the maximum total earnings to be the maximum total earnings for any employee in the Employee table. Write a query to find the maximum total earnings for all employees as well as the total number of employees who have maximum total earnings. Then print these values as 2 space-separated integers.

Employee:
| Column      | Type    |
| ----------- | ------- |
| employee_id | Integer |
| name        | String  |
| months      | Integer |
| salary      | Integer |

```sql
SELECT salary*months as te, COUNT(*)
FROM Employee
GROUP BY te
ORDER BY te DESC
LIMIT 1
```

## Type of Triangle
Write a query identifying the type of each record in the TRIANGLES table using its three side lengths. Output one of the following statements for each record in the table:

Equilateral: It's a triangle with  sides of equal length.
Isosceles: It's a triangle with  sides of equal length.
Scalene: It's a triangle with  sides of differing lengths.
Not A Triangle: The given values of A, B, and C don't form a triangle.

TRIANGLES:
| Column | Type    |
| ------ | ------- |
| A      | Integer |
| B      | Integer |
| C      | Integer |

```sql
SELECT
CASE
    WHEN not ((A+B) > C and (A+C) > B and (B+C) > A) THEN "Not A Triangle"
    WHEN A = B and B = C THEN "Equilateral"
    WHEN A = B or B = C or A = C THEN "Isosceles"
    ELSE "Scalene"
END
FROM TRIANGLES
```

# Update
```sql
UPDATE documents SET author = "Jackie Draper" where author = "Jackie Paper";
SELECT * from documents;
```

# Delete
```sql
DELETE from documents where title = "Things I'm Afraid Of";
select * from documents;
```

