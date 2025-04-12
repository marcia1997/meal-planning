import { useState } from "react";
import axios from "axios";

export default function MealPlanPage() {
  const [days, setDays] = useState(7);
  const [mealPlan, setMealPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const generateMealPlan = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/generate-meal-plan", { days }, {
        withCredentials: true, // Ensures auth token is sent
      });
      setMealPlan(response.data.meal_plan);
    } catch (error) {
      console.error("Error generating meal plan", error);
    }
    setLoading(false);
  };
  
  return (
    <div className="max-w-lg mx-auto p-6 bg-white rounded-lg shadow-md mt-10">
      <h1 className="text-2xl font-bold mb-4">Generate Meal Plan</h1>
      <label className="block mb-2">
        <span className="text-gray-700">Number of days:</span>
        <input
          type="number"
          value={days}
          onChange={(e) => setDays(e.target.value)}
          className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
          min="1"
          max="7"
        />
      </label>
      <button
        onClick={generateMealPlan}
        className="w-full bg-blue-500 text-white py-2 px-4 rounded-md mt-2 hover:bg-blue-600"
        disabled={loading}
      >
        {loading ? "Generating..." : "Generate"}
      </button>
      {mealPlan && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold">Your Meal Plan:</h2>
          <ul className="mt-2 space-y-2">
            {Object.entries(mealPlan).map(([day, meals]) => (
              <li key={day} className="p-3 bg-gray-100 rounded-md">
                <strong>{day}:</strong>
                <ul className="ml-4 list-disc">
                  {meals.map((meal, index) => (
                    <li key={index}>{meal}</li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
