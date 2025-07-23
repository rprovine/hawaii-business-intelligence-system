import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import ReactMarkdown from 'react-markdown';
import { 
  ArrowLeft, 
  MapPin, 
  Briefcase, 
  Globe, 
  Phone, 
  TrendingUp,
  DollarSign,
  Calendar,
  AlertCircle,
  Target,
  Users,
  Building,
  CheckCircle,
  XCircle,
  Mail,
  Linkedin,
  User
} from 'lucide-react';
import { fetchProspectById } from '../services/api';
import { formatCurrency } from '../utils/format';
import { cn } from '../utils/cn';

const ProspectDetail: React.FC = () => {
  const { id } = useParams();
  
  const { data: prospect, isLoading, error } = useQuery(
    ['prospect', id],
    () => fetchProspectById(id!),
    { enabled: !!id }
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading prospect details...</div>
      </div>
    );
  }

  if (error || !prospect) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-500">Error loading prospect details</div>
      </div>
    );
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High': return 'bg-red-100 text-red-800 border-red-200';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'Low': return 'bg-gray-100 text-gray-800 border-gray-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="px-4 sm:px-0">
      <Link to="/prospects" className="flex items-center text-ocean-600 hover:text-ocean-700 mb-4 sm:mb-6">
        <ArrowLeft className="h-4 w-4 mr-1" />
        Back to Prospects
      </Link>

      {/* Company Header */}
      <div className="bg-white rounded-lg shadow mb-6">
        <div className="p-4 sm:p-6">
          <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
            <div className="flex-1">
              <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">{prospect.company.name}</h1>
              <div className="flex flex-wrap items-center gap-2 sm:gap-4 mt-3 text-sm sm:text-base text-gray-600">
                <div className="flex items-center">
                  <MapPin className="h-4 w-4 mr-1" />
                  {prospect.company.island}
                </div>
                <div className="flex items-center">
                  <Briefcase className="h-4 w-4 mr-1" />
                  {prospect.company.industry}
                </div>
                {prospect.company.website && !prospect.company.website.includes('.com') ? (
                  <div className="flex items-center text-gray-500">
                    <Globe className="h-4 w-4 mr-1" />
                    <span className="text-sm">No website</span>
                  </div>
                ) : prospect.company.website ? (
                  <a 
                    href={prospect.company.website} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center text-ocean-600 hover:text-ocean-700"
                  >
                    <Globe className="h-4 w-4 mr-1" />
                    <span className="hidden sm:inline">Website</span>
                    <span className="sm:hidden">Web</span>
                  </a>
                ) : null}
                {prospect.company.phone && (
                  <div className="flex items-center">
                    <Phone className="h-4 w-4 mr-1" />
                    <span className="hidden sm:inline">{prospect.company.phone}</span>
                    <span className="sm:hidden">Call</span>
                  </div>
                )}
              </div>
              {prospect.company.address && (
                <p className="text-sm sm:text-base text-gray-600 mt-2">{prospect.company.address}</p>
              )}
            </div>
            <div className="flex flex-row sm:flex-col items-center sm:items-end gap-4 sm:gap-2">
              <div className="flex items-center">
                <TrendingUp className="h-5 w-5 mr-2 text-ocean-600" />
                <span className={cn("text-2xl sm:text-3xl font-bold", getScoreColor(prospect.score))}>
                  {prospect.score}
                </span>
                <span className="text-gray-500 text-sm ml-1">/100</span>
              </div>
              <span className={cn(
                'px-3 py-1 inline-flex text-xs sm:text-sm font-semibold rounded-full border',
                getPriorityColor(prospect.priority_level)
              )}>
                {prospect.priority_level} Priority
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-4 sm:space-y-6 order-2 lg:order-1">
          {/* AI Analysis */}
          <div className="bg-white rounded-lg shadow p-4 sm:p-6">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4 flex items-center">
              <Target className="h-5 w-5 mr-2 text-ocean-600" />
              AI Analysis
            </h2>
            <div className="prose prose-sm sm:prose max-w-none">
              <ReactMarkdown
                components={{
                  h2: ({ children }) => <h2 className="text-lg font-semibold text-gray-900 mt-4 mb-2">{children}</h2>,
                  h3: ({ children }) => <h3 className="text-base font-semibold text-gray-800 mt-3 mb-2">{children}</h3>,
                  p: ({ children }) => <p className="text-sm sm:text-base text-gray-700 mb-3">{children}</p>,
                  ul: ({ children }) => <ul className="list-disc list-inside space-y-1 mb-3">{children}</ul>,
                  li: ({ children }) => <li className="text-sm sm:text-base text-gray-700">{children}</li>,
                  strong: ({ children }) => <strong className="font-semibold text-gray-900">{children}</strong>,
                }}
              >
                {prospect.ai_analysis}
              </ReactMarkdown>
            </div>
          </div>

          {/* Pain Points */}
          <div className="bg-white rounded-lg shadow p-4 sm:p-6">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4 flex items-center">
              <AlertCircle className="h-5 w-5 mr-2 text-coral-600" />
              Identified Pain Points
            </h2>
            <ul className="space-y-2 sm:space-y-3">
              {prospect.pain_points?.map((pain: string, index: number) => (
                <li key={index} className="flex items-start">
                  <XCircle className="h-4 sm:h-5 w-4 sm:w-5 text-coral-500 mr-2 flex-shrink-0 mt-0.5" />
                  <span className="text-sm sm:text-base text-gray-700">{pain}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Growth Signals */}
          {prospect.growth_signals && prospect.growth_signals.length > 0 && (
            <div className="bg-white rounded-lg shadow p-4 sm:p-6">
              <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4 flex items-center">
                <TrendingUp className="h-5 w-5 mr-2 text-green-600" />
                Growth Signals
              </h2>
              <ul className="space-y-2 sm:space-y-3">
                {prospect.growth_signals.map((signal: string, index: number) => (
                  <li key={index} className="flex items-start">
                    <CheckCircle className="h-4 sm:h-5 w-4 sm:w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                    <span className="text-sm sm:text-base text-gray-700">{signal}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Company Details */}
          <div className="bg-white rounded-lg shadow p-4 sm:p-6">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4 flex items-center">
              <Building className="h-5 w-5 mr-2 text-ocean-600" />
              Company Information
            </h2>
            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 text-sm sm:text-base">
              {prospect.company.employee_count_estimate && (
                <>
                  <dt className="text-sm font-medium text-gray-500">Estimated Employees</dt>
                  <dd className="text-sm text-gray-900">{prospect.company.employee_count_estimate}</dd>
                </>
              )}
              {prospect.company.annual_revenue_estimate && (
                <>
                  <dt className="text-sm font-medium text-gray-500">Estimated Annual Revenue</dt>
                  <dd className="text-sm text-gray-900">
                    {formatCurrency(prospect.company.annual_revenue_estimate)}
                  </dd>
                </>
              )}
              <dt className="text-sm font-medium text-gray-500">Technology Readiness</dt>
              <dd className="text-sm text-gray-900">{prospect.technology_readiness}</dd>
              
              <dt className="text-sm font-medium text-gray-500">Data Source</dt>
              <dd className="text-sm text-gray-900">{prospect.company.source}</dd>
              
              {prospect.company.founded_date && (
                <>
                  <dt className="text-sm font-medium text-gray-500">Founded</dt>
                  <dd className="text-sm text-gray-900">{prospect.company.founded_date}</dd>
                </>
              )}
              
              <dt className="text-sm font-medium text-gray-500">Last Analyzed</dt>
              <dd className="text-sm text-gray-900">
                {new Date(prospect.last_analyzed).toLocaleDateString()}
              </dd>
            </dl>
            
            {prospect.company.description && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <dt className="text-sm font-medium text-gray-500 mb-2">Description</dt>
                <dd className="text-sm text-gray-700 whitespace-pre-line">{prospect.company.description}</dd>
              </div>
            )}
          </div>

          {/* Decision Makers */}
          {prospect.decision_makers && prospect.decision_makers.length > 0 && (
            <div className="bg-white rounded-lg shadow p-4 sm:p-6">
              <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4 flex items-center">
                <Users className="h-5 w-5 mr-2 text-ocean-600" />
                Key Decision Makers
              </h2>
              <div className="space-y-4">
                {prospect.decision_makers.map((dm: any, index: number) => (
                  <div key={index} className="border-l-4 border-ocean-400 pl-4 py-2">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">{dm.name}</h3>
                        <p className="text-sm text-gray-600">{dm.title}</p>
                        <div className="mt-2 space-y-1">
                          {dm.email && (
                            <a 
                              href={`mailto:${dm.email}`}
                              className="flex items-center text-sm text-ocean-600 hover:text-ocean-700"
                            >
                              <Mail className="h-4 w-4 mr-1" />
                              {dm.email}
                            </a>
                          )}
                          {dm.phone && (
                            <a 
                              href={`tel:${dm.phone}`}
                              className="flex items-center text-sm text-ocean-600 hover:text-ocean-700"
                            >
                              <Phone className="h-4 w-4 mr-1" />
                              {dm.phone}
                            </a>
                          )}
                          {dm.linkedin_url && (
                            <a 
                              href={dm.linkedin_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex items-center text-sm text-ocean-600 hover:text-ocean-700"
                            >
                              <Linkedin className="h-4 w-4 mr-1" />
                              LinkedIn Profile
                            </a>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-4 sm:space-y-6 order-1 lg:order-2">
          {/* Deal Information */}
          <div className="bg-white rounded-lg shadow p-4 sm:p-6">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4 flex items-center">
              <DollarSign className="h-5 w-5 mr-2 text-green-600" />
              Deal Information
            </h2>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-500">Estimated Deal Value</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(prospect.estimated_deal_value)}
                </p>
              </div>
              
              <div>
                <p className="text-sm text-gray-500 mb-2">Recommended Services</p>
                <div className="flex flex-wrap gap-2">
                  {prospect.recommended_services?.map((service: string, index: number) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-ocean-100 text-ocean-800 text-sm font-medium rounded-full"
                    >
                      {service}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="bg-white rounded-lg shadow p-4 sm:p-6">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4">Actions</h2>
            <div className="space-y-3">
              <button className="w-full px-3 sm:px-4 py-2 bg-ocean-600 text-white text-sm sm:text-base rounded-lg hover:bg-ocean-700 transition-colors">
                Create Proposal
              </button>
              <button className="w-full px-3 sm:px-4 py-2 bg-white text-ocean-600 border border-ocean-600 text-sm sm:text-base rounded-lg hover:bg-ocean-50 transition-colors">
                Schedule Meeting
              </button>
              <button className="w-full px-3 sm:px-4 py-2 bg-white text-gray-600 border border-gray-300 text-sm sm:text-base rounded-lg hover:bg-gray-50 transition-colors">
                Add to CRM
              </button>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="bg-gray-50 rounded-lg p-4 sm:p-6">
            <h3 className="text-sm font-semibold text-gray-900 mb-3">Quick Stats</h3>
            <dl className="space-y-2">
              <div className="flex justify-between">
                <dt className="text-sm text-gray-500">Score</dt>
                <dd className="text-sm font-medium text-gray-900">{prospect.score}/100</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-sm text-gray-500">Priority</dt>
                <dd className="text-sm font-medium text-gray-900">{prospect.priority_level}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-sm text-gray-500">Services</dt>
                <dd className="text-sm font-medium text-gray-900">
                  {prospect.recommended_services?.length || 0}
                </dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-sm text-gray-500">Pain Points</dt>
                <dd className="text-sm font-medium text-gray-900">
                  {prospect.pain_points?.length || 0}
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProspectDetail;