SELECT CONCAT(route_short_name , ' - ', route_long_name) as rota
FROM routes 

SELECT *
FROM routes ;

SELECT  *
FROM shapes

DROP TABLE SHAPES


select shape_pt_lat as lat, shape_pt_lon as long
FROM shapes
where shape_id = '81072'

select  *
FROM shapes


CREATE TABLE shapes (
    shape_id VARCHAR(20) NOT NULL,
    shape_pt_lat DECIMAL(10, 6) NOT NULL,
    shape_pt_lon DECIMAL(10, 6) NOT NULL,
    shape_pt_sequence INT NOT NULL,
    shape_dist_traveled DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (shape_id, shape_pt_sequence)
);



INSERT INTO shapes (shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled)
VALUES
    ('81072', -23.432024, -46.787121, 1, 0)


DELETE FROM 
shapes

