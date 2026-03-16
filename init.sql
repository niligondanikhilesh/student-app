CREATE TABLE IF NOT EXISTS students (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100),
	grade VARCHAR(10)
);

INSERT INTO students (name, grade) VALUES ('Nikhil', 'A');
INSERT INTO students (name, grade) VALUES ('Charani', 'O');
INSERT INTO students (name, grade) VALUES ('Jaswanth', 'A+');
