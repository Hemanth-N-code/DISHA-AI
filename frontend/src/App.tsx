// frontend/src/App.tsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { ErrorBoundary } from './components/ErrorBoundary';

// Pages
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { SignupPage } from './pages/SignupPage';
import { OnboardingPage } from './pages/OnboardingPage';
import { DashboardPage } from './pages/DashboardPage';
import { CareerDiscoveryPage } from './pages/CareerDiscoveryPage';
import { CareerDetailPage } from './pages/CareerDetailPage';
import { CareerGraphPage } from './pages/CareerGraphPage';
import { WhatIfPage } from './pages/WhatIfPage';
import { CareerComparisonPage } from './pages/CareerComparisonPage';
import { SkillGapPage } from './pages/SkillGapPage';
import { RoadmapPage } from './pages/RoadmapPage';
import { JourneyPage } from './pages/JourneyPage';
import { AssistantPage } from './pages/AssistantPage';
import { ProfilePage } from './pages/ProfilePage';
import { ResearchDashboardPage } from './pages/ResearchDashboardPage';

// CET Support Module Pages
import { CetLandingPage } from './pages/cet/CetLandingPage';
import { CetExplorerPage } from './pages/cet/CetExplorerPage';
import { CetCollegeDetailPage } from './pages/cet/CetCollegeDetailPage';
import { CetComparisonPage } from './pages/cet/CetComparisonPage';
import { CetOptionBuilderPage } from './pages/cet/CetOptionBuilderPage';


// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm font-medium text-slate-600">Loading your profile session...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans selection:bg-brand-500 selection:text-white">
      <Navbar />

      <main className="flex-1">
        <ErrorBoundary>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/research" element={<ResearchDashboardPage />} />

            {/* Semi-Public / Explorable Routes */}
            <Route path="/discover" element={<CareerDiscoveryPage />} />
            <Route path="/careers/:id" element={<CareerDetailPage />} />
            <Route path="/careers/:careerId" element={<CareerDetailPage />} />
            <Route path="/graph" element={<CareerGraphPage />} />
            <Route path="/graph/:id" element={<CareerGraphPage />} />
            <Route path="/assistant" element={<AssistantPage />} />

            {/* CET Support Module Routes */}
            <Route path="/cet" element={<CetLandingPage />} />
            <Route path="/cet/explore" element={<CetExplorerPage />} />
            <Route path="/cet/colleges/:id" element={<CetCollegeDetailPage />} />
            <Route path="/cet/compare" element={<CetComparisonPage />} />
            <Route path="/cet/option-list" element={<CetOptionBuilderPage />} />

            {/* Authenticated / Student Guided Routes */}
            <Route
              path="/onboarding"
              element={
                <ProtectedRoute>
                  <OnboardingPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/what-if"
              element={
                <ProtectedRoute>
                  <WhatIfPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/compare"
              element={
                <ProtectedRoute>
                  <CareerComparisonPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/skill-gap/:id"
              element={
                <ProtectedRoute>
                  <SkillGapPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/roadmap"
              element={
                <ProtectedRoute>
                  <RoadmapPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/journey"
              element={
                <ProtectedRoute>
                  <JourneyPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </ErrorBoundary>
      </main>

      <Footer />
    </div>
  );
};

export default App;
