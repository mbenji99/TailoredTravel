import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';

interface OptionData {
  weather: string[];
  activity: string[];
  lodging: string[];
}

const NewTripPage: React.FC = () => {
  const [budgetMin, setBudgetMin] = useState('');
  const [budgetMax, setBudgetMax] = useState('');
  const [weather, setWeather] = useState<string[]>([]);
  const [activity, setActivity] = useState<string[]>([]);
  const [lodging, setLodging] = useState<string[]>([]);
  const [options, setOptions] = useState<OptionData>({
    weather: [],
    activity: [],
    lodging: [],
  });

  const navigate = useNavigate();

  useEffect(() => {
    async function fetchOptions() {
      const data: OptionData = await new Promise((resolve) =>
        setTimeout(
          () =>
            resolve({
              weather: ['Hot', 'Cold', 'Tropical'],
              activity: ['Adventure', 'Relaxation', 'Cultural'],
              lodging: ['Hotel', 'AirBnB'],
            }),
          500
        )
      );
      setOptions(data);
    }
    fetchOptions();
  }, []);

  const toggleSelection = (
    value: string,
    current: string[],
    setCurrent: (val: string[]) => void
  ) => {
    setCurrent(
      current.includes(value)
        ? current.filter((v) => v !== value)
        : [...current, value]
    );
  };

  const optionClass = (active: boolean) =>
    `px-4 py-2 rounded-full border text-sm transition ${
      active
        ? 'bg-green-200 text-green-900 font-semibold'
        : 'bg-white text-gray-600 border-gray-300'
    } hover:bg-green-300 hover:text-black cursor-pointer`;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const budget = budgetMin && budgetMax
      ? (parseFloat(budgetMin) + parseFloat(budgetMax)) / 2
      : parseFloat(budgetMax || budgetMin);

    if (isNaN(budget)) {
      alert('Please enter a valid budget.');
      return;
    }

    const tripData = {
      user_id: 1,
      budget,
      weather: weather.length > 0 ? weather[0] : null,
      activities: activity.length > 0 ? activity.join(',') : null,
      accommodation_type: lodging.length > 0 ? lodging[0] : null,
      top_n: 10,
    };

    try {
      const response = await fetch('http://localhost:5000/api/recommendations/hybrid', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tripData),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.error || 'Failed to fetch recommendations');
      }

      const { recommendations } = await response.json();
      navigate('/trip-results', { state: { matches: recommendations } });
    } catch (err: any) {
      console.error('Recommendation fetch error:', err);
      alert(err.message || 'Something went wrong. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-teal-100 via-white to-blue-50 px-6 py-12">
      <div className="max-w-3xl mx-auto relative bg-white/70 backdrop-blur-md rounded-2xl shadow-xl p-8 sm:p-12 border border-gray-200">
        <img
          src={logo}
          alt="Tailored Travels Logo"
          className="absolute top-6 right-6 h-25 w-auto drop-shadow"
        />

        <h1 className="text-3xl font-extrabold text-center text-blue-900 mb-10">Let's Plan a Trip</h1>

        <form onSubmit={handleSubmit} className="space-y-10">

          {/* Budget Range */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <label className="block mb-2 text-lg font-medium text-gray-800">Budget Min</label>
              <input
                type="number"
                placeholder="$0"
                value={budgetMin}
                onChange={(e) => setBudgetMin(e.target.value)}
                className="w-full rounded-md bg-white p-3 border border-gray-300 text-gray-700 focus:ring-2 focus:ring-blue-300"
              />
            </div>
            <div>
              <label className="block mb-2 text-lg font-medium text-gray-800">Budget Max</label>
              <input
                type="number"
                placeholder="$1000"
                value={budgetMax}
                onChange={(e) => setBudgetMax(e.target.value)}
                className="w-full rounded-md bg-white p-3 border border-gray-300 text-gray-700 focus:ring-2 focus:ring-blue-300"
              />
            </div>
          </div>

          {/* Weather Filter */}
          <div>
            <label className="block mb-3 text-lg font-medium text-gray-800">Weather Preference</label>
            <div className="flex flex-wrap gap-3">
              {options.weather.map((item) => (
                <button
                  key={item}
                  type="button"
                  className={optionClass(weather.includes(item))}
                  onClick={() => toggleSelection(item, weather, setWeather)}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>

          {/* Activity Filter */}
          <div>
            <label className="block mb-3 text-lg font-medium text-gray-800">Activity Type</label>
            <div className="flex flex-wrap gap-3">
              {options.activity.map((item) => (
                <button
                  key={item}
                  type="button"
                  className={optionClass(activity.includes(item))}
                  onClick={() => toggleSelection(item, activity, setActivity)}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>

          {/* Lodging Filter */}
          <div>
            <label className="block mb-3 text-lg font-medium text-gray-800">Lodging Preference</label>
            <div className="flex flex-wrap gap-3">
              {options.lodging.map((item) => (
                <button
                  key={item}
                  type="button"
                  className={optionClass(lodging.includes(item))}
                  onClick={() => toggleSelection(item, lodging, setLodging)}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 text-lg font-semibold rounded-md hover:bg-blue-700 transition-all focus:ring-2 focus:ring-blue-400"
          >
            Plan My Trip!
          </button>
        </form>
      </div>
    </div>
  );
};

export default NewTripPage;
