import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png'; 
const Navbar: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();

    const handleLogout = () => {
        console.log('Logging out...');
        navigate('/login');
    };

    return (
        <nav className="bg-white shadow-md px-4 py-3 flex justify-between items-center">
            {/* Brand Section with Logo */}
            <Link to="/" className="flex items-center space-x-2">
                <img src={logo} alt="Tailored Travels Logo" className="w-18 h-18" />
                <span className="text-2xl font-bold text-yellow-500">Tailored Travels</span>
            </Link>

            {/* Navigation Links */}
            <div className="flex items-center space-x-6 font-bold">
                <Link to="/dashboard" className="text-gray-700 text-xl hover:text-blue-500">Dashboard</Link>
                <Link to="/trip-details" className="text-gray-700 text-xl hover:text-blue-500">View Trips</Link>
                <Link to="/profile" className="text-gray-700 text-xl hover:text-blue-500">Profile</Link>

                {location.pathname === '/dashboard' && (
                    <button
                        onClick={handleLogout}
                        className="text-blue-600 text-xl hover:underline"
                    >
                        Log out
                    </button>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
