import { useLocation, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { MapIcon, CalendarIcon, ArrowLeftIcon } from '@heroicons/react/solid';

const imagePool = import.meta.glob('../assets/images/*.{jpg,jpeg,png,gif}', { eager: true });

type Trip = {
  destination: string;
  budget?: number;
  weather?: string;
  activities?: string[];
  accommodation_type?: string;
};

const TripResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    console.log("📦 TripResultsPage loaded with location.state:", location.state);
  }, [location]);

  const fallbackTrips: Trip[] = [
    {
      destination: 'Kyoto, Japan',
      budget: 1500,
      weather: 'Mild',
      activities: ['Cultural', 'Relaxation'],
      accommodation_type: 'Ryokan',
    },
  ];

  const trips: Trip[] = Array.isArray(location.state?.matches)
    ? location.state.matches
    : fallbackTrips;

  const enrichedTrips = trips.map((trip) => ({
    ...trip,
    budget: trip.budget ?? 1000,
    weather: trip.weather ?? 'Varied',
    activities: Array.isArray(trip.activities) ? trip.activities : ['Sightseeing', 'Local Food'],
  }));

  const getRandomImage = () => {
    const imagePaths = Object.values(imagePool);
    const randomImage = imagePaths[Math.floor(Math.random() * imagePaths.length)];
    return randomImage.default;
  };

  const viewDetails = (trip: Trip) => {
    navigate('/trip-details', { state: { trip } });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-100 via-white to-blue-50 p-6 pb-24">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div className="flex items-center gap-3">
            <CalendarIcon className="h-7 w-7 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-800">Matching Trips</h1>
          </div>
          <button
            onClick={() => navigate('/new-trip')}
            className="bg-gray-600 text-white flex items-center gap-2 px-4 py-2 rounded-full hover:bg-gray-800 transition"
          >
            <ArrowLeftIcon className="h-5 w-5" />
            Back to Planning
          </button>
        </div>

        {/* Trip Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {enrichedTrips.map((trip, idx) => (
            <div
              key={idx}
              className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-lg transform transition-transform hover:scale-105 hover:shadow-xl"
            >
              <img
                src={getRandomImage()}
                alt={trip.destination}
                className="w-full h-48 object-cover"
              />
              <div className="p-5">
                <h2 className="text-xl font-bold mb-2 text-gray-800">{trip.destination}</h2>
                <p className="text-sm text-gray-600 mb-1">💰 Budget: ${trip.budget}</p>
                <p className="text-sm text-gray-600 mb-1">🌤 Weather: {trip.weather}</p>
                <p className="text-sm text-gray-600 mb-1">🎯 Activities: {trip.activities.join(', ')}</p>
                <p className="text-sm text-gray-600 mb-4">🏨 Lodging: {trip.accommodation_type || 'N/A'}</p>

                <button
                  onClick={() => viewDetails(trip)}
                  className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-600 hover:text-white transition"
                >
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Optional Bottom Nav (if using on other pages too) */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-md flex justify-around py-3 z-50">
        <button onClick={() => navigate('/')} className="text-blue-600 text-sm flex flex-col items-center">
          <MapIcon className="h-6 w-6" />
          <span>Home</span>
        </button>
        <button onClick={() => navigate('/new-trip')} className="text-gray-600 text-sm flex flex-col items-center">
          <CalendarIcon className="h-6 w-6" />
          <span>Plan</span>
        </button>
      </nav>
    </div>
  );
};

export default TripResultsPage;
