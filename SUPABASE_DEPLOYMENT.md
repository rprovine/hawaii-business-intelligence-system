# Supabase Deployment Guide

## Step 1: Set up Supabase Project

1. Go to [app.supabase.com](https://app.supabase.com)
2. Create a new project or use existing one
3. Note your project URL and anon key

## Step 2: Run Database Migration

1. Go to SQL Editor in Supabase Dashboard
2. Copy and paste the contents of `supabase/migrations/001_initial_schema.sql`
3. Click "Run" to create tables and seed data

## Step 3: Deploy Edge Function

### Option A: Using Supabase CLI
```bash
# Install Supabase CLI if not already installed
brew install supabase/tap/supabase

# Login to Supabase
supabase login

# Link to your project
supabase link --project-ref YOUR_PROJECT_REF

# Deploy the edge function
supabase functions deploy api --no-verify-jwt
```

### Option B: Using Dashboard
1. Go to Edge Functions in Supabase Dashboard
2. Click "New Function"
3. Name it "api"
4. Copy the contents of `supabase/functions/api/index.ts`
5. Deploy

## Step 4: Update Frontend Environment

Create `.env` file in frontend directory:
```env
REACT_APP_SUPABASE_URL=https://YOUR_PROJECT.supabase.co
REACT_APP_SUPABASE_ANON_KEY=YOUR_ANON_KEY
REACT_APP_API_URL=https://YOUR_PROJECT.supabase.co/functions/v1/api
```

## Step 5: Update Frontend API Service

The frontend api.ts file needs to be updated to use the Supabase Edge Function URL.

## URLs After Deployment

- Database: Managed by Supabase (PostgreSQL)
- API: `https://YOUR_PROJECT.supabase.co/functions/v1/api`
- Frontend: Keep on Vercel at current URL

## Testing

Test the API endpoints:
```bash
# Test health endpoint
curl https://YOUR_PROJECT.supabase.co/functions/v1/api/health

# Test dashboard endpoint
curl https://YOUR_PROJECT.supabase.co/functions/v1/api/analytics/dashboard
```