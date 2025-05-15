import { useLocation, useNavigate } from 'react-router-dom';

const TripConfirmationPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const trip = location.state?.trip;

    if (!trip) {
        navigate('/');
        return null;
    }

    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gray-50">
            <div className="bg-white p-8 rounded-lg shadow-lg max-w-md text-center">
                <h1 className="text-2xl font-bold text-green-700 mb-4">Trip Purchased!</h1>
                <p className="mb-2">You’ve successfully booked your trip to:</p>
                <h2 className="text-xl font-semibold text-olive-800">{trip.destination}</h2>

                <p className="mt-4 text-gray-600">
                    Get ready for an adventure with {trip.activity.join(', ')} in a {trip.environment} environment!
                </p>

                <button
                    onClick={() => navigate('/dashboard')}
                    className="mt-6 bg-gray-700 text-white px-4 py-2 rounded hover:bg-black"
                >
                    Back to Dashboard
                </button>
            </div>
        </div>
    );
};

export default TripConfirmationPage;
