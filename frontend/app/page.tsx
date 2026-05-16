"use client";
import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Activity, ShieldAlert, Layers, RefreshCw } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isAuthorized, setIsAuthorized] = useState(false);
  const router = useRouter();
 
  // Secure Token Retrieval Sequence
  useEffect(() => {
    const secureToken = localStorage.getItem("access_token");
    
    if (!secureToken) {
      router.replace("/login");
      return;
    }

    setIsAuthorized(true);
    fetchMetrics(secureToken);
  }, [router]);

  const fetchMetrics = async (authToken: string) => {
    setLoading(true); 
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || "https://analytics-backend-api.onrender.com";
    try {
      const res = await fetch(`${backendUrl}/api/dashboard/metrics/`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });

      if (res.status === 401) {
        // if token is invalid or expired, clear it and redirect to login
        localStorage.clear();
        router.replace("/login");
        return;
      }

      const result = await res.json();
      setData(result);
    } catch (err) {
      console.error("Failed fetching pipeline telemetry context layers:", err);
    } finally {
      setLoading(false);
    }
  };

  // Force Reload click handler with valid token pass
  const handleForceReload = () => {
    const secureToken = localStorage.getItem("access_token");
    if (secureToken) {
      fetchMetrics(secureToken);
    } else {
      router.replace("/login");
    }
  };
 
  // While token is being verified or data is loading, show the loader
  if (!isAuthorized || loading) return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
      <div className="text-center space-y-4">
        <RefreshCw className="animate-spin text-emerald-500 w-12 h-12 mx-auto" />
        <p className="text-sm text-slate-400">Syncing enterprise metrics layers...</p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8">
      {/* Header Banner */}
      <div className="flex justify-between items-center mb-8 border-b border-slate-800 pb-5">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-2">
            <Layers className="text-emerald-500" /> Enterprise Metrics Platform
          </h1>
          <p className="text-slate-400 text-sm mt-1">Real-time multi-tenant observability and data isolation logs.</p>
        </div>
        <button onClick={handleForceReload} className="bg-emerald-600 hover:bg-emerald-500 transition px-4 py-2 rounded-lg font-medium text-sm flex items-center gap-2">
          <RefreshCw size={16} /> Force Reload
        </button>
      </div>

      {/* KPI Cards Grid Layer */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-md">
          <div className="flex justify-between items-center text-slate-400 mb-2">
            <span className="text-sm font-semibold uppercase tracking-wider">Total Events Ingested</span>
            <Activity className="text-emerald-500" />
          </div>
          <h2 className="text-4xl font-extrabold text-white">{data?.total_events || 0}</h2>
        </div>
        
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-md">
          <div className="flex justify-between items-center text-slate-400 mb-2">
            <span className="text-sm font-semibold uppercase tracking-wider">Unique Active Actions</span>
            <Layers className="text-blue-500" />
          </div>
          <h2 className="text-4xl font-extrabold text-white">{data?.breakdown?.length || 0}</h2>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-md">
          <div className="flex justify-between items-center text-slate-400 mb-2">
            <span className="text-sm font-semibold uppercase tracking-wider">System Operational Guard</span>
            <ShieldAlert className="text-amber-500" />
          </div>
          <h2 className="text-xl font-bold text-emerald-400 mt-2">Active (Isolated)</h2>
        </div>
      </div>

      {/* Analytics Visualization Engine Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Time-Series Line Graph Node */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
          <h3 className="text-lg font-bold text-white mb-4">Ingestion Volume Over Intervals</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data?.time_series || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                <Line type="monotone" dataKey="count" stroke="#10b981" strokeWidth={3} dot={{ fill: '#10b981' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Aggregated Categorical Bar Chart Graph Node */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
          <h3 className="text-lg font-bold text-white mb-4">Event Types Allocation Breakdown</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data?.breakdown || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="event_name" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}