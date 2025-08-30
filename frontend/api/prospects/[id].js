// Vercel serverless function for individual prospect data
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const { id } = req.query;
  const prospectId = parseInt(id);

  const allProspects = [
    {
      id: 1,
      company_id: 1,
      score: 92,
      priority_level: "High",
      ai_analysis: "High potential for AI integration in patient management, appointment scheduling, and diagnostic assistance. Strong digital presence indicates readiness.",
      pain_points: ["Long patient wait times", "Manual record keeping", "Staff scheduling complexity"],
      recommended_services: ["AI Scheduling System", "Predictive Analytics", "Patient Chatbot"],
      technology_readiness: "High",
      last_analyzed: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2).toISOString(),
      decision_makers: [
        {
          name: "Dr. Sarah Chen",
          title: "Chief Medical Officer",
          email: "s.chen@alohamedical.com",
          phone: "(808) 555-0100",
          linkedin_url: "https://linkedin.com/in/sarahchen"
        },
        {
          name: "Michael Tanaka",
          title: "IT Director",
          email: "m.tanaka@alohamedical.com",
          phone: "(808) 555-0101"
        }
      ],
      company: {
        name: "Aloha Medical Center",
        island: "Oahu",
        industry: "Healthcare",
        website: "https://alohamedical.com",
        employee_count_estimate: 450,
        annual_revenue_estimate: 125000000,
        founded_date: "1998",
        source: "Google Business Profile",
        description: "Leading healthcare provider in Honolulu specializing in advanced medical treatments and patient care. Recently expanded their facilities and looking to modernize operations."
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
      technology_readiness: "Medium-High",
      last_analyzed: new Date(Date.now() - 1000 * 60 * 60 * 24 * 3).toISOString(),
      decision_makers: [
        {
          name: "Jennifer Walsh",
          title: "General Manager",
          email: "j.walsh@pacificparadise.com",
          phone: "(808) 555-0200"
        }
      ],
      company: {
        name: "Pacific Paradise Resort",
        island: "Maui",
        industry: "Tourism",
        website: "https://pacificparadise.com",
        employee_count_estimate: 320,
        annual_revenue_estimate: 85000000,
        founded_date: "2005",
        source: "Yelp Business",
        description: "Award-winning beachfront resort offering luxury accommodations and world-class amenities. Looking to enhance guest experience through technology."
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
      technology_readiness: "Medium",
      last_analyzed: new Date(Date.now() - 1000 * 60 * 60 * 24 * 5).toISOString(),
      decision_makers: [
        {
          name: "David Kim",
          title: "Owner/CEO",
          email: "d.kim@konacoffee.com",
          phone: "(808) 555-0300"
        }
      ],
      company: {
        name: "Kona Coffee Collective",
        island: "Big Island",
        industry: "Food Service",
        website: "https://konacoffee.com",
        employee_count_estimate: 85,
        annual_revenue_estimate: 12000000,
        founded_date: "2010",
        source: "LinkedIn Company",
        description: "Sustainable coffee producer and distributor specializing in premium Kona coffee. Expanding operations and seeking efficiency improvements."
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
      technology_readiness: "Very High",
      last_analyzed: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
      decision_makers: [
        {
          name: "Robert Chang",
          title: "CTO",
          email: "r.chang@islandtech.com",
          phone: "(808) 555-0400",
          linkedin_url: "https://linkedin.com/in/robertchang"
        }
      ],
      company: {
        name: "Island Tech Solutions",
        island: "Oahu",
        industry: "Technology",
        website: "https://islandtech.com",
        employee_count_estimate: 150,
        annual_revenue_estimate: 45000000,
        founded_date: "2015",
        source: "Pacific Business News",
        description: "Leading technology consulting firm specializing in digital transformation for Hawaii businesses. Strong expertise in cloud and AI solutions."
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
      technology_readiness: "Medium",
      last_analyzed: new Date(Date.now() - 1000 * 60 * 60 * 24 * 4).toISOString(),
      decision_makers: [
        {
          name: "Lisa Nakamura",
          title: "Operations Director",
          email: "l.nakamura@kauaiadventure.com",
          phone: "(808) 555-0500"
        }
      ],
      company: {
        name: "Kauai Adventure Tours",
        island: "Kauai",
        industry: "Tourism",
        website: "https://kauaiadventure.com",
        employee_count_estimate: 65,
        annual_revenue_estimate: 8000000,
        founded_date: "2008",
        source: "Google Business Profile",
        description: "Premier adventure tour operator offering hiking, kayaking, and helicopter tours. Focused on sustainable tourism and enhancing customer experience."
      },
      company_name: "Kauai Adventure Tours"
    }
  ];

  const prospect = allProspects.find(p => p.id === prospectId);

  if (prospect) {
    res.status(200).json(prospect);
  } else {
    res.status(404).json({ error: 'Prospect not found' });
  }
}