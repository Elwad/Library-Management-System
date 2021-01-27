drop table customer;
drop table author;
drop table book1;
drop table book2;
drop table publisher;
drop table employee;
drop table borrows;
drop table writes;
drop table publishes;
drop table issues;

drop VIEW American_Publishers;
drop VIEW Copies_per_book;


CREATE TABLE customer(cName VARCHAR2(30), cEmail VARCHAR2(30), phoneNumber VARCHAR2(30),libraryCardNumber VARCHAR2(30) PRIMARY KEY, address VARCHAR2(30));

CREATE TABLE author(aName VARCHAR2(30) , aID VARCHAR2(30) PRIMARY KEY);

CREATE TABLE book1(title VARCHAR2(30),ISBN VARCHAR2(30) PRIMARY KEY, price FLOAT, numberOfCopies INTEGER,pName VARCHAR2(30));

CREATE TABLE book2(title VARCHAR2(30), aName VARCHAR2(30));

CREATE TABLE publisher(pName VARCHAR2(30) , pID VARCHAR2(30) PRIMARY KEY);

CREATE TABLE employee(eName VARCHAR2(30) ,eEmail VARCHAR2(30), employeeNumber VARCHAR2(30) PRIMARY KEY);

CREATE TABLE borrows(ISBN VARCHAR2(30),cName VARCHAR2(30),borrowDate date, returnDate date);

CREATE TABLE writes(title VARCHAR2(30) , aID VARCHAR2(30));

CREATE TABLE publishes(ISBN VARCHAR2(30),publishDate date, publishCountry VARCHAR2(30),pID VARCHAR2(30));

CREATE TABLE issues(ISBN VARCHAR2(30),cName VARCHAR2(30),eName VARCHAR2(30),issueDate date,returnDate date);

insert into customer values('Robert Morrison', 'robert12@gmail.com', '9876543210', 'AB12-3456-7890', '350 Victoria St,Toronto,ON');

insert into author values('J K Rowling', '123456789');
insert into author values('Stephanie Meyer', '987654321');

insert into book1 values('Harry Potter','9788700631625', 11.99, 6,'Bloomsbury Publishing');
insert into book2 values('Harry Potter','J K Rowling');
insert into book1 values('Harry Potter','9788700639000', 9.99, 5,'HarperCollins');
insert into book1 values( 'Harry Potter','9788700612345', 8.99, 2,'Macmillan');
insert into book1 values('Harry Potter','9788700633348', 9.99, 8,'Penguin Random House');
insert into book1 values( 'Twilight','9788700999921', 13.99, 5,'Little, Brown and Company');
insert into book2 values('Twilight','Stephenie Meyer');

insert into publisher values('Bloomsbury Publishing','01984336');
insert into publisher values('HarperCollins','01984000');
insert into publisher values('Macmillan','01984123');
insert into publisher values('Penguin Random House','01984987');
insert into publisher values('Little, Brown and Company','01985000');

insert into employee values('Emily Waren', 'emily09@gmail.com', '5432167890');
insert into employee values('Danny Frank', 'dfrank@gmail.com', '5432167000');
insert into employee values('David Thomas', 'dthomas@gmail.com', '5432163000');
insert into employee values('Robert Morrison', 'robert12@gmail.com', '5432149800');

insert into borrows values('9788700631625','Robert Morrison','2019-09-30', '2019-10-15');
insert into borrows values('9788700612345','Robert Morrison','2019-09-30', '2019-10-15');
insert into borrows values('9788700631625','Robert Morrison','2019-09-30', '2019-10-15');

insert into writes values('Harry Potter','123456789');
insert into writes values('Twilight','987654321');

insert into publishes values('9788700631625','1997-06-26','UK','01984336');
insert into publishes values('9788700639000','1999-08-19','America','01984000');
insert into publishes values('9788700612345','1997-10-05','UK','01984123');
insert into publishes values('9788700633348','1998-12-11','America','01984987');
insert into publishes values('9788700999921','2005-10-05','America','01985000');

insert into issues values('9788700631625','Robert Morrison','Emily Waren',  '2019-09-30', '2019-10-15');
insert into issues values('9788700612345','Robert Morrison','Danny Frank',  '2019-09-30', '2019-10-15');
insert into issues values('9788700631625','Robert Morrison','David Thomas',  '2019-09-30', '2019-10-15');

select * from customer;

select * from author;

select * from book1;

select * from book2;

select * from publisher;

select * from employee;

select * from borrows;

select * from writes;

select * from publishes;

select * from issues;

select book1.title, ISBN,book2.aName from book1,book2 
where book2.aName='J K Rowling'
AND book1.title= book2.title;

select book1.title, publishes.ISBN, publishes.publishDate, publishes.publishCountry,book1.pName from publishes, book1
where publishes.ISBN= book1.ISBN;

select book1.title,issues.ISBN,issues.eName, employee.employeeNumber,issues.cName,issues.issueDate from issues, book1, employee
where issues.eName= employee.eName
AND issues.ISBN= book1.ISBN;

select title, ISBN, price from book1
order by price ASC;

select title, ISBN, price from book1 
where price<=10;

select DISTINCT title,aName from book2;

select DISTINCT pName from book1
where title = 'Harry Potter';


create view American_Publishers as (select publisher.pName from publisher, publishes 
where publishes.pID= publisher.pID
AND publishes.publishCountry='America'
);

select * from American_Publishers;


select * from Copies_per_book;

select cName from customer INTERSECT select eName from employee;

SELECT title, SUM(price)
FROM book1
GROUP BY title;
