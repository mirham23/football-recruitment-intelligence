-- Football Recruitment Intelligence -- v1 schema.
-- Grain: one row per player-team-season in player_season; one row per player in players.
-- Run with: psql -U postgres -d fri -f sql/schema.sql

CREATE TABLE IF NOT EXISTS players (
    player_id           INTEGER PRIMARY KEY,
    player_name         TEXT NOT NULL,
    date_of_birth       DATE,
    position            TEXT,
    foot                TEXT,
    height_in_cm        REAL,
    current_club_name   TEXT
);

CREATE TABLE IF NOT EXISTS player_season (
    league_season       TEXT NOT NULL,
    sb_player           TEXT NOT NULL,
    sb_team             TEXT NOT NULL,
    minutes             REAL NOT NULL DEFAULT 0,
    matches             INTEGER NOT NULL DEFAULT 0,
    starts              INTEGER NOT NULL DEFAULT 0,
    position            TEXT,
    shots               REAL NOT NULL DEFAULT 0,
    goals               REAL NOT NULL DEFAULT 0,
    xg                  REAL NOT NULL DEFAULT 0,
    passes              REAL NOT NULL DEFAULT 0,
    pass_ok             REAL NOT NULL DEFAULT 0,
    drib_att            REAL NOT NULL DEFAULT 0,
    drib_ok             REAL NOT NULL DEFAULT 0,
    carries             REAL NOT NULL DEFAULT 0,
    pressures           REAL NOT NULL DEFAULT 0,
    duels_w             REAL NOT NULL DEFAULT 0,
    duels_l             REAL NOT NULL DEFAULT 0,
    interceptions       REAL NOT NULL DEFAULT 0,
    recoveries          REAL NOT NULL DEFAULT 0,
    blocks              REAL NOT NULL DEFAULT 0,
    clearances          REAL NOT NULL DEFAULT 0,
    fouls_w             REAL NOT NULL DEFAULT 0,
    fouls_c             REAL NOT NULL DEFAULT 0,
    shots_p90           REAL,
    goals_p90           REAL,
    xg_p90              REAL,
    passes_p90          REAL,
    drib_att_p90        REAL,
    drib_ok_p90         REAL,
    carries_p90         REAL,
    pressures_p90       REAL,
    duels_w_p90         REAL,
    interceptions_p90   REAL,
    recoveries_p90      REAL,
    blocks_p90          REAL,
    clearances_p90      REAL,
    pass_pct            REAL,
    player_id           INTEGER REFERENCES players (player_id),
    player_name         TEXT,
    tm_club             TEXT,
    method              TEXT,
    value_date          DATE,
    market_value_in_eur BIGINT,
    PRIMARY KEY (league_season, sb_player, sb_team)
);

CREATE INDEX IF NOT EXISTS idx_player_season_player
    ON player_season (player_id);
CREATE INDEX IF NOT EXISTS idx_player_season_league
    ON player_season (league_season);
