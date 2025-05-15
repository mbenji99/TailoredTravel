import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { UserIcon } from "@heroicons/react/solid"; 

interface ProfileData {
  username: string;
  email: string;
  age: string;
  password: string;
}

interface OptionData {
  weather: string[];
  environment: string[];
  activity: string[];
  lodging: string[];
}

const ProfilePage = () => {
  const [profile, setProfile] = useState<ProfileData>({
    username: "",
    email: "",
    age: "",
    password: "",
  });

  const [preferences, setPreferences] = useState({
    weather: [] as string[],
    environment: [] as string[],
    activity: [] as string[],
    lodging: [] as string[],
  });

  const [options, setOptions] = useState<OptionData>({
    weather: [],
    environment: [],
    activity: [],
    lodging: [],
  });

  const [isEditing, setIsEditing] = useState(false);
  const [editingPreferences, setEditingPreferences] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUsername = localStorage.getItem("username") || "";
    const storedEmail = localStorage.getItem("email") || "";

    setTimeout(() => {
      setProfile({
        username: storedUsername,
        email: storedEmail,
        age: "34",
        password: "",
      });

      setOptions({
        weather: ["Hot", "Cold", "Tropical"],
        environment: ["Beach", "Mountain", "Historic"],
        activity: ["Adventure", "Relaxation", "Cultural"],
        lodging: ["Hotel", "AirBnB"],
      });
    }, 300);
  }, []);

  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  };

  const toggleSelection = (
    category: keyof typeof preferences,
    value: string
  ) => {
    setPreferences((prev) => ({
      ...prev,
      [category]: prev[category].includes(value)
        ? prev[category].filter((v) => v !== value)
        : [...prev[category], value],
    }));
  };

  const optionClass = (active: boolean) =>
    `px-4 py-2 border rounded-full text-sm font-semibold transition-all ${
      active
        ? "bg-green-300 text-black"
        : "bg-gray-100 text-gray-600 hover:bg-gray-200"
    }`;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    localStorage.setItem("username", profile.username);
    localStorage.setItem("email", profile.email);

    console.log("Profile:", profile);
    console.log("Preferences:", preferences);
    alert("Profile and preferences saved!");
    setIsEditing(false);
    setEditingPreferences(false);  // Close preferences section after saving
    navigate("/dashboard");
  };

  const toggleEdit = () => {
    setIsEditing((prev) => !prev);
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-purple-500 to-indigo-500 py-10 px-6">
      <div className="max-w-3xl mx-auto bg-white shadow-xl rounded-lg p-10 space-y-8">
        <div className="flex items-center space-x-4">
          {/* User Icon */}
          <UserIcon className="h-12 w-12 text-blue-700" />
          <h1 className="text-4xl font-bold text-blue-700">Your Profile</h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Profile Fields */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <label className="block font-bold mb-2 text-lg">Username</label>
              <input
                type="text"
                name="username"
                value={profile.username}
                onChange={handleProfileChange}
                disabled={!isEditing}
                className={`w-full p-4 border-2 rounded-lg bg-gray-100 ${
                  !isEditing ? "opacity-60 cursor-not-allowed" : ""
                }`}
                required
              />
            </div>

            <div>
              <label className="block font-bold mb-2 text-lg">Email</label>
              <input
                type="email"
                name="email"
                value={profile.email}
                onChange={handleProfileChange}
                disabled={!isEditing}
                className={`w-full p-4 border-2 rounded-lg bg-gray-100 ${
                  !isEditing ? "opacity-60 cursor-not-allowed" : ""
                }`}
                required
              />
            </div>

            <div>
              <label className="block font-bold mb-2 text-lg">Age</label>
              <input
                type="number"
                name="age"
                value={profile.age}
                onChange={handleProfileChange}
                disabled={!isEditing}
                className={`w-full p-4 border-2 rounded-lg bg-gray-100 ${
                  !isEditing ? "opacity-60 cursor-not-allowed" : ""
                }`}
              />
            </div>

            <div>
              <label className="block font-bold mb-2 text-lg">Change Password</label>
              <input
                type="password"
                name="password"
                value={profile.password}
                onChange={handleProfileChange}
                disabled={!isEditing}
                className={`w-full p-4 border-2 rounded-lg bg-gray-100 ${
                  !isEditing ? "opacity-60 cursor-not-allowed" : ""
                }`}
              />
            </div>
          </div>

          {/* Edit Toggle & Save Button */}
          <div className="flex justify-between items-center pt-4">
            <button
              type="button"
              onClick={toggleEdit}
              className="bg-yellow-500 text-white px-6 py-3 rounded-lg hover:bg-yellow-600 transition"
            >
              {isEditing ? "Cancel" : "Edit Profile"}
            </button>

            {isEditing && (
              <button
                type="submit"
                className="bg-blue-600 text-white font-bold px-6 py-3 rounded-lg hover:bg-blue-700 transition"
              >
                Save Profile
              </button>
            )}
          </div>

          {/* Preferences Section */}
          <div className="pt-6 border-t">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Set Personal Preferences</h2>
              <button
                type="button"
                onClick={() => setEditingPreferences((prev) => !prev)}
                className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition"
              >
                {editingPreferences ? "Cancel" : "Edit Preferences"}
              </button>
            </div>

            {editingPreferences && (
              <div className="space-y-8">
                {[ 
                  {
                    label: "Weather Preference",
                    key: "weather",
                    data: options.weather,
                  },
                  {
                    label: "Environment Preference",
                    key: "environment",
                    data: options.environment,
                  },
                  {
                    label: "Activity Type",
                    key: "activity",
                    data: options.activity,
                  },
                  {
                    label: "Lodging Preference",
                    key: "lodging",
                    data: options.lodging,
                  },
                ].map(({ label, key, data }) => (
                  <div key={key}>
                    <label className="block text-lg font-semibold">{label}</label>
                    <div className="flex flex-wrap gap-4">
                      {data.map((item) => (
                        <button
                          type="button"
                          key={item}
                          className={optionClass(
                            preferences[key as keyof typeof preferences].includes(item)
                          )}
                          onClick={() =>
                            toggleSelection(key as keyof typeof preferences, item)
                          }
                        >
                          {item}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
                {/* Save Preferences Button */}
                <div className="flex justify-end mt-6">
                  <button
                    type="button"
                    onClick={() => {
                      console.log("Preferences saved:", preferences);
                      alert("Preferences saved!");
                      setEditingPreferences(false);
                    }}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
                  >
                    Save Preferences
                  </button>
                </div>
              </div>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProfilePage;
