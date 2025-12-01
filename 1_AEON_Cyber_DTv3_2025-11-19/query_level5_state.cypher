// Query current Level 5 component counts
MATCH (n) WHERE n:GeopoliticalEvent OR n:ThreatFeed OR n:CognitiveBias OR n:EventProcessor OR n:InformationEvent
RETURN labels(n) as Type, count(*) as Count
ORDER BY Type;
