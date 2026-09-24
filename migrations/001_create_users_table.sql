CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    google_id TEXT UNIQUE NOT NULL,

    name TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    avatar_url TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);