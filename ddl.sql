CREATE TABLE IF NOT EXISTS tb_hockei_team(
    id SERIAL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "year" SMALLINT NOT NULL,
    wins SMALLINT NOT NULL,
    losses SMALLINT NOT NULL,
    ot_losses VARCHAR(100) NOT NULL,
    win_percent VARCHAR(10) NOT NULL,
    goals_for SMALLINT NOT NULL,
    goals_against SMALLINT NOT NULL,
    diff VARCHAR(10) NOT NULL
);