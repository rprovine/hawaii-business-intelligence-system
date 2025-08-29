import React from 'react';
import { useQuery } from 'react-query';
import { 
  TrendingUp, 
  Users, 
  DollarSign, 
  Target,
  MapPin,
  Briefcase,
  AlertCircle,
  ArrowRight
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { fetchDashboardData } from '../services/api';
import { formatCurrency } from '../utils/format';

const ISLAND_COLORS = {
  'Oahu': '#0ea5e9',
  'Maui': '#22c55e',
  'Big Island': '#f43f5e',
  'Kauai': '#facc15',
  'Molokai': '#a855f7',
  'Lanai': '#f97316'
};

const Dashboard: React.FC = () => {
  const { data, isLoading, error } = useQuery('dashboard', fetchDashboardData, {
    refetchInterval: 60000 // Refresh every minute
  });

  if (isLoading) return <div className="flex items-center justify-center h-64">Loading dashboard...</div>;
  // Don't show error since we have fallback data
  if (error) {
    console.error('Dashboard API error (using fallback data):', error);
  }

  const stats = [
    {
      name: 'Total Prospects',
      value: data?.total_prospects || 0,
      icon: Users,
      color: 'bg-ocean-100 text-ocean-600',
    },
    {
      name: 'High Priority',
      value: data?.high_priority_count || 0,
      icon: Target,
      color: 'bg-coral-100 text-coral-600',
    },
    {
      name: 'Pipeline Value',
      value: formatCurrency(data?.total_pipeline_value || 0),
      icon: DollarSign,
      color: 'bg-palm-100 text-palm-600',
    },
    {
      name: 'Avg Score',
      value: Math.round(data?.average_score || 0),
      icon: TrendingUp,
      color: 'bg-sand-100 text-sand-600',
    },
  ];

  const pieData = data?.by_island?.map((item: any) => ({
    name: item.island,
    value: item.prospect_count,
    color: ISLAND_COLORS[item.island as keyof typeof ISLAND_COLORS] || '#gray'
  })) || [];

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
        <p className="text-gray-600 mt-1">
          Real-time Hawaii business intelligence insights
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="mt-2 text-3xl font-bold text-gray-900">{stat.value}</p>
                </div>
                <div className={`p-3 rounded-lg ${stat.color}`}>
                  <Icon className="h-6 w-6" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Prospects by Island */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <MapPin className="h-5 w-5 mr-2 text-ocean-600" />
            Prospects by Island
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Prospects by Industry */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Briefcase className="h-5 w-5 mr-2 text-ocean-600" />
            Top Industries
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart 
              data={data?.by_industry?.slice(0, 5) || []}
              margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="industry" 
                angle={-45}
                textAnchor="end"
                height={100}
              />
              <YAxis />
              <Tooltip />
              <Bar dataKey="prospect_count" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent High Score Prospects */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <AlertCircle className="h-5 w-5 mr-2 text-coral-600" />
            Recent High-Score Prospects
          </h3>
        </div>
        <div className="divide-y divide-gray-200">
          {data?.recent_high_scores?.slice(0, 5).map((prospect: any) => (
            <div key={prospect.id} className="px-6 py-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center">
                    <h4 className="text-sm font-medium text-gray-900">
                      {prospect.company.name}
                    </h4>
                    <span className="ml-2 px-2 py-1 text-xs font-medium bg-coral-100 text-coral-800 rounded-full">
                      Score: {prospect.score}
                    </span>
                  </div>
                  <div className="mt-1 text-sm text-gray-500">
                    {prospect.company.island} • {prospect.company.industry}
                  </div>
                  <div className="mt-2 text-sm text-gray-600">
                    {prospect.recommended_services?.join(', ')}
                  </div>
                </div>
                <Link
                  to={`/prospects/${prospect.id}`}
                  className="flex items-center text-ocean-600 hover:text-ocean-700"
                >
                  View
                  <ArrowRight className="h-4 w-4 ml-1" />
                </Link>
              </div>
            </div>
          ))}
        </div>
        <div className="px-6 py-3 bg-gray-50 text-center">
          <Link
            to="/prospects"
            className="text-sm font-medium text-ocean-600 hover:text-ocean-700"
          >
            View all prospects →
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;