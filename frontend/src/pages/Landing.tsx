import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Brain, 
  Globe, 
  Search, 
  TrendingUp, 
  Target, 
  BarChart3,
  CheckCircle,
  ArrowRight,
  Sparkles,
  Database,
  Settings,
  Users,
  MapPin,
  Briefcase,
  Shield,
  Zap
} from 'lucide-react';

const Landing: React.FC = () => {
  const features = [
    {
      icon: Globe,
      title: "Multi-Source Data Collection",
      description: "Automatically scrape and gather data from Google Maps/Places, Yelp, LinkedIn, Pacific Business News, and custom websites you specify."
    },
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description: "Advanced AI algorithms analyze each prospect, generating scores, readiness assessments, and personalized recommendations."
    },
    {
      icon: Target,
      title: "Lead Scoring & Prioritization",
      description: "Automatically score and prioritize prospects based on technology readiness, company size, industry, and growth indicators."
    },
    {
      icon: Settings,
      title: "Customizable Parameters",
      description: "Tweak scoring criteria, industry focus, geographic regions, and company size thresholds to match your ideal customer profile."
    },
    {
      icon: BarChart3,
      title: "Competitive Intelligence",
      description: "Track competitors, market trends, and industry movements in real-time across the Hawaiian islands."
    },
    {
      icon: Zap,
      title: "Automated Workflows",
      description: "Set up automated data collection schedules, alert triggers, and AI analysis runs to keep your pipeline fresh."
    }
  ];

  const dataSources = [
    { name: "Google Business", icon: "🗺️", description: "Business profiles, reviews, locations" },
    { name: "Yelp", icon: "⭐", description: "Ratings, customer feedback, trends" },
    { name: "LinkedIn", icon: "💼", description: "Company data, decision makers, updates" },
    { name: "Pacific Business News", icon: "📰", description: "Local business news and developments" },
    { name: "Custom Websites", icon: "🌐", description: "Any website you want to monitor" },
    { name: "Public Records", icon: "📊", description: "Business registrations, permits, filings" }
  ];

  const benefits = [
    "Generate 10x more qualified leads with AI-powered prospect identification",
    "Save 20+ hours per week on manual research and data entry",
    "Increase conversion rates by 35% with better prospect intelligence",
    "Never miss a business opportunity in your target market",
    "Stay ahead of competitors with real-time market insights"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-ocean-50 to-white">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-ocean-600/10 to-transparent"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="p-3 bg-ocean-100 rounded-2xl">
                <Brain className="h-12 w-12 text-ocean-600" />
              </div>
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              Hawaii Business Intelligence System
            </h1>
            <p className="text-xl sm:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
              AI-powered lead generation and competitive intelligence for Hawaii businesses. 
              Automatically discover, analyze, and prioritize your next best customers.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/dashboard"
                className="px-8 py-4 bg-ocean-600 text-white rounded-lg hover:bg-ocean-700 font-semibold text-lg flex items-center justify-center gap-2"
              >
                View Dashboard
                <ArrowRight className="h-5 w-5" />
              </Link>
              <a
                href="#how-it-works"
                className="px-8 py-4 bg-white text-ocean-600 border-2 border-ocean-600 rounded-lg hover:bg-ocean-50 font-semibold text-lg"
              >
                Learn How It Works
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Bar */}
      <div className="bg-ocean-600 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-white">15,000+</div>
              <div className="text-ocean-100">Hawaii Businesses Tracked</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white">6</div>
              <div className="text-ocean-100">Islands Covered</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white">24/7</div>
              <div className="text-ocean-100">Automated Monitoring</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white">95%</div>
              <div className="text-ocean-100">AI Accuracy Rate</div>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div id="how-it-works" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600">
              Three simple steps to supercharge your business development
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-ocean-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Search className="h-10 w-10 text-ocean-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">1. Data Collection</h3>
              <p className="text-gray-600">
                Our system continuously scrapes multiple sources including Google Maps, Yelp, 
                LinkedIn, and custom websites to gather comprehensive business data across Hawaii.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-palm-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="h-10 w-10 text-palm-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">2. AI Analysis</h3>
              <p className="text-gray-600">
                Advanced AI analyzes each business for technology readiness, growth potential, 
                pain points, and generates personalized engagement recommendations.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-coral-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Target className="h-10 w-10 text-coral-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">3. Lead Prioritization</h3>
              <p className="text-gray-600">
                Prospects are automatically scored and prioritized based on your custom criteria, 
                delivering your hottest leads directly to your dashboard.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Data Sources */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Comprehensive Data Sources
            </h2>
            <p className="text-xl text-gray-600">
              We aggregate data from all the sources that matter
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {dataSources.map((source, index) => (
              <div key={index} className="bg-white rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
                <div className="text-3xl mb-3">{source.icon}</div>
                <h3 className="text-lg font-semibold mb-2">{source.name}</h3>
                <p className="text-gray-600 text-sm">{source.description}</p>
              </div>
            ))}
          </div>

          <div className="mt-8 text-center">
            <p className="text-gray-600 mb-4">
              Plus any custom website or data source you need monitored
            </p>
            <Link
              to="/workflows"
              className="inline-flex items-center text-ocean-600 hover:text-ocean-700 font-semibold"
            >
              Configure Data Sources
              <ArrowRight className="h-4 w-4 ml-1" />
            </Link>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Powerful Features
            </h2>
            <p className="text-xl text-gray-600">
              Everything you need to dominate your market
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="flex">
                  <div className="flex-shrink-0">
                    <div className="p-3 bg-ocean-100 rounded-lg">
                      <Icon className="h-6 w-6 text-ocean-600" />
                    </div>
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                    <p className="text-gray-600">{feature.description}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Customization Section */}
      <div className="py-16 bg-gradient-to-r from-ocean-500 to-ocean-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl sm:text-4xl font-bold mb-6">
                Fully Customizable to Your Business
              </h2>
              <p className="text-xl mb-8 text-ocean-100">
                Tailor every aspect of the system to match your ideal customer profile and business goals.
              </p>
              
              <div className="space-y-4">
                <div className="flex items-start">
                  <Settings className="h-6 w-6 mr-3 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-semibold mb-1">Custom Scoring Criteria</h3>
                    <p className="text-ocean-100">Define what makes a prospect valuable to your business</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <MapPin className="h-6 w-6 mr-3 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-semibold mb-1">Geographic Focus</h3>
                    <p className="text-ocean-100">Target specific islands, cities, or neighborhoods</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <Briefcase className="h-6 w-6 mr-3 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-semibold mb-1">Industry Filters</h3>
                    <p className="text-ocean-100">Focus on the industries where you excel</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <Users className="h-6 w-6 mr-3 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-semibold mb-1">Company Size Thresholds</h3>
                    <p className="text-ocean-100">Target businesses that match your service capacity</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur rounded-2xl p-8">
              <h3 className="text-2xl font-semibold mb-6">AI-Generated Intelligence</h3>
              <div className="space-y-6">
                <div>
                  <div className="flex justify-between mb-2">
                    <span>Technology Readiness Score</span>
                    <span className="font-bold">0-100</span>
                  </div>
                  <div className="w-full bg-white/20 rounded-full h-2">
                    <div className="bg-white h-2 rounded-full" style={{width: '85%'}}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span>Growth Potential</span>
                    <span className="font-bold">High/Medium/Low</span>
                  </div>
                  <div className="w-full bg-white/20 rounded-full h-2">
                    <div className="bg-white h-2 rounded-full" style={{width: '70%'}}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span>Engagement Priority</span>
                    <span className="font-bold">1-5 Stars</span>
                  </div>
                  <div className="w-full bg-white/20 rounded-full h-2">
                    <div className="bg-white h-2 rounded-full" style={{width: '90%'}}></div>
                  </div>
                </div>
              </div>
              <p className="text-sm mt-6 text-ocean-100">
                All scores and percentages are automatically calculated by our AI based on 
                dozens of data points and your custom parameters.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Benefits */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Transform Your Business Development
            </h2>
            <p className="text-xl text-gray-600">
              Join Hawaii's leading businesses using AI-powered intelligence
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {benefits.map((benefit, index) => (
              <div key={index} className="flex items-start">
                <CheckCircle className="h-6 w-6 text-green-500 mr-3 flex-shrink-0 mt-1" />
                <p className="text-lg text-gray-700">{benefit}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-16 bg-gradient-to-r from-ocean-600 to-ocean-700">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to 10x Your Lead Generation?
          </h2>
          <p className="text-xl text-ocean-100 mb-8">
            Start discovering your next best customers with AI-powered intelligence
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/dashboard"
              className="px-8 py-4 bg-white text-ocean-600 rounded-lg hover:bg-gray-100 font-semibold text-lg flex items-center justify-center gap-2"
            >
              <Sparkles className="h-5 w-5" />
              Start Free Trial
            </Link>
            <Link
              to="/prospects"
              className="px-8 py-4 bg-ocean-500 text-white rounded-lg hover:bg-ocean-400 font-semibold text-lg flex items-center justify-center gap-2"
            >
              View Sample Prospects
              <ArrowRight className="h-5 w-5" />
            </Link>
          </div>
          <p className="text-ocean-100 text-sm mt-6">
            No credit card required • 14-day free trial • Cancel anytime
          </p>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <Brain className="h-8 w-8 text-ocean-400 mr-2" />
                <span className="text-white font-semibold">Hawaii BI System</span>
              </div>
              <p className="text-sm">
                AI-powered business intelligence for Hawaii's growing businesses.
              </p>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-3">Product</h3>
              <ul className="space-y-2 text-sm">
                <li><Link to="/dashboard" className="hover:text-white">Dashboard</Link></li>
                <li><Link to="/prospects" className="hover:text-white">Prospects</Link></li>
                <li><Link to="/analytics" className="hover:text-white">Analytics</Link></li>
                <li><Link to="/workflows" className="hover:text-white">Workflows</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-3">Data Sources</h3>
              <ul className="space-y-2 text-sm">
                <li>Google Business</li>
                <li>Yelp</li>
                <li>LinkedIn</li>
                <li>Pacific Business News</li>
                <li>Custom Websites</li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-3">Company</h3>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white">About</a></li>
                <li><a href="#" className="hover:text-white">Contact</a></li>
                <li><a href="#" className="hover:text-white">Privacy</a></li>
                <li><a href="#" className="hover:text-white">Terms</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
            <p>© 2024 Hawaii Business Intelligence System. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;