CREATE TABLE users (
    id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT
);

CREATE TABLE gymplans (
	id SERIAL PRIMARY KEY,
	name TEXT,
	owner_id INTEGER REFERENCES users,
	visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE moves (
    id SERIAL PRIMARY KEY,
	name TEXT
);

CREATE TABLE moveinformations (
    id SERIAL PRIMARY KEY,
	move_id INTEGER REFERENCES moves,
	sets INTEGER,
	reps INTEGER,
	weight INTEGER
);

CREATE TABLE movesinplans (
    id SERIAL PRIMARY KEY,
	moveinfo_id INTEGER REFERENCES moveinformations,
    plan_id INTEGER REFERENCES gymplans,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE movesdone ( 
    id SERIAL PRIMARY KEY,
	moveinfo_id INTEGER REFERENCES moveinformations,
	plan_id INTEGER REFERENCES gymplans,
	day DATE
);

INSERT INTO moves (name) VALUES ('Kyykky');
INSERT INTO moves (name) VALUES ('Penkkipunnerrus');
INSERT INTO moves (name) VALUES ('Maastaveto');
INSERT INTO moves (name) VALUES ('Ylätalja');
INSERT INTO moves (name) VALUES ('Alatalja');
INSERT INTO moves (name) VALUES ('Selän ojennus');
INSERT INTO moves (name) VALUES ('Vipunosto taakse');
INSERT INTO moves (name) VALUES ('Hauiskääntö');
INSERT INTO moves (name) VALUES ('Vatsarutistus');
INSERT INTO moves (name) VALUES ('Vatsakierto');
INSERT INTO moves (name) VALUES ('Jalkojen loitonnus');
INSERT INTO moves (name) VALUES ('Jalkojen lähennys');
INSERT INTO moves (name) VALUES ('Penkkipunnerrus vino');
INSERT INTO moves (name) VALUES ('Ranskalainen punnerrus');
INSERT INTO moves (name) VALUES ('Vipunosto sivulle');
INSERT INTO moves (name) VALUES ('Vipunosto eteen');
INSERT INTO moves (name) VALUES ('Pystypunnerrus');
