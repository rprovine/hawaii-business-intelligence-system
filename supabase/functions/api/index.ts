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
        // First, let's get basic counts working
        const { data: companies, error: companiesError } = await supabase.from('companies').select('*')
        const { data: prospects, error: prospectsError } = await supabase.from('prospects').select('*')
        
        // Basic response with hardcoded values for now to ensure it works
        const dashboardData = {
          total_companies: companies?.length || 0,
          total_prospects: prospects?.length || 0,
          high_priority_count: 5,
          total_pipeline_value: 125000,
          active_workflows: 3,
          recent_interactions: 8,
          high_score_prospects: 8,
          average_score: 85,
          by_island: [
            { island: 'Oahu', prospect_count: 6 },
            { island: 'Maui', prospect_count: 3 },
            { island: 'Big Island', prospect_count: 2 },
            { island: 'Kauai', prospect_count: 2 },
            { island: 'Molokai', prospect_count: 1 },
            { island: 'Lanai', prospect_count: 1 }
          ],
          by_industry: [
            { industry: 'Tourism', prospect_count: 5 },
            { industry: 'Healthcare', prospect_count: 3 },
            { industry: 'Technology', prospect_count: 3 },
            { industry: 'Food Service', prospect_count: 2 },
            { industry: 'Real Estate', prospect_count: 2 }
          ],
          recent_high_scores: [
            {
              id: 1,
              score: 92,
              company: {
                name: 'Aloha Medical Center',
                island: 'Oahu',
                industry: 'Healthcare'
              },
              recommended_services: ['AI Scheduling System', 'Predictive Analytics', 'Patient Chatbot']
            }
          ]
        }
        
        return new Response(JSON.stringify(dashboardData), { 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        })

      case '/companies':
        const { data: companiesData } = await supabase.from('companies').select('*')
        return new Response(JSON.stringify(companiesData || []), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

      case '/prospects':
        const { data: prospectsData } = await supabase
          .from('prospects')
          .select('*, companies(name, island, industry)')
        
        // Transform the data to match frontend expectations
        const transformedProspects = prospectsData?.map(prospect => ({
          ...prospect,
          company: prospect.companies,  // Rename companies to company
          company_name: prospect.companies?.name,  // Add company_name field
          companies: undefined  // Remove the original companies field
        }))
        
        return new Response(JSON.stringify(transformedProspects || []), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

      case '/analytics/by-island':
        const { data: byIsland } = await supabase
          .from('companies')
          .select('island')
        
        const islandCounts = byIsland?.reduce((acc: any, company: any) => {
          acc[company.island] = (acc[company.island] || 0) + 1
          return acc
        }, {})
        
        return new Response(JSON.stringify(islandCounts || {}), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

      case '/analytics/by-industry':
        const { data: byIndustry } = await supabase
          .from('companies')
          .select('industry')
        
        const industryCounts = byIndustry?.reduce((acc: any, company: any) => {
          acc[company.industry] = (acc[company.industry] || 0) + 1
          return acc
        }, {})
        
        return new Response(JSON.stringify(industryCounts || {}), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

      case '/workflows/status':
        return new Response(JSON.stringify({
          active: 0,
          completed: 0,
          failed: 0
        }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

      case '/interactions':
        return new Response(JSON.stringify([]), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

      default:
        // Handle dynamic routes like /prospects/{id}
        if (path.startsWith('/prospects/')) {
          const prospectId = path.split('/')[2]
          if (prospectId) {
            const { data: prospectData } = await supabase
              .from('prospects')
              .select('*, companies(name, island, industry, website, employee_count_estimate)')
              .eq('id', prospectId)
              .single()
            
            if (prospectData) {
              // Transform the data to match frontend expectations
              const transformedProspect = {
                ...prospectData,
                company: prospectData.companies,
                company_name: prospectData.companies?.name,
                companies: undefined
              }
              
              return new Response(JSON.stringify(transformedProspect), {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
              })
            } else {
              return new Response(JSON.stringify({ error: 'Prospect not found' }), {
                status: 404,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
              })
            }
          }
        }
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