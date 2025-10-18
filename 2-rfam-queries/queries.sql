-- 2a, Part 1: How many types of tigers?
SELECT COUNT(*) AS tiger_count
FROM taxonomy 
WHERE species LIKE 'Panthera tigris%';


--  2a, Part 2: ncbi_id of the Sumatran Tiger
SELECT ncbi_id 
FROM taxonomy 
WHERE species = 'Panthera tigris sumatrae';

-- 2b : columns to connect tables (primary key -> foreign key)

-- family.rfam_acc (PK) -> full_region.rfam_acc (FK)
-- family.rfam_acc (PK) -> seed_region.rfam_acc (FK)
-- family.rfam_acc (PK) -> family_literature.rfam_acc (FK)
--
-- rfamseq.rfamseq_acc (PK) -> full_region.rfamseq_acc (FK)
-- rfamseq.rfamseq_acc (PK) -> seed_region.rfamseq_acc (FK)
--
-- taxonomy.ncbi_id (PK) -> rfamseq.ncbi_id (FK)
--
-- literature_reference.pmid (PK) -> family_literature.pmid (FK)


-- 2c: Which type of rice has the longest DNA sequence?
SELECT
t.species,
r.length
FROM rfamseq r
JOIN taxonomy t ON r.ncbi_id = t.ncbi_id
WHERE t.species LIKE 'Oryza%'
ORDER BY r.length DESC
LIMIT 1;



-- 2d: Paginated query for families with max DNA sequence > 1,000,000
SELECT
f.rfam_acc,
f.description AS family_name,
MAX(rs.length) AS max_length
FROM family f
JOIN full_region fr ON f.rfam_acc = fr.rfam_acc
JOIN rfamseq rs ON fr.rfamseq_acc = rs.rfamseq_acc
GROUP BY f.rfam_acc, f.description
HAVING max_length > 1000000
ORDER BY max_length DESC
LIMIT 15
OFFSET 120;