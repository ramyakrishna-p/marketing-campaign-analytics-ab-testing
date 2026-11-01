-- SYNTHETIC campaign data
SELECT channel, SUM(clicks)*1.0/SUM(impressions) AS ctr, SUM(conversions)*1.0/NULLIF(SUM(clicks),0) AS conv_rate, (SUM(revenue)-SUM(cost))/SUM(cost) AS roi FROM campaign GROUP BY channel ORDER BY roi DESC;
SELECT variant, SUM(conversions), SUM(clicks) FROM campaign GROUP BY variant;
