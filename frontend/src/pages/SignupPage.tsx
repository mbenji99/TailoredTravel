import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser } from '../services/authService';
import logo from '../assets/logo.png'; 

const SignupPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const navigate = useNavigate();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    setIsSubmitting(true);

    try {
      const response = await registerUser(username, email, password);

      if (response.success) {
        localStorage.setItem('username', username);
        localStorage.setItem('email', email);
        setSuccessMessage('Signup successful! Redirecting to login...');
        setTimeout(() => navigate('/login'), 2000);
      } else {
        setError(response.message || 'Something went wrong, please try again.');
      }
    } catch (err) {
      console.error(err);
      setError('Error occurred. Please try again later.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-center px-4"
      style={{ backgroundImage: "url('https://source.unsplash.com/1600x900/?adventure,explore')" }}
    >
      <div className="bg-white/90 backdrop-blur-md rounded-3xl shadow-xl p-10 w-full max-w-md">
        {/* Logo and Title */}
        <div className="flex items-center justify-center mb-6">
          <img src={logo} alt="Tailored Travels Logo" className="h-16 w-16 mr-3" />
          <h1 className="text-4xl font-extrabold text-yellow-500 tracking-tight">Tailored Travels</h1>
        </div>

        <h2 className="text-center text-xl font-semibold text-gray-800 mb-6">
          Create Your Account
        </h2>

        <form onSubmit={handleSignup} className="space-y-5">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              placeholder="e.g. travel_buddy"
            />
          </div>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              placeholder="Create a strong password"
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 rounded-xl transition shadow-sm disabled:opacity-60"
          >
            {isSubmitting ? 'Signing Up...' : 'Sign Up'}
          </button>
        </form>

        {/* Success & Error Messages */}
        {successMessage && (
          <p className="mt-4 text-green-600 text-center text-sm">{successMessage}</p>
        )}
        {error && (
          <p className="mt-4 text-red-600 text-center text-sm">{error}</p>
        )}

        {/* Redirect to Login */}
        <p className="text-center text-sm text-gray-600 mt-5">
          Already have an account?{' '}
          <span
            onClick={() => navigate('/login')}
            className="text-blue-500 hover:underline cursor-pointer font-medium"
          >
            Log in
          </span>
        </p>
      </div>
    </div>
  );
};

export default SignupPage;
