CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    avatar VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE games (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    category_id UUID REFERENCES categories(id),
    is_multiplayer BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE favorites (
    user_id UUID REFERENCES users(id),
    game_id UUID REFERENCES games(id),
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, game_id)
);

CREATE TABLE friendships (
    user1_id UUID REFERENCES users(id),
    user2_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user1_id, user2_id),
    CHECK (user1_id < friendships.user2_id)
);

CREATE TABLE upvotes (
    user1_id UUID REFERENCES users(id),
    game_id UUID REFERENCES games(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user1_id, game_id)
);

CREATE TABLE game_activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    game_id UUID REFERENCES games(id),
    played_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    duration INTEGER NOT NULL, -- seconds
    UNIQUE(user_id, game_id, played_at)
);

-- Users indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- Games indexes
CREATE INDEX idx_games_title ON games(title);
CREATE INDEX idx_games_category_id ON games(category_id);
CREATE INDEX idx_games_is_multiplayer ON games(is_multiplayer);

-- Activities indexes
CREATE INDEX idx_game_activities_user_game ON game_activities(user_id, game_id);
CREATE INDEX idx_game_activities_played_at ON game_activities(played_at DESC);

-- Composite indexes for frequent queries
CREATE INDEX idx_favorites_user_added ON favorites(user_id, added_at DESC);
CREATE INDEX idx_upvotes_game_count ON upvotes(game_id, created_at DESC);