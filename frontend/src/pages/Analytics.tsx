import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { 
  BarChart3, 
  TrendingUp, 
  DollarSign, 
  MapPin,
  Calendar,
  Download,
  Filter,
  PieChart,
  Activity
} from 'lucide-react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  AreaChart,
  Area
} from 'recharts';
import { fetchAnalyticsByIsland, fetchAnalyticsByIndustry, fetchAnalyticsTimeline, fetchDashboardData } from '../services/api';
import { formatCurrency } from '../utils/format';

const COLORS = {
  islands: {
    'Oahu': '#0ea5e9',
    'Maui': '#22c55e',
    'Big Island': '#f43f5e',
    'Kauai': '#facc15',
    'Molokai': '#a855f7',
    'Lanai': '#f97316'
  },
  industries: [
    '#0ea5e9', '#22c55e', '#f43f5e', '#facc15', 
    '#a855f7', '#f97316', '#06b6d4', '#84cc16'
  ]
};

const Analytics: React.FC = () => {
  const [dateRange, setDateRange] = useState('30');
  const [selectedIsland, setSelectedIsland] = useState('all');

  // Fetch all analytics data
  const { data: dashboardData } = useQuery('analytics-dashboard', fetchDashboardData);
  const { data: islandData } = useQuery('analytics-by-island', fetchAnalyticsByIsland);
  const { data: industryData } = useQuery('analytics-by-industry', fetchAnalyticsByIndustry);
  const { data: timelineData } = useQuery(
    ['analytics-timeline', dateRange],
    () => fetchAnalyticsTimeline(parseInt(dateRange))
  );

  // Calculate key metrics
  const totalPipelineValue = dashboardData?.total_pipeline_value || 0;
  const avgDealSize = dashboardData?.total_prospects > 0 
    ? totalPipelineValue / dashboardData.total_prospects 
    : 0;
  const conversionRate = dashboardData?.conversion_rate || 0;

  // Prepare timeline data for charts
  const timelineChartData = timelineData?.map((item: any) => ({
    date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    prospects: item.new_prospects,
    value: item.pipeline_value
  })) || [];

  // Industry distribution pie chart data
  const industryPieData = industryData?.slice(0, 6).map((item: any, index: number) => ({
    name: item.industry,
    value: item.prospect_count,
    percentage: ((item.prospect_count / dashboardData?.total_prospects) * 100).toFixed(1)
  })) || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 flex items-center">
              <BarChart3 className="h-6 w-6 mr-2 text-ocean-600" />
              Analytics
            </h2>
            <p className="text-gray-600 mt-1">
              Deep insights into your Hawaii business pipeline
            </p>
          </div>
          <div className="mt-4 sm:mt-0 flex items-center gap-3">
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-ocean-500 focus:border-ocean-500"
            >
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 90 days</option>
            </select>
            <button className="px-4 py-2 bg-ocean-600 text-white rounded-lg hover:bg-ocean-700 flex items-center gap-2">
              <Download className="h-4 w-4" />
              Export
            </button>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total Pipeline</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {formatCurrency(totalPipelineValue)}
              </p>
              <p className="text-sm text-green-600 mt-2">
                <TrendingUp className="h-4 w-4 inline mr-1" />
                +12% from last period
              </p>
            </div>
            <div className="p-3 bg-ocean-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-ocean-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Avg Deal Size</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {formatCurrency(avgDealSize)}
              </p>
              <p className="text-sm text-gray-600 mt-2">
                Per prospect
              </p>
            </div>
            <div className="p-3 bg-palm-100 rounded-lg">
              <Activity className="h-6 w-6 text-palm-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Conversion Rate</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {conversionRate.toFixed(1)}%
              </p>
              <p className="text-sm text-gray-600 mt-2">
                Lead to client
              </p>
            </div>
            <div className="p-3 bg-coral-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-coral-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Active Prospects</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {dashboardData?.total_prospects || 0}
              </p>
              <p className="text-sm text-ocean-600 mt-2">
                {dashboardData?.high_priority_count || 0} high priority
              </p>
            </div>
            <div className="p-3 bg-sand-100 rounded-lg">
              <PieChart className="h-6 w-6 text-sand-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pipeline Growth Over Time */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Pipeline Growth</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={timelineChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip formatter={(value: any) => formatCurrency(value)} />
              <Area 
                type="monotone" 
                dataKey="value" 
                stroke="#0ea5e9" 
                fill="#0ea5e9" 
                fillOpacity={0.1}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Prospects by Island */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Prospects by Island</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={islandData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="island" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="prospect_count" fill="#0ea5e9">
                {islandData?.map((entry: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={COLORS.islands[entry.island as keyof typeof COLORS.islands] || '#gray'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Industry Distribution */}
        <div className="bg-white rounded-lg shadow p-6 lg:col-span-2">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Industry Distribution</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <ResponsiveContainer width="100%" height={250}>
              <RechartsPieChart>
                <Pie
                  data={industryPieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ percentage }) => `${percentage}%`}
                >
                  {industryPieData.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={COLORS.industries[index % COLORS.industries.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </RechartsPieChart>
            </ResponsiveContainer>
            <div className="space-y-2">
              {industryPieData.map((item: any, index: number) => (
                <div key={item.name} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div 
                      className="w-3 h-3 rounded-full mr-2" 
                      style={{ backgroundColor: COLORS.industries[index % COLORS.industries.length] }}
                    />
                    <span className="text-sm text-gray-700">{item.name}</span>
                  </div>
                  <span className="text-sm font-medium text-gray-900">{item.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Score Distribution */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Score Distribution</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">High (80-100)</span>
                <span className="font-medium">{dashboardData?.high_priority_count || 0}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-green-600 h-2 rounded-full" 
                  style={{ width: `${(dashboardData?.high_priority_count || 0) / (dashboardData?.total_prospects || 1) * 100}%` }}
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">Medium (60-79)</span>
                <span className="font-medium">
                  {(dashboardData?.total_prospects || 0) - (dashboardData?.high_priority_count || 0)}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-yellow-600 h-2 rounded-full" 
                  style={{ width: '40%' }}
                />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">Low (0-59)</span>
                <span className="font-medium">0</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-red-600 h-2 rounded-full" style={{ width: '0%' }} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Island Performance Table */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Island Performance</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Island
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Prospects
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Avg Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Pipeline Value
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Top Industry
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {islandData?.map((island: any) => (
                <tr key={island.island} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <MapPin className="h-4 w-4 mr-2 text-gray-400" />
                      <span className="text-sm font-medium text-gray-900">{island.island}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {island.prospect_count}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm text-gray-900">{island.average_score.toFixed(1)}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatCurrency(island.total_pipeline_value)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {island.top_industry || 'Various'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Analytics;