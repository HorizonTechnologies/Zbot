
create table resources(
id serial primary key,
title varchar(30),
resource varchar(200),
ts timestamp



)


create table resources(
id serial primary key,
title varchar(30),
resource varchar(200),
ts timestamp



)

create table dayoff(
id serial primary key,
slack_id varchar(30),
ts timestamp



)
create table reminders(
id serial primary key,
slack_id varchar(30),
timetoset varchar(10),
ts timestamp



)

