# Troubleshooting

mysql 8.0

## password_policy

修改密码的限制。

```sql
show variables like 'validate_password%';
```

```bash
+--------------------------------------+--------+
| Variable_name                        | Value  |
+--------------------------------------+--------+
| validate_password.dictionary_file    |        |
| validate_password.length             | 8      |
| validate_password.mixed_case_count   | 1      |
| validate_password.number_count       | 1      |
| validate_password.policy             | MEDIUM |
| validate_password.special_char_count | 1      |
+--------------------------------------+--------+
```

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new-password';
flush privileges;
```

## 跳过登陆认证

```bash
systemctl stop mysql
mysqld --skip-grant-tables
sudo mysql
```

## 登陆认证方式

```sql
use mysql;
select user, host, plugin from user;
```

```bash
+------------------+-----------+-----------------------+
| user             | host      | plugin                |
+------------------+-----------+-----------------------+
| clay             | localhost | caching_sha2_password |
| debian-sys-maint | localhost | caching_sha2_password |
| mysql.infoschema | localhost | caching_sha2_password |
| mysql.session    | localhost | caching_sha2_password |
| mysql.sys        | localhost | caching_sha2_password |
| root             | localhost | auth_socket           |
+------------------+-----------+-----------------------+
```

```sql
update user set plugin = 'caching_sha2_password';
flush privileges;
```

# 一些常用操作

```sql
## 数据库的创建
create database bank;
# 引用之
use bank;
## 表的创建
create table person
(
    person_id smallint unsigned,
    fname varchar(20),
    iname varchar(20),
    gender enum('M', 'F'),
    birth_date date,
    street varchar(30),
    city varchar(20),
    state varchar(20),
    country varchar(20),
    postal_code varchar(20),
#     约束为主键，创建在 person_id，并命名为 pk_person
    constraint pk_person primary key (person_id)
);
desc person;
create table favorite_food
(
    person_id smallint unsigned,
    food varchar(20),
#     联合主键，person_id和food
    constraint pk_favorite_food primary key (person_id, food),
#     foreign 约束，限制了 person_id 的值只能来自 person 表
    constraint fk_fav_food_person_id foreign key (person_id)
        references person (person_id)
);
desc favorite_food;
# 主键生成 1, 查看表中主键最大值；2, auto_increment
# 必须去掉foreign key约束才可以修改person_id列
alter table favorite_food
    drop foreign key fk_fav_food_person_id,
    modify person_id smallint unsigned;

# alter table语句选中表，modify 修改已存在的列的属性
alter table person modify person_id smallint unsigned auto_increment;
desc favorite_food;
alter table favorite_food
    add constraint fk_fav_food_person_id foreign key (person_id)
        references person (person_id);

# 发现person表中的列lname写错了，change修改名字以及数据类型
alter table person change iname lname varchar(20);
desc person;

## 插入：表名、列名、值
insert into person
    (person_id, fname, lname, gender, birth_date)
    values (null, 'William', 'Turner', 'M', '1972-05-27');
insert into favorite_food
    (person_id, food)
    values (1, 'pizza');
insert into favorite_food
    (person_id, food)
    values (1, 'cookies');
insert into favorite_food
    (person_id, food)
    values (1, 'nachos');
select food
    from favorite_food
    where person_id = 1
    order by food;

insert into person
    (person_id, fname, lname, gender, birth_date,
     street, city, state, country, postal_code)
    values(null, 'Sussan', 'Smith', 'F', '1975-11-02',
           '23 Maple St.', 'Arlington', 'VA', 'USA', '20220');
select * from person;

## 更新数据
update person
    set street = '1225 Tremont St.',
        city = 'Boston',
        country = 'USA',
        postal_code = '02138'
    where person_id = 1;
select * from person where person_id = 1;

## 删除数据
delete from person
    where person_id = 2;

update person
    set gender = 'a'
    where person_id = 1;

# 日期格式化
update person
    set birth_date = str_to_date('DEC-21-1980', '%b-%d-%Y')
    where person_id = 1;
select * from person;

desc person;

## 删除表
drop table favorite_food;
drop table person;
```







