import { useState, useEffect } from "react";
import useUserPreferences from "../store/useUserPreferences";

export default function UserPreferencesForm() {
  const { preferences, updatePreferences } = useUserPreferences();
  const [formData, setFormData] = useState(preferences);

  useEffect(() => {
    console.log("Loaded preferences:", preferences);
    setFormData(preferences); // Ensure form updates when preferences change
  }, [preferences]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await updatePreferences(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto space-y-4">
      <label className="block">
        <span className="text-gray-700">Dietary Preferences:</span>
        <input type="text" name="dietary_preferences" value={formData.dietary_preferences} onChange={handleChange} className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" />
      </label>

      <label className="block">
        <span className="text-gray-700">Allergies:</span>
        <input type="text" name="allergies" value={formData.allergies} onChange={handleChange} className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" />
      </label>

      <label className="block">
        <span className="text-gray-700">Health Goals:</span>
        <input type="text" name="health_goals" value={formData.health_goals} onChange={handleChange} className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" />
      </label>

      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Save Preferences</button>
    </form>
  );
}
