import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { Link } from 'react-router-dom';
import { 
  Search, 
  Filter, 
  MapPin, 
  Briefcase, 
  TrendingUp,
  ArrowRight,
  RefreshCw
} from 'lucide-react';
import { fetchProspects } from '../services/api';
import { cn } from '../utils/cn';

const ISLANDS = ['All', 'Oahu', 'Maui', 'Big Island', 'Kauai', 'Molokai', 'Lanai'];
const PRIORITIES = ['All', 'High', 'Medium', 'Low'];

const Prospects: React.FC = () => {
  const [filters, setFilters] = useState({
    island: 'All',
    priority: 'All',
    minScore: 0
  });

  const { data: prospects, isLoading, refetch } = useQuery(
    ['prospects', filters],
    () => fetchProspects({
      island: filters.island !== 'All' ? filters.island : undefined,
      priority: filters.priority !== 'All' ? filters.priority : undefined,
      min_score: filters.minScore > 0 ? filters.minScore : undefined
    }),
    { refetchInterval: 30000 }
  );

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High': return 'bg-red-100 text-red-800';
      case 'Medium': return 'bg-yellow-100 text-yellow-800';
      case 'Low': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Prospects</h2>
            <p className="text-gray-600 mt-1">
              Manage and track potential clients across Hawaii
            </p>
          </div>
          <button
            onClick={() => refetch()}
            className="flex items-center px-4 py-2 bg-ocean-600 text-white rounded-lg hover:bg-ocean-700"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Island Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Island
            </label>
            <select
              value={filters.island}
              onChange={(e) => setFilters({ ...filters, island: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-ocean-500 focus:border-ocean-500"
            >
              {ISLANDS.map(island => (
                <option key={island} value={island}>{island}</option>
              ))}
            </select>
          </div>

          {/* Priority Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              value={filters.priority}
              onChange={(e) => setFilters({ ...filters, priority: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-ocean-500 focus:border-ocean-500"
            >
              {PRIORITIES.map(priority => (
                <option key={priority} value={priority}>{priority}</option>
              ))}
            </select>
          </div>

          {/* Min Score Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Minimum Score
            </label>
            <input
              type="number"
              min="0"
              max="100"
              value={filters.minScore}
              onChange={(e) => setFilters({ ...filters, minScore: parseInt(e.target.value) || 0 })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-ocean-500 focus:border-ocean-500"
            />
          </div>

          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <div className="relative">
              <input
                type="text"
                placeholder="Search prospects..."
                className="w-full px-3 py-2 pl-10 border border-gray-300 rounded-md focus:ring-ocean-500 focus:border-ocean-500"
              />
              <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
            </div>
          </div>
        </div>
      </div>

      {/* Prospects List */}
      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">Loading prospects...</div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Company
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Priority
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Services
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Deal Value
                </th>
                <th className="relative px-6 py-3">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {prospects?.map((prospect: any) => (
                <tr key={prospect.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        {prospect.company.name}
                      </div>
                      <div className="text-sm text-gray-500 flex items-center">
                        <MapPin className="h-3 w-3 mr-1" />
                        {prospect.company.island}
                        <span className="mx-2">•</span>
                        <Briefcase className="h-3 w-3 mr-1" />
                        {prospect.company.industry}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <TrendingUp className="h-4 w-4 mr-1 text-ocean-600" />
                      <span className="text-sm font-medium text-gray-900">
                        {prospect.score}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={cn(
                      'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
                      getPriorityColor(prospect.priority_level)
                    )}>
                      {prospect.priority_level}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {prospect.recommended_services?.slice(0, 2).join(', ')}
                    {prospect.recommended_services?.length > 2 && '...'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    ${(prospect.estimated_deal_value || 0).toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <Link
                      to={`/prospects/${prospect.id}`}
                      className="text-ocean-600 hover:text-ocean-900 flex items-center justify-end"
                    >
                      View
                      <ArrowRight className="h-4 w-4 ml-1" />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Prospects;