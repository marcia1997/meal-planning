import { useState, useEffect } from "react";
import axios from "axios";

export default function Preferences() {
  const [preferences, setPreferences] = useState({
    dietary_preferences: [],
    allergies: [],
    health_goals: "",
  });
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Fetch user preferences from the backend
    axios.get("/app/user/preferences")
      .then((res) => setPreferences(res.data))
      .catch((err) => console.error(err));
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setPreferences({ ...preferences, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.put("/app/user/preferences", preferences);
      setMessage(res.data.message);
    } catch (error) {
      console.error(error);
      setMessage("Error updating preferences");
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-4">Update Preferences</h2>
      {message && <p className="text-green-600">{message}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <label className="block">
          <span className="text-gray-700">Dietary Preferences</span>
          <input
            type="text"
            name="dietary_preferences"
            value={preferences.dietary_preferences}
            onChange={handleChange}
            className="mt-1 block w-full p-2 border rounded"
          />
        </label>

        <label className="block">
          <span className="text-gray-700">Allergies</span>
          <input
            type="text"
            name="allergies"
            value={preferences.allergies}
            onChange={handleChange}
            className="mt-1 block w-full p-2 border rounded"
          />
        </label>

        <label className="block">
          <span className="text-gray-700">Health Goals</span>
          <input
            type="text"
            name="health_goals"
            value={preferences.health_goals}
            onChange={handleChange}
            className="mt-1 block w-full p-2 border rounded"
          />
        </label>

        <button type="submit" className="bg-blue-500 text-white p-2 rounded hover:bg-blue-700">
          Save Preferences
        </button>
      </form>
    </div>
  );
}
