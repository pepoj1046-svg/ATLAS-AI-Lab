-- ATLAS initial schema; already applied to the dedicated ATLAS Supabase project.
-- Keep tables closed until user authentication and ownership-based RLS are designed.
create table if not exists public.atlas_experiments (
 id uuid primary key default gen_random_uuid(), code text not null unique,
 title text not null, hypothesis text not null,
 status text not null default 'planned' check(status in ('planned','running','completed','failed')),
 created_at timestamptz not null default now()
);
create table if not exists public.atlas_attempts (
 id uuid primary key default gen_random_uuid(),
 experiment_id uuid not null references public.atlas_experiments(id) on delete restrict,
 arm text not null check(arm in ('baseline','memory')),
 task_key text not null, candidate_json jsonb not null default '{}'::jsonb,
 created_at timestamptz not null default now(), unique(experiment_id,arm,task_key)
);
create table if not exists public.atlas_evaluations (
 id uuid primary key default gen_random_uuid(),
 attempt_id uuid not null unique references public.atlas_attempts(id) on delete restrict,
 evaluator_version text not null, passed boolean not null,
 evidence_json jsonb not null default '{}'::jsonb,
 evaluated_at timestamptz not null default now()
);
create table if not exists public.atlas_lessons (
 id uuid primary key default gen_random_uuid(), lesson_key text not null unique,
 operation text not null, rule_json jsonb not null, evidence_json jsonb not null,
 verified_at timestamptz not null default now()
);
alter table public.atlas_experiments enable row level security;
alter table public.atlas_attempts enable row level security;
alter table public.atlas_evaluations enable row level security;
alter table public.atlas_lessons enable row level security;
revoke all on public.atlas_experiments, public.atlas_attempts, public.atlas_evaluations, public.atlas_lessons from anon, authenticated;
