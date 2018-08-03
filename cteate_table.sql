
create table hk_financials(
id int not null primary key auto_increment,
Dates date not null,
coding text CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci' ,
before_profits varchar(11),
after_profits varchar(11)
) engine = InnoDB default charset=utf8;