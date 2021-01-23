-- DROP TABLE IF EXISTS fact_tags;
CREATE TABLE fact_tags
(
  id                INT IDENTITY (1,1) UNIQUE,
  instagram_post_id VARCHAR(256),
  tag               NVARCHAR(1024),
  created_date      DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

ALTER TABLE fact_tags
  ADD CONSTRAINT tag_id UNIQUE (instagram_post_id, tag);