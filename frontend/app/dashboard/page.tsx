'use client';

import { useEffect, useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import Link from 'next/link';
import { srsAPI, challengesAPI, analyticsAPI } from '@/lib/api';

export default function DashboardPage() {
  const [stats, setStats] = useState({
    dueCards: 0,
    dailyChallenges: 0,
    currentStreak: 0,
    wordsLearned: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [srsData, challengeData, streakData] = await Promise.all([
        srsAPI.getDueCards(),
        challengesAPI.getProgress(),
        challengesAPI.getStreak(),
      ]);

      setStats({
        dueCards: srsData.data.due_now || 0,
        dailyChallenges: challengeData.data.filter((c: any) => !c.completed).length,
        currentStreak: streakData.data.current_streak || 0,
        wordsLearned: srsData.data.total_cards || 0,
      });
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome back!</h1>
          <p className="text-gray-600">Continue your Korean learning journey</p>
        </div>

        {/* Quick Stats */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-md card-hover">
            <div className="flex items-center justify-between mb-3">
              <div className="text-3xl">🎴</div>
              <div className="text-2xl font-bold text-primary">{stats.dueCards}</div>
            </div>
            <p className="text-gray-600 font-medium">Cards Due</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md card-hover">
            <div className="flex items-center justify-between mb-3">
              <div className="text-3xl">🔥</div>
              <div className="text-2xl font-bold text-coral">{stats.currentStreak}</div>
            </div>
            <p className="text-gray-600 font-medium">Day Streak</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md card-hover">
            <div className="flex items-center justify-between mb-3">
              <div className="text-3xl">📚</div>
              <div className="text-2xl font-bold text-success">{stats.wordsLearned}</div>
            </div>
            <p className="text-gray-600 font-medium">Words Learned</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md card-hover">
            <div className="flex items-center justify-between mb-3">
              <div className="text-3xl">🎯</div>
              <div className="text-2xl font-bold text-primary">{stats.dailyChallenges}</div>
            </div>
            <p className="text-gray-600 font-medium">Challenges Left</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <Link href="/dashboard/flashcards">
            <div className="bg-gradient-to-br from-blue-500 to-blue-700 p-8 rounded-xl shadow-lg card-hover cursor-pointer text-white">
              <div className="text-4xl mb-4">🎴</div>
              <h3 className="text-2xl font-bold mb-2">Study Flashcards</h3>
              <p className="text-blue-100">Review your due flashcards with spaced repetition</p>
              <div className="mt-4 inline-flex items-center gap-2 text-white font-semibold">
                Start Studying →
              </div>
            </div>
          </Link>

          <Link href="/dashboard/quiz">
            <div className="bg-gradient-to-br from-purple-500 to-purple-700 p-8 rounded-xl shadow-lg card-hover cursor-pointer text-white">
              <div className="text-4xl mb-4">📝</div>
              <h3 className="text-2xl font-bold mb-2">Take a Quiz</h3>
              <p className="text-purple-100">Test your knowledge with interactive quizzes</p>
              <div className="mt-4 inline-flex items-center gap-2 text-white font-semibold">
                Start Quiz →
              </div>
            </div>
          </Link>
        </div>

        {/* Today's Progress */}
        <div className="bg-white p-6 rounded-xl shadow-md mb-8">
          <h2 className="text-xl font-bold mb-4">Today's Progress</h2>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-gray-600">Daily Goal</span>
                <span className="font-semibold">60%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="bg-primary h-3 rounded-full" style={{ width: '60%' }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span className="text-gray-600">Study Time</span>
                <span className="font-semibold">25 minutes</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="bg-success h-3 rounded-full" style={{ width: '50%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
              <div className="text-2xl">✅</div>
              <div>
                <p className="font-medium">Completed Quiz</p>
                <p className="text-sm text-gray-600">Score: 85% - 2 hours ago</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
              <div className="text-2xl">🎯</div>
              <div>
                <p className="font-medium">Daily Challenge Completed</p>
                <p className="text-sm text-gray-600">Learned 10 new words - 5 hours ago</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-purple-50 rounded-lg">
              <div className="text-2xl">⭐</div>
              <div>
                <p className="font-medium">Achievement Unlocked</p>
                <p className="text-sm text-gray-600">Vocabulary Builder - Yesterday</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
