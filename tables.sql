
CREATE TABLE public.standup1
(
    _id serial,
    slack_id varchar(20),
    report json NOT NULL,
    ts timestamp 
)


create table resources(
id serial primary key,
title varchar(30),
resource varchar(200),
ts timestamp



)

