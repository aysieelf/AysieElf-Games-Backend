-- Create enum type "role"
CREATE TYPE "role" AS ENUM ('USER', 'ADMIN');
-- Create "blacklisted_tokens" table
CREATE TABLE "blacklisted_tokens" ("token" character varying NOT NULL, "blacklisted_at" timestamptz NOT NULL DEFAULT now(), "expires_at" timestamptz NOT NULL, PRIMARY KEY ("token"));
-- Create index "ix_blacklisted_tokens_token" to table: "blacklisted_tokens"
CREATE INDEX "ix_blacklisted_tokens_token" ON "blacklisted_tokens" ("token");
-- Create "categories" table
CREATE TABLE "categories" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "name" character varying(50) NOT NULL, "slug" character varying(50) NOT NULL, "description" text NULL, PRIMARY KEY ("id"));
-- Create index "ix_categories_id" to table: "categories"
CREATE INDEX "ix_categories_id" ON "categories" ("id");
-- Create index "ix_categories_name" to table: "categories"
CREATE UNIQUE INDEX "ix_categories_name" ON "categories" ("name");
-- Create index "ix_categories_slug" to table: "categories"
CREATE UNIQUE INDEX "ix_categories_slug" ON "categories" ("slug");
-- Create "games" table
CREATE TABLE "games" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "title" character varying(100) NOT NULL, "slug" character varying(100) NOT NULL, "icon" character varying(255) NULL, "description" text NULL, "is_multiplayer" boolean NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "category_id" uuid NOT NULL, PRIMARY KEY ("id"), CONSTRAINT "games_category_id_fkey" FOREIGN KEY ("category_id") REFERENCES "categories" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION);
-- Create index "ix_games_category_id" to table: "games"
CREATE INDEX "ix_games_category_id" ON "games" ("category_id");
-- Create index "ix_games_id" to table: "games"
CREATE INDEX "ix_games_id" ON "games" ("id");
-- Create index "ix_games_is_multiplayer" to table: "games"
CREATE INDEX "ix_games_is_multiplayer" ON "games" ("is_multiplayer");
-- Create index "ix_games_slug" to table: "games"
CREATE UNIQUE INDEX "ix_games_slug" ON "games" ("slug");
-- Create index "ix_games_title" to table: "games"
CREATE UNIQUE INDEX "ix_games_title" ON "games" ("title");
-- Create "users" table
CREATE TABLE "users" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "username" character varying(50) NOT NULL, "slug" character varying(50) NOT NULL, "email" character varying(320) NOT NULL, "password_hash" character varying(60) NOT NULL, "role" "role" NOT NULL, "avatar" character varying(255) NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "last_login" timestamptz NULL, "is_verified" boolean NOT NULL, PRIMARY KEY ("id"));
-- Create index "ix_users_email" to table: "users"
CREATE UNIQUE INDEX "ix_users_email" ON "users" ("email");
-- Create index "ix_users_id" to table: "users"
CREATE INDEX "ix_users_id" ON "users" ("id");
-- Create index "ix_users_slug" to table: "users"
CREATE UNIQUE INDEX "ix_users_slug" ON "users" ("slug");
-- Create index "ix_users_username" to table: "users"
CREATE UNIQUE INDEX "ix_users_username" ON "users" ("username");
-- Create "favorites" table
CREATE TABLE "favorites" ("user_id" uuid NOT NULL, "game_id" uuid NOT NULL, "added_at" timestamptz NULL DEFAULT now(), PRIMARY KEY ("user_id", "game_id"), CONSTRAINT "favorites_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "games" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION, CONSTRAINT "favorites_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION);
-- Create "friendships" table
CREATE TABLE "friendships" ("user1_id" uuid NOT NULL, "user2_id" uuid NOT NULL, "created_at" timestamptz NULL DEFAULT now(), PRIMARY KEY ("user1_id", "user2_id"), CONSTRAINT "friendships_user1_id_fkey" FOREIGN KEY ("user1_id") REFERENCES "users" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION, CONSTRAINT "friendships_user2_id_fkey" FOREIGN KEY ("user2_id") REFERENCES "users" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION);
-- Create "game_activities" table
CREATE TABLE "game_activities" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "user_id" uuid NOT NULL, "game_id" uuid NOT NULL, "played_at" timestamptz NOT NULL DEFAULT now(), PRIMARY KEY ("id"), CONSTRAINT "uix_activity" UNIQUE ("user_id", "game_id", "played_at"), CONSTRAINT "game_activities_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "games" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION, CONSTRAINT "game_activities_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION);
-- Create index "ix_game_activities_id" to table: "game_activities"
CREATE INDEX "ix_game_activities_id" ON "game_activities" ("id");
-- Create "upvotes" table
CREATE TABLE "upvotes" ("user_id" uuid NOT NULL, "game_id" uuid NOT NULL, "created_at" timestamptz NULL DEFAULT now(), PRIMARY KEY ("user_id", "game_id"), CONSTRAINT "upvotes_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "games" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION, CONSTRAINT "upvotes_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION);
