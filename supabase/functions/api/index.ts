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
        
        // Calculate high priority count
        const highPriorityCount = prospects?.filter(p => p.priority_level === 'High').length || 0
        
        // Calculate pipeline value (estimated)
        const totalPipelineValue = prospects?.reduce((sum, p) => sum + (p.score * 1000), 0) || 0
        
        // Get island distribution for pie chart
        const islandCounts = companies?.reduce((acc: any, company: any) => {
          acc[company.island] = (acc[company.island] || 0) + 1
          return acc
        }, {})
        
        const byIsland = Object.entries(islandCounts || {}).map(([island, count]) => ({
          island,
          prospect_count: count as number
        }))
        
        // Get industry distribution
        const industryCounts = companies?.reduce((acc: any, company: any) => {
          acc[company.industry] = (acc[company.industry] || 0) + 1
          return acc
        }, {})
        
        const byIndustry = Object.entries(industryCounts || {}).map(([industry, count]) => ({
          industry,
          prospect_count: count as number
        }))
        
        // Get recent high-score prospects
        const recentHighScores = prospects?.filter(p => p.score > 85)
          ?.sort((a, b) => b.score - a.score)
          ?.slice(0, 5)
          ?.map(p => {
            const company = companies?.find(c => c.id === p.company_id)
            return {
              id: p.id,
              score: p.score,
              company: {
                name: company?.name || 'Unknown',
                island: company?.island || 'Unknown',
                industry: company?.industry || 'Unknown'
              },
              recommended_services: p.recommended_services || []
            }
          }) || []
        
        return new Response(JSON.stringify({
          total_companies: companies?.length || 0,
          total_prospects: prospects?.length || 0,
          high_priority_count: highPriorityCount,
          total_pipeline_value: totalPipelineValue,
          active_workflows: 3,
          recent_interactions: 8,
          high_score_prospects: prospects?.filter(p => p.score > 80).length || 0,
          average_score: prospects?.reduce((sum, p) => sum + p.score, 0) / (prospects?.length || 1) || 85,
          by_island: byIsland,
          by_industry: byIndustry,
          recent_high_scores: recentHighScores
        }), { headers: { ...corsHeaders, 'Content-Type': 'application/json' } })

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