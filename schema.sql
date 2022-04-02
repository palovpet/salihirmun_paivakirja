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
	weights INTEGER
);

CREATE TABLE movesinplans (
    id SERIAL PRIMARY KEY,
    plan_id INTEGER REFERENCES gymplans,
    visible BOOLEAN DEFAULT TRUE
);
