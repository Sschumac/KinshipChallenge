create user kinship_webapp with password 'eLW351QurgM9kZWDnoyTalHx6VpVAclZd';
create table daily_agg_2019(
    dog_id INT NOT NULL,
   	date date NOT NULL,
    eat_score real NOT NULL,
    drink_score real NOT NULL,
    chew_score real NOT NULL,
    sniff_score real NOT NULL,
    jump_score real NOT NULL,
    PRIMARY KEY(dog_id, date)
);

ALTER TABLE daily_agg_2019 
   ADD CONSTRAINT date 
   CHECK (extract(year from date) = 2019);

grant select, insert, update, delete on daily_agg_2019 to kinship_webapp;