CREATE TABLE `active` (
	`bet_id`	TEXT,
	`bet_amt`	INTEGER,
	`amount`	INTEGER,
	`bet_desc`	TEXT,
	`bet_date`	INTEGER
);

CREATE TABLE `his` (
	`bet_status`	TEXT,
	`bet_time`	TEXT NOT NULL,
	`bet_desc`	TEXT,
	`pos_win`	INTEGER,
	`ID`	TEXT,
	`bet_amnt`	INTEGER,
	PRIMARY KEY(bet_time)
);


