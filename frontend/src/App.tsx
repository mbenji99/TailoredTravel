import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import DashboardPage from './pages/DashboardPage';
import NewTripPage from './pages/NewTripPage';
import TripResultsPage from './pages/TripResultsPage';
import TripDetailsPage from './pages/TripDetailsPage';
import TripConfirmationPage from './pages/TripConfirmationPage';
import ProfilePage from './pages/ProfilePage';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  const hideNavbar = location.pathname === '/login' || location.pathname === '/signup';

  return (
    <div className="min-h-screen">
      {!hideNavbar && <Navbar />}
      {children}
    </div>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/new-trip" element={<NewTripPage />} />
          <Route path="/trip-results" element={<TripResultsPage />} />
          <Route path="/trip-details" element={<TripDetailsPage />} />
          <Route path="/trip-confirmation" element={<TripConfirmationPage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;
