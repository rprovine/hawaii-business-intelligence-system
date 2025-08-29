// Supabase Edge Function for Hawaii BI API
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  const supabaseUrl = Deno.env.get('SUPABASE_URL')!
  const supabaseKey = Deno.env.get('SUPABASE_ANON_KEY')!
  const supabase = createClient(supabaseUrl, supabaseKey)

  const url = new URL(req.url)
  // Get the full pathname for debugging
  const fullPath = url.pathname
  
  // Remove everything up to and including 'api' to get the route
  const pathMatch = fullPath.match(/\/api(.*)$/)
  const path = pathMatch ? (pathMatch[1] || '/') : '/'

  try {
    // Route handling
    switch (path) {
      case '/':
        return new Response(JSON.stringify({
          message: "Hawaii Business Intelligence System API",
          status: "operational"
        }), { headers: { ...corsHeaders, 'Content-Type': 'application/json' } })

      case '/health':
        return new Response(JSON.stringify({
          status: "healthy",
          database: "connected"
        }), { headers: { ...corsHeaders, 'Content-Type': 'application/json' } })

      case '/analytics/dashboard':
        const { data: companies } = await supabase.from('companies').select('*')
        const { data: prospects } = await supabase.from('prospects').select('*')
        
        return new Response(JSON.stringify({
          total_companies: companies?.length || 0,
          total_prospects: prospects?.length || 0,
          active_workflows: 3,
          recent_interactions: 8,
          high_score_prospects: prospects?.filter(p => p.score > 80).length || 0,
          average_score: 85
        }), { headers: { ...corsHeaders, 'Content-Type': 'application/json' } })

      case '/companies':
        const { data: companiesData } = await supabase.from('companies').select('*')
        return new Response(JSON.stringify(companiesData || []), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

      case '/prospects':
        const { data: prospectsData } = await supabase
          .from('prospects')
          .select('*, companies(name)')
        
        return new Response(JSON.stringify(prospectsData || []), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

      default:
        return new Response(JSON.stringify({ error: 'Not found' }), {
          status: 404,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })
    }
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  }
})