'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

export default function Home() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-6xl font-bold text-gray-900 mb-6 slide-up">
            VocabKo
            <span className="block text-primary mt-2">한국어 학습</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 slide-up">
            Master Korean vocabulary with spaced repetition, interactive quizzes, and gamification
          </p>

          <div className="flex gap-4 justify-center mb-12 slide-up">
            <Link
              href="/login"
              className="px-8 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-blue-700 transition"
            >
              Get Started
            </Link>
            <Link
              href="/dashboard"
              className="px-8 py-3 bg-white text-primary border-2 border-primary rounded-lg font-semibold hover:bg-blue-50 transition"
            >
              View Demo
            </Link>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-6 mt-16">
            <div className="bg-white p-6 rounded-xl shadow-md card-hover">
              <div className="text-4xl mb-4">🧠</div>
              <h3 className="text-xl font-semibold mb-2">Spaced Repetition</h3>
              <p className="text-gray-600">
                Learn efficiently with SM-2 algorithm that optimizes review intervals
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md card-hover">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold mb-2">Interactive Quizzes</h3>
              <p className="text-gray-600">
                Test your knowledge with engaging quizzes and track your progress
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md card-hover">
              <div className="text-4xl mb-4">🏆</div>
              <h3 className="text-xl font-semibold mb-2">Gamification</h3>
              <p className="text-gray-600">
                Earn achievements, compete on leaderboards, and stay motivated
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md card-hover">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-semibold mb-2">Advanced Analytics</h3>
              <p className="text-gray-600">
                Visualize your learning journey with detailed statistics and insights
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md card-hover">
              <div className="text-4xl mb-4">🔥</div>
              <h3 className="text-xl font-semibold mb-2">Daily Challenges</h3>
              <p className="text-gray-600">
                Build consistency with daily goals and maintain your study streak
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md card-hover">
              <div className="text-4xl mb-4">👥</div>
              <h3 className="text-xl font-semibold mb-2">Social Learning</h3>
              <p className="text-gray-600">
                Connect with friends, join study groups, and learn together
              </p>
            </div>
          </div>

          {/* Stats Section */}
          <div className="mt-16 grid md:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="text-3xl font-bold text-primary">500+</div>
              <div className="text-gray-600 mt-2">Korean Words</div>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="text-3xl font-bold text-success">SM-2</div>
              <div className="text-gray-600 mt-2">Algorithm</div>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="text-3xl font-bold text-coral">100+</div>
              <div className="text-gray-600 mt-2">Achievements</div>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="text-3xl font-bold text-primary">24/7</div>
              <div className="text-gray-600 mt-2">Learning</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
