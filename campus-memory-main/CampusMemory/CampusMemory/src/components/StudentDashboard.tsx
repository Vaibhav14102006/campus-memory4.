/**
 * Student Dashboard Component
 * For students to view their attendance history and OD status
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Award, Calendar, TrendingUp, CheckCircle } from 'lucide-react';

interface AttendedEvent {
  eventId: string;
  title: string;
  date: string;
  category: string;
  odGranted: boolean;
}

interface DashboardData {
  studentId: string;
  totalEventsAttended: number;
  presentCount: number;
  odGrantedCount: number;
  attendedEvents: AttendedEvent[];
}

const API_BASE_URL = 'http://localhost:8001';

export default function StudentDashboard({ studentId = 'STU001' }: { studentId?: string }) {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, [studentId]);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/dashboard/student/${studentId}`);
      const data = await response.json();
      setDashboardData(data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 flex items-center justify-center">
        <div className="text-xl text-gray-600">No data available</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h1 className="text-3xl font-bold text-gray-800">My Attendance</h1>
          <p className="text-gray-600 mt-2">Student ID: {studentId}</p>

          {/* Statistics Cards */}
          <div className="grid grid-cols-4 gap-4 mt-6">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="flex items-center gap-3">
                <Calendar className="text-blue-600" size={24} />
                <div>
                  <div className="text-2xl font-bold text-blue-600">
                    {dashboardData.totalEventsAttended}
                  </div>
                  <div className="text-sm text-gray-600">Events Attended</div>
                </div>
              </div>
            </div>

            <div className="bg-green-50 p-4 rounded-lg">
              <div className="flex items-center gap-3">
                <CheckCircle className="text-green-600" size={24} />
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {dashboardData.presentCount}
                  </div>
                  <div className="text-sm text-gray-600">Present</div>
                </div>
              </div>
            </div>

            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="flex items-center gap-3">
                <Award className="text-purple-600" size={24} />
                <div>
                  <div className="text-2xl font-bold text-purple-600">
                    {dashboardData.odGrantedCount}
                  </div>
                  <div className="text-sm text-gray-600">OD Granted</div>
                </div>
              </div>
            </div>

            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="flex items-center gap-3">
                <TrendingUp className="text-orange-600" size={24} />
                <div>
                  <div className="text-2xl font-bold text-orange-600">
                    {dashboardData.totalEventsAttended > 0
                      ? ((dashboardData.presentCount / dashboardData.totalEventsAttended) * 100).toFixed(0)
                      : 0}%
                  </div>
                  <div className="text-sm text-gray-600">Attendance Rate</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Attendance History */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Attendance History</h2>

          <div className="space-y-3">
            {dashboardData.attendedEvents.map((event) => (
              <div
                key={event.eventId}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h3 className="font-semibold text-gray-800 text-lg">{event.title}</h3>
                      {event.odGranted && (
                        <span className="flex items-center gap-1 text-xs font-semibold text-green-600 bg-green-50 px-2 py-1 rounded">
                          <Award size={14} />
                          OD Granted
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-600">
                      <span className="flex items-center gap-1">
                        <Calendar size={14} />
                        {event.date}
                      </span>
                      <span className="text-xs font-semibold text-indigo-600 bg-indigo-50 px-2 py-1 rounded">
                        {event.category}
                      </span>
                    </div>
                  </div>

                  <div className="text-green-600">
                    <CheckCircle size={24} />
                  </div>
                </div>
              </div>
            ))}

            {dashboardData.attendedEvents.length === 0 && (
              <div className="text-center py-12 text-gray-500">
                <Calendar className="mx-auto mb-4" size={48} />
                <p>No attendance records yet</p>
                <p className="text-sm mt-2">Start attending events to build your record!</p>
              </div>
            )}
          </div>
        </div>

        {/* Tips Section */}
        <div className="mt-8 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
          <h3 className="text-xl font-bold mb-2">💡 Pro Tips</h3>
          <ul className="space-y-2 text-sm">
            <li>✓ Attend events to earn OD (Official Duty) credits</li>
            <li>✓ OD can help with attendance requirements</li>
            <li>✓ Teachers can grant OD for event participation</li>
            <li>✓ Keep track of your attendance rate</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
