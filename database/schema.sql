DROP TABLE IF EXISTS predictions;

CREATE TABLE predictions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    text        TEXT      NOT NULL,      -- first 1000 chars of the article
    label       TEXT      NOT NULL,      -- 'fake' or 'real'
    confidence  REAL      NOT NULL,      -- 0.0 – 1.0
    created_at  TEXT      NOT NULL       -- ISO-8601 UTC timestamp
);

CREATE INDEX idx_predictions_created_at ON predictions(created_at DESC);
CREATE INDEX idx_predictions_label      ON predictions(label);

DROP TABLE IF EXISTS feedback;

CREATE TABLE feedback (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id  INTEGER NOT NULL REFERENCES predictions(id) ON DELETE CASCADE,
    was_correct    INTEGER NOT NULL,   -- 1 = yes, 0 = no
    created_at     TEXT    NOT NULL
);
