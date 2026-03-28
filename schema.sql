CREATE DATABASE IF NOT EXISTS dating_app;
USE dating_app;

CREATE TABLE user (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(120)    NOT NULL UNIQUE,
    username        VARCHAR(80)     NOT NULL UNIQUE,
    password_hash   VARCHAR(255)    NOT NULL,
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE interest (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES "user"(id) ON DELETE CASCADE,
    first_name VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50)     NOT NULL,
    date_of_birth   DATE            NOT NULL,
    gender VARCHAR(20) NOT NULL,
    looking_for VARCHAR(20)     NOT NULL DEFAULT 'any',
    bio TEXT,
    location VARCHAR(100),
    profile_photo VARCHAR(255),
    occupation VARCHAR(100),
    education_level VARCHAR(50),   
    height_cm SMALLINT,
    relationship_goal VARCHAR(50),  
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profile_interest (
    profile_id  INTEGER NOT NULL REFERENCES profile(id)   ON DELETE CASCADE,
    interest_id INTEGER NOT NULL REFERENCES interest(id)  ON DELETE CASCADE,
    PRIMARY KEY (profile_id, interest_id)
);

CREATE TABLE match (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    receiver_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'liked',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_match_pair UNIQUE (sender_id, receiver_id),
    CONSTRAINT no_self_match CHECK (sender_id <> receiver_id)
);

CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES match(id)  ON DELETE CASCADE,
    sender_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
 
 CREATE TABLE favourite (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    profile_id INTEGER NOT NULL REFERENCES profile(id) ON DELETE CASCADE,
    saved_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_favourite UNIQUE (user_id, profile_id)
);
 