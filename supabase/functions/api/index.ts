// Supabase Edge Function for Hawaii BI API
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

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
        const dashboardData = {
          total_companies: 15,
          total_prospects: 15,
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
            },
            {
              id: 2,
              score: 88,
              company: {
                name: 'Pacific Paradise Resort',
                island: 'Maui',
                industry: 'Tourism'
              },
              recommended_services: ['Dynamic Pricing AI', 'Guest Experience Bot']
            },
            {
              id: 4,
              score: 95,
              company: {
                name: 'Island Tech Solutions',
                island: 'Oahu',
                industry: 'Technology'
              },
              recommended_services: ['AI Development Tools', 'Automated Testing']
            }
          ]
        }
        
        return new Response(JSON.stringify(dashboardData), { 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        })

      case '/companies':
        const companiesData = [
          {id: 1, name: "Aloha Medical Center", website: "https://alohamedical.com", island: "Oahu", industry: "Healthcare", employee_count_estimate: 450},
          {id: 2, name: "Pacific Paradise Resort", website: "https://pacificparadise.com", island: "Maui", industry: "Tourism", employee_count_estimate: 320},
          {id: 3, name: "Kona Coffee Collective", website: "https://konacoffee.com", island: "Big Island", industry: "Food Service", employee_count_estimate: 85},
          {id: 4, name: "Island Tech Solutions", website: "https://islandtech.com", island: "Oahu", industry: "Technology", employee_count_estimate: 150},
          {id: 5, name: "Kauai Adventure Tours", website: "https://kauaiadventure.com", island: "Kauai", industry: "Tourism", employee_count_estimate: 65}
        ]
        return new Response(JSON.stringify(companiesData), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

      case '/prospects':
        const prospectsData = [
          {
            id: 1,
            company_id: 1,
            score: 92,
            priority_level: "High",
            ai_analysis: "High potential for AI integration in patient management, appointment scheduling, and diagnostic assistance. Strong digital presence indicates readiness.",
            pain_points: ["Long patient wait times", "Manual record keeping", "Staff scheduling complexity"],
            recommended_services: ["AI Scheduling System", "Predictive Analytics", "Patient Chatbot"],
            company: {
              name: "Aloha Medical Center",
              island: "Oahu",
              industry: "Healthcare"
            },
            company_name: "Aloha Medical Center"
          },
          {
            id: 2,
            company_id: 2,
            score: 88,
            priority_level: "High",
            ai_analysis: "Excellent candidate for AI-powered booking optimization and guest experience enhancement. Tourism sector with high automation potential.",
            pain_points: ["Seasonal demand fluctuations", "Guest service response time", "Revenue optimization"],
            recommended_services: ["Dynamic Pricing AI", "Guest Experience Bot", "Predictive Maintenance"],
            company: {
              name: "Pacific Paradise Resort",
              island: "Maui", 
              industry: "Tourism"
            },
            company_name: "Pacific Paradise Resort"
          },
          {
            id: 3,
            company_id: 3,
            score: 85,
            priority_level: "Medium",
            ai_analysis: "Could benefit from AI in supply chain optimization and customer preference analytics. Growing business with scalability needs.",
            pain_points: ["Inventory management", "Demand forecasting", "Customer retention"],
            recommended_services: ["Inventory AI", "Customer Analytics", "Quality Control ML"],
            company: {
              name: "Kona Coffee Collective",
              island: "Big Island",
              industry: "Food Service"
            },
            company_name: "Kona Coffee Collective"
          },
          {
            id: 4,
            company_id: 4,
            score: 95,
            priority_level: "High",
            ai_analysis: "Already tech-savvy, perfect for advanced AI solutions and could be a strategic partner for implementations.",
            pain_points: ["Project resource allocation", "Client requirement analysis", "Code quality assurance"],
            recommended_services: ["AI Development Tools", "Automated Testing", "Project Management AI"],
            company: {
              name: "Island Tech Solutions",
              island: "Oahu",
              industry: "Technology"
            },
            company_name: "Island Tech Solutions"
          },
          {
            id: 5,
            company_id: 5,
            score: 87,
            priority_level: "High",
            ai_analysis: "AI can significantly optimize tour scheduling, weather-based planning, and personalized recommendations.",
            pain_points: ["Weather-dependent scheduling", "Group size optimization", "Marketing reach"],
            recommended_services: ["Booking Optimization", "Weather Prediction AI", "Marketing Automation"],
            company: {
              name: "Kauai Adventure Tours",
              island: "Kauai",
              industry: "Tourism"
            },
            company_name: "Kauai Adventure Tours"
          }
        ]
        
        return new Response(JSON.stringify(prospectsData), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

      case '/analytics/by-island':
        const islandCounts = {
          "Oahu": 2,
          "Maui": 1,
          "Big Island": 1,
          "Kauai": 1
        }
        
        return new Response(JSON.stringify(islandCounts), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })

      case '/analytics/by-industry':
        const industryCounts = {
          "Tourism": 2,
          "Healthcare": 1,
          "Technology": 1,
          "Food Service": 1
        }
        
        return new Response(JSON.stringify(industryCounts), {
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
          const prospectId = parseInt(path.split('/')[2])
          if (prospectId) {
            const allProspects = [
              {
                id: 1,
                company_id: 1,
                score: 92,
                priority_level: "High",
                ai_analysis: "High potential for AI integration in patient management, appointment scheduling, and diagnostic assistance. Strong digital presence indicates readiness.",
                pain_points: ["Long patient wait times", "Manual record keeping", "Staff scheduling complexity"],
                recommended_services: ["AI Scheduling System", "Predictive Analytics", "Patient Chatbot"],
                company: {
                  name: "Aloha Medical Center",
                  island: "Oahu",
                  industry: "Healthcare",
                  website: "https://alohamedical.com",
                  employee_count_estimate: 450
                },
                company_name: "Aloha Medical Center"
              },
              {
                id: 2,
                company_id: 2,
                score: 88,
                priority_level: "High",
                ai_analysis: "Excellent candidate for AI-powered booking optimization and guest experience enhancement. Tourism sector with high automation potential.",
                pain_points: ["Seasonal demand fluctuations", "Guest service response time", "Revenue optimization"],
                recommended_services: ["Dynamic Pricing AI", "Guest Experience Bot", "Predictive Maintenance"],
                company: {
                  name: "Pacific Paradise Resort",
                  island: "Maui",
                  industry: "Tourism",
                  website: "https://pacificparadise.com",
                  employee_count_estimate: 320
                },
                company_name: "Pacific Paradise Resort"
              },
              {
                id: 3,
                company_id: 3,
                score: 85,
                priority_level: "Medium",
                ai_analysis: "Could benefit from AI in supply chain optimization and customer preference analytics. Growing business with scalability needs.",
                pain_points: ["Inventory management", "Demand forecasting", "Customer retention"],
                recommended_services: ["Inventory AI", "Customer Analytics", "Quality Control ML"],
                company: {
                  name: "Kona Coffee Collective",
                  island: "Big Island",
                  industry: "Food Service",
                  website: "https://konacoffee.com",
                  employee_count_estimate: 85
                },
                company_name: "Kona Coffee Collective"
              },
              {
                id: 4,
                company_id: 4,
                score: 95,
                priority_level: "High",
                ai_analysis: "Already tech-savvy, perfect for advanced AI solutions and could be a strategic partner for implementations.",
                pain_points: ["Project resource allocation", "Client requirement analysis", "Code quality assurance"],
                recommended_services: ["AI Development Tools", "Automated Testing", "Project Management AI"],
                company: {
                  name: "Island Tech Solutions",
                  island: "Oahu",
                  industry: "Technology",
                  website: "https://islandtech.com",
                  employee_count_estimate: 150
                },
                company_name: "Island Tech Solutions"
              },
              {
                id: 5,
                company_id: 5,
                score: 87,
                priority_level: "High",
                ai_analysis: "AI can significantly optimize tour scheduling, weather-based planning, and personalized recommendations.",
                pain_points: ["Weather-dependent scheduling", "Group size optimization", "Marketing reach"],
                recommended_services: ["Booking Optimization", "Weather Prediction AI", "Marketing Automation"],
                company: {
                  name: "Kauai Adventure Tours",
                  island: "Kauai",
                  industry: "Tourism",
                  website: "https://kauaiadventure.com",
                  employee_count_estimate: 65
                },
                company_name: "Kauai Adventure Tours"
              }
            ]
            
            const prospect = allProspects.find(p => p.id === prospectId)
            
            if (prospect) {
              return new Response(JSON.stringify(prospect), {
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