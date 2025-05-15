import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

// Import images dynamically from the assets/images folder
const imagePool = import.meta.glob('../assets/images/*.{jpg,jpeg,png,gif}', { eager: true });

const TripDetailsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const trip = location.state?.trip;

  const [cardBg, setCardBg] = useState<string | null>(null);

  useEffect(() => {
    if (!trip) {
      navigate('/trip-results');
    } else {
      console.log("Trip Details Page loaded with trip:", trip);

      // Pick a random background image for the info card
      const images = Object.values(imagePool);
      const random = images[Math.floor(Math.random() * images.length)];
      setCardBg(random.default);
    }
  }, [trip, navigate]);

  const handleAddToItinerary = () => {
    navigate('/trip-confirmation', { state: { trip } });
  };

  if (!trip || !cardBg) return null;

  return (
    <div className="min-h-screen bg-gray-50 px-6 py-10">
      <h1 className="text-3xl font-bold text-center text-purple-600 mb-6 animate__animated animate__fadeIn">
        Your Dream Trip Awaits!
      </h1>

      <div
        className="max-w-4xl mx-auto p-12 rounded-2xl shadow-lg text-white transition hover:shadow-2xl hover:scale-[1.02]"
        style={{
          backgroundImage: `url(${cardBg})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          maxHeight: '800px', // Ensure the card doesn’t shrink too much
        }}
      >
        <div className="backdrop-blur-sm bg-black/50 p-8 rounded-xl space-y-4">
          <h2 className="text-3xl font-bold text-yellow-300 text-center">
            {trip.destination}
          </h2>

          <p className="text-center text-lg text-blue-200 font-medium">
            Tailored Just for You.
          </p>

          <div className="space-y-3 text-lg">
            <p><strong>Budget:</strong> ${trip.budget}</p>
            <p><strong>Weather:</strong> {trip.weather}</p>
            <p>
              <strong>Activities:</strong>{' '}
              {Array.isArray(trip.activities)
                ? trip.activities.join(', ')
                : trip.activities || 'N/A'}
            </p>
            <p><strong>Lodging:</strong> {trip.accommodation_type || 'N/A'}</p>
          </div>
        </div>
      </div>

      <div className="mt-8 flex justify-center gap-6">
        <button
          onClick={() => navigate(-1)}
          className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-all hover:scale-105"
        >
          Back to Results
        </button>

        <button
          onClick={handleAddToItinerary}
          className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-all hover:scale-105"
        >
          Add to Itinerary
        </button>
      </div>
    </div>
  );
};

export default TripDetailsPage;
