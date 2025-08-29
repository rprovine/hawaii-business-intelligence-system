// Vercel serverless function for companies data
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const companiesData = [
    {
      id: 1,
      name: "Aloha Medical Center",
      website: "https://alohamedical.com",
      island: "Oahu",
      industry: "Healthcare",
      employee_count_estimate: 450,
      annual_revenue: "$125M",
      founded_year: 1998
    },
    {
      id: 2,
      name: "Pacific Paradise Resort",
      website: "https://pacificparadise.com",
      island: "Maui",
      industry: "Tourism",
      employee_count_estimate: 320,
      annual_revenue: "$85M",
      founded_year: 2005
    },
    {
      id: 3,
      name: "Kona Coffee Collective",
      website: "https://konacoffee.com",
      island: "Big Island",
      industry: "Food Service",
      employee_count_estimate: 85,
      annual_revenue: "$12M",
      founded_year: 2010
    },
    {
      id: 4,
      name: "Island Tech Solutions",
      website: "https://islandtech.com",
      island: "Oahu",
      industry: "Technology",
      employee_count_estimate: 150,
      annual_revenue: "$45M",
      founded_year: 2015
    },
    {
      id: 5,
      name: "Kauai Adventure Tours",
      website: "https://kauaiadventure.com",
      island: "Kauai",
      industry: "Tourism",
      employee_count_estimate: 65,
      annual_revenue: "$8M",
      founded_year: 2008
    },
    {
      id: 6,
      name: "Honolulu Construction Group",
      website: "https://hnlconstruction.com",
      island: "Oahu",
      industry: "Real Estate",
      employee_count_estimate: 280,
      annual_revenue: "$95M",
      founded_year: 1995
    },
    {
      id: 7,
      name: "Ohana Dental Care",
      website: "https://ohanadental.com",
      island: "Oahu",
      industry: "Healthcare",
      employee_count_estimate: 45,
      annual_revenue: "$6M",
      founded_year: 2012
    },
    {
      id: 8,
      name: "Big Island Solar",
      website: "https://bigislandsolar.com",
      island: "Big Island",
      industry: "Technology",
      employee_count_estimate: 75,
      annual_revenue: "$18M",
      founded_year: 2018
    },
    {
      id: 9,
      name: "Maui Ocean Center",
      website: "https://mauioceancenter.com",
      island: "Maui",
      industry: "Tourism",
      employee_count_estimate: 120,
      annual_revenue: "$22M",
      founded_year: 1998
    },
    {
      id: 10,
      name: "Lanai Luxury Properties",
      website: "https://lanailuxury.com",
      island: "Lanai",
      industry: "Real Estate",
      employee_count_estimate: 35,
      annual_revenue: "$28M",
      founded_year: 2007
    },
    {
      id: 11,
      name: "Molokai Fish & Dive",
      website: "https://molokaifish.com",
      island: "Molokai",
      industry: "Tourism",
      employee_count_estimate: 25,
      annual_revenue: "$3M",
      founded_year: 2003
    },
    {
      id: 12,
      name: "Waikiki Beach Hotel",
      website: "https://waikikibeach.com",
      island: "Oahu",
      industry: "Tourism",
      employee_count_estimate: 380,
      annual_revenue: "$110M",
      founded_year: 1985
    },
    {
      id: 13,
      name: "Kauai Medical Clinic",
      website: "https://kauaimedical.com",
      island: "Kauai",
      industry: "Healthcare",
      employee_count_estimate: 95,
      annual_revenue: "$15M",
      founded_year: 2006
    },
    {
      id: 14,
      name: "Maui Fresh Produce",
      website: "https://mauifresh.com",
      island: "Maui",
      industry: "Food Service",
      employee_count_estimate: 60,
      annual_revenue: "$9M",
      founded_year: 2014
    },
    {
      id: 15,
      name: "Hawaii Digital Marketing",
      website: "https://hawaiidigital.com",
      island: "Oahu",
      industry: "Technology",
      employee_count_estimate: 40,
      annual_revenue: "$7M",
      founded_year: 2019
    }
  ];

  res.status(200).json(companiesData);
}