import React, { useState, type FormEvent } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { loginUser } from '../api/auth';
import { Link, useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png'; 

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [rememberMe, setRememberMe] = useState<boolean>(false);
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const res = await loginUser(email, password);
      localStorage.setItem('token', res.token);
      localStorage.setItem('user_id', res.user_id);
      setTimeout(() => navigate('/dashboard'), 500);
    } catch (err: any) {
      alert(err.response?.data?.error || 'Login failed');
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-center px-4"
      style={{ backgroundImage: "url('https://source.unsplash.com/1600x900/?travel,nature')" }}
    >
      <div className="bg-white/90 backdrop-blur-md rounded-3xl shadow-xl p-10 w-full max-w-md">
        {/* Logo + Brand */}
        <div className="flex items-center justify-center mb-6">
          <img src={logo} alt="Tailored Travels" className="h-16 w-16 mr-3" />
          <h1 className="text-4xl font-extrabold text-yellow-500 tracking-tight">Tailored Travels</h1>
        </div>

        <h2 className="text-center text-xl font-semibold text-gray-800 mb-6">
          Welcome Back, Traveler ✈️
        </h2>

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Email */}
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

          {/* Password */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 pr-10 transition"
                placeholder="••••••••"
              />
              <button
                type="button"
                className="absolute right-3 top-2.5 text-gray-500 hover:text-gray-700"
                onClick={() => setShowPassword(prev => !prev)}
                aria-label="Toggle password visibility"
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>

          {/* Remember Me + Forgot */}
          <div className="flex items-center justify-between text-sm">
            <label className="flex items-center gap-2 text-gray-600">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="accent-blue-500"
              />
              Remember me
            </label>
            <a href="#" className="text-blue-500 hover:underline">Forgot password?</a>
          </div>

          {/* Login Button */}
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 rounded-xl transition shadow-sm"
          >
            Log In
          </button>
        </form>

        {/* Signup Link */}
        <p className="text-center text-gray-600 mt-5 text-sm">
          Don’t have an account?{' '}
          <Link to="/signup" className="text-blue-500 hover:underline font-medium">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
