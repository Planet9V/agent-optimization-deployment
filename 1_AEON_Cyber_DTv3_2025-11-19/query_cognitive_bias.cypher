// Query existing CognitiveBias nodes
MATCH (cb:CognitiveBias)
RETURN cb.biasName as BiasName, cb.category as Category, count(*) as Count
ORDER BY BiasName;
