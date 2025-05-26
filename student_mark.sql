create database proj;
use proj;
create table classs(
c_id VARCHAR(10) PRIMARY KEY,
c_name text not null
);

create table faculty(
f_id VARCHAR(10) PRIMARY KEY,
f_name text not null,
c_id VARCHAR(10),
password text not null
);
drop table student;
select * from faculty;
create table student(
s_id VARCHAR(20) primary key,
s_name text,
password text,
c_id VARCHAR(20)
);
select * from student;

create table subject(
sub_id VARCHAR(20) primary key,
sub_name text not null,
s_id VARCHAR(20)
);

create table internals(
m_id serial primary key,
f_id VARCHAR(20),
s_id VARCHAR(20),
sub_id VARCHAR(20),
sub_name text,
mid1 int,
mid2 int,
mid3 int,
internal_total float);
drop table internals;
select * from internals;

CREATE TABLE externals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    s_id VARCHAR(50),
    f_id VARCHAR(50),
    sub_id VARCHAR(50),
    sub_name VARCHAR(100),
    external_marks FLOAT,
    internal_total FLOAT,
    final_marks FLOAT
);
DROP table externals;
select * from externals;