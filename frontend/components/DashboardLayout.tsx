'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Mock user data (in real app, fetch from API)
    setUser({
      username: 'User',
      level: 'Intermediate',
      points: 1250,
    });
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    router.push('/');
  };

  const navItems = [
    { href: '/dashboard', label: 'Dashboard', icon: '📊' },
    { href: '/dashboard/flashcards', label: 'Flashcards', icon: '🎴' },
    { href: '/dashboard/quiz', label: 'Quiz', icon: '📝' },
    { href: '/dashboard/progress', label: 'Progress', icon: '📈' },
    { href: '/dashboard/leaderboard', label: 'Leaderboard', icon: '🏆' },
    { href: '/dashboard/challenges', label: 'Challenges', icon: '🎯' },
    { href: '/dashboard/achievements', label: 'Achievements', icon: '⭐' },
    { href: '/dashboard/social', label: 'Social', icon: '👥' },
    { href: '/dashboard/profile', label: 'Profile', icon: '👤' },
  ];

  if (!user) return null;

  return (
    <div className="min-h-screen bg-background-light">
      {/* Sidebar */}
      <aside className={`
        fixed top-0 left-0 h-full w-64 bg-white shadow-lg z-50 transform transition-transform duration-300
        ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0
      `}>
        <div className="p-6">
          <Link href="/dashboard" className="block">
            <h1 className="text-2xl font-bold text-primary">VocabKo</h1>
            <p className="text-sm text-gray-500">한국어 학습</p>
          </Link>
        </div>

        <nav className="px-4 space-y-1">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`
                flex items-center gap-3 px-4 py-3 rounded-lg transition
                ${pathname === item.href
                  ? 'bg-primary text-white'
                  : 'text-gray-700 hover:bg-gray-100'}
              `}
              onClick={() => setMobileMenuOpen(false)}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="font-medium">{item.label}</span>
            </Link>
          ))}
        </nav>

        <div className="absolute bottom-0 w-full p-4 border-t">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 transition"
          >
            <span className="text-xl">🚪</span>
            <span className="font-medium">Logout</span>
          </button>
        </div>
      </aside>

      {/* Mobile menu overlay */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Main content */}
      <div className="lg:ml-64">
        {/* Top bar */}
        <header className="bg-white shadow-sm sticky top-0 z-30">
          <div className="flex items-center justify-between px-6 py-4">
            <button
              className="lg:hidden text-2xl"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              ☰
            </button>

            <div className="flex items-center gap-6">
              <div className="flex items-center gap-2 bg-primary/10 px-4 py-2 rounded-lg">
                <span className="text-xl">⭐</span>
                <span className="font-semibold text-primary">{user.points} pts</span>
              </div>

              <div className="flex items-center gap-3">
                <div className="hidden sm:block text-right">
                  <p className="font-semibold text-gray-900">{user.username}</p>
                  <p className="text-sm text-gray-500">{user.level}</p>
                </div>
                <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center text-white font-bold">
                  {user.username[0]}
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
