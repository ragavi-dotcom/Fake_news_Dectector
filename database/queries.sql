SELECT id, substr(text, 1, 80) AS preview, label, confidence, created_at
FROM predictions
ORDER BY id DESC
LIMIT 20;

SELECT label, COUNT(*) AS n, ROUND(AVG(confidence), 3) AS avg_conf
FROM predictions
GROUP BY label;

SELECT id, label, confidence, substr(text, 1, 120) AS preview
FROM predictions
WHERE confidence < 0.70
ORDER BY confidence ASC;

SELECT
    p.label,
    COUNT(f.id)                                       AS n_reviewed,
    SUM(f.was_correct)                                AS n_correct,
    ROUND(1.0 * SUM(f.was_correct) / COUNT(f.id), 3)  AS accuracy
FROM predictions p
JOIN feedback f ON f.prediction_id = p.id
GROUP BY p.label;

DELETE FROM predictions WHERE created_at < date('now', '-30 day');
