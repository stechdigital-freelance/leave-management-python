CREATE TABLE public.users (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE DEFAULT uuidv7(),
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT check_user_role CHECK (role IN ('user', 'supervisor', 'admin', 'superAdmin'))
);

CREATE TABLE public.departments (
    id BIGSERIAL PRIMARY KEY,       -- auto-incrementing ID (serial)
    name VARCHAR(255) NOT NULL UNIQUE,
    code VARCHAR(50) UNIQUE,        -- optional short code
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE, -- tracks active/inactive departments
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE public.department_admins (
    id BIGSERIAL PRIMARY KEY,               -- auto-incrementing ID (serial)
    department_id BIGINT NOT NULL REFERENCES departments(id) ON DELETE CASCADE,
    user_id int NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_active BOOLEAN DEFAULT TRUE,         -- tracks active/inactive admins
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(department_id, user_id)
);
