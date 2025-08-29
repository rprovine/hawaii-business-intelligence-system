// Mock data for testing the frontend without backend
export const mockDashboardData = {
  total_prospects: 156,
  high_priority_count: 42,
  total_pipeline_value: 2850000,
  average_score: 78,
  by_island: [
    { island: 'Oahu', prospect_count: 68 },
    { island: 'Maui', prospect_count: 34 },
    { island: 'Big Island', prospect_count: 28 },
    { island: 'Kauai', prospect_count: 18 },
    { island: 'Molokai', prospect_count: 5 },
    { island: 'Lanai', prospect_count: 3 }
  ],
  by_industry: [
    { industry: 'Tourism & Hospitality', prospect_count: 45 },
    { industry: 'Construction', prospect_count: 32 },
    { industry: 'Healthcare', prospect_count: 28 },
    { industry: 'Retail', prospect_count: 24 },
    { industry: 'Technology', prospect_count: 18 },
    { industry: 'Agriculture', prospect_count: 9 }
  ],
  recent_high_scores: [
    {
      id: '1',
      score: 95,
      company: {
        name: 'Aloha Resorts International',
        island: 'Maui',
        industry: 'Tourism & Hospitality'
      },
      recommended_services: ['Workforce Development', 'Business Consulting', 'Digital Transformation']
    },
    {
      id: '2',
      score: 92,
      company: {
        name: 'Pacific Construction Group',
        island: 'Oahu',
        industry: 'Construction'
      },
      recommended_services: ['Project Management', 'Safety Training', 'Equipment Optimization']
    },
    {
      id: '3',
      score: 89,
      company: {
        name: 'Island Health Systems',
        island: 'Big Island',
        industry: 'Healthcare'
      },
      recommended_services: ['Healthcare IT', 'Staff Training', 'Process Improvement']
    },
    {
      id: '4',
      score: 87,
      company: {
        name: 'Kauai Tech Innovations',
        island: 'Kauai',
        industry: 'Technology'
      },
      recommended_services: ['IT Consulting', 'Cybersecurity', 'Cloud Migration']
    },
    {
      id: '5',
      score: 85,
      company: {
        name: 'Sunset Retail Partners',
        island: 'Oahu',
        industry: 'Retail'
      },
      recommended_services: ['E-commerce Strategy', 'Inventory Management', 'Customer Analytics']
    }
  ]
};

export const mockProspectsData = {
  prospects: [
    {
      id: '1',
      company: {
        name: 'Aloha Resorts International',
        island: 'Maui',
        industry: 'Tourism & Hospitality',
        size: 'Large',
        annual_revenue: 50000000
      },
      score: 95,
      priority_level: 'High',
      status: 'active',
      last_contact: '2024-01-15',
      estimated_deal_value: 250000,
      recommended_services: ['Workforce Development', 'Business Consulting', 'Digital Transformation']
    },
    {
      id: '2',
      company: {
        name: 'Pacific Construction Group',
        island: 'Oahu',
        industry: 'Construction',
        size: 'Medium',
        annual_revenue: 25000000
      },
      score: 92,
      priority_level: 'High',
      status: 'active',
      last_contact: '2024-01-10',
      estimated_deal_value: 180000,
      recommended_services: ['Project Management', 'Safety Training', 'Equipment Optimization']
    },
    {
      id: '3',
      company: {
        name: 'Island Health Systems',
        island: 'Big Island',
        industry: 'Healthcare',
        size: 'Large',
        annual_revenue: 75000000
      },
      score: 89,
      priority_level: 'High',
      status: 'active',
      last_contact: '2024-01-08',
      estimated_deal_value: 320000,
      recommended_services: ['Healthcare IT', 'Staff Training', 'Process Improvement']
    },
    {
      id: '4',
      company: {
        name: 'Kauai Tech Innovations',
        island: 'Kauai',
        industry: 'Technology',
        size: 'Small',
        annual_revenue: 5000000
      },
      score: 87,
      priority_level: 'Medium',
      status: 'active',
      last_contact: '2024-01-12',
      estimated_deal_value: 95000,
      recommended_services: ['IT Consulting', 'Cybersecurity', 'Cloud Migration']
    },
    {
      id: '5',
      company: {
        name: 'Sunset Retail Partners',
        island: 'Oahu',
        industry: 'Retail',
        size: 'Medium',
        annual_revenue: 15000000
      },
      score: 85,
      priority_level: 'Medium',
      status: 'active',
      last_contact: '2024-01-05',
      estimated_deal_value: 120000,
      recommended_services: ['E-commerce Strategy', 'Inventory Management', 'Customer Analytics']
    },
    {
      id: '6',
      company: {
        name: 'Molokai Agriculture Co-op',
        island: 'Molokai',
        industry: 'Agriculture',
        size: 'Small',
        annual_revenue: 3000000
      },
      score: 78,
      priority_level: 'Medium',
      status: 'active',
      last_contact: '2024-01-14',
      estimated_deal_value: 45000,
      recommended_services: ['Supply Chain Optimization', 'Market Analysis', 'Sustainability Consulting']
    },
    {
      id: '7',
      company: {
        name: 'Lanai Luxury Estates',
        island: 'Lanai',
        industry: 'Real Estate',
        size: 'Medium',
        annual_revenue: 20000000
      },
      score: 75,
      priority_level: 'Low',
      status: 'active',
      last_contact: '2024-01-09',
      estimated_deal_value: 85000,
      recommended_services: ['Marketing Strategy', 'Property Management Systems', 'Customer Experience']
    },
    {
      id: '8',
      company: {
        name: 'Waikiki Entertainment Group',
        island: 'Oahu',
        industry: 'Entertainment',
        size: 'Medium',
        annual_revenue: 12000000
      },
      score: 72,
      priority_level: 'Low',
      status: 'active',
      last_contact: '2024-01-11',
      estimated_deal_value: 65000,
      recommended_services: ['Event Management', 'Digital Marketing', 'Revenue Optimization']
    }
  ],
  total: 156,
  page: 1,
  per_page: 20
};