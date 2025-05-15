import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { PlusIcon, MapIcon, CalendarIcon } from '@heroicons/react/solid';

const imagePool = import.meta.glob('../assets/images/*.{jpg,jpeg,png,gif}', { eager: true });

type Trip = {
  id: number;
  destination: string;
  budget: number;
  status: 'Recommended' | 'Saved' | 'Completed' | 'Planned';
  imageUrl: string;
};

const DashboardPage: React.FC = () => {
  const [username, setUsername] = useState('Traveler');
  const [trips, setTrips] = useState<Trip[]>([]);

  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) setUsername(storedUsername);
  }, []);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/recommendations/hybrid', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: 1,
            budget: 1000,
            weather: null,
            destination: null,
            activities: null,
            accommodation_type: null,
            top_n: 3,
          }),
        });

        const { recommendations } = await response.json();
        const formattedTrips: Trip[] = recommendations.map((rec: any, idx: number) => ({
          id: rec.id || idx + 1,
          destination: rec.name || rec.destination || 'Unknown Destination',
          budget: rec.budget || 100,
          status: 'Recommended',
          imageUrl: getRandomImage(),
        }));

        setTrips(formattedTrips);
      } catch (error) {
        console.error('❌ Error fetching recommendations:', error);
      }
    };

    fetchRecommendations();
  }, []);

  const getRandomImage = () => {
    const imagePaths = Object.values(imagePool);
    const randomImage = imagePaths[Math.floor(Math.random() * imagePaths.length)];
    return randomImage.default;
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-100 via-white to-blue-50 p-6 pb-24">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="flex justify-between items-center mb-8">
          <div className="flex items-center gap-3">
            <MapIcon className="h-8 w-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-800">Welcome, {username} 👋</h1>
          </div>
          <Link to="/new-trip">
            <button className="bg-green-600 flex items-center gap-2 text-white px-5 py-2 rounded-full hover:bg-green-700 transition">
              <PlusIcon className="h-5 w-5" />
              Plan New Trip
            </button>
          </Link>
        </header>

        {/* Content */}
        {trips.length === 0 ? (
          <div className="text-center mt-12 text-gray-600 text-lg">
            <p className="animate-pulse">Fetching recommendations...</p>
          </div>
        ) : (
          <section>
            <h2 className="text-2xl font-semibold text-gray-700 mb-6 flex items-center gap-2">
              <CalendarIcon className="h-6 w-6 text-blue-500" />
              Recommended Trips
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {trips.map((trip) => (
                <div
                  key={trip.id}
                  className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-lg transform transition-transform hover:scale-105 hover:shadow-xl"
                >
                  <img
                    src={trip.imageUrl}
                    alt={trip.destination}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-5">
                    <h3 className="text-xl font-bold mb-2 text-gray-800">{trip.destination}</h3>
                    <p className="text-sm text-gray-600 mb-1">💰 Budget: ${trip.budget}</p>
                    <p className="text-sm text-gray-600 mb-4">📌 Status: {trip.status}</p>
                    <Link to={`/trip-details/${trip.id}`}>
                      <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-600 hover:text-white transition">
                        View Details
                      </button>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>

      {/* Bottom Nav */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-md flex justify-around py-3 z-50">
        <Link to="/" className="text-blue-600 text-sm flex flex-col items-center">
          <MapIcon className="h-6 w-6" />
          <span>Home</span>
        </Link>
        <Link to="/new-trip" className="text-green-600 text-sm flex flex-col items-center">
          <PlusIcon className="h-6 w-6" />
          <span>Plan</span>
        </Link>
        <Link to="/trips" className="text-gray-500 text-sm flex flex-col items-center">
          <CalendarIcon className="h-6 w-6" />
          <span>Trips</span>
        </Link>
      </nav>
    </div>
  );
};

export default DashboardPage;
