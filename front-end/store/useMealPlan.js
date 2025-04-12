import { create } from "zustand";
import axios from "axios";

const useMealPlan = create((set) => ({
  mealPlan: {},
  generateMealPlan: async (days) => {
    try {
      const response = await axios.post("/api/generate-meal-plan", { days });
      set({ mealPlan: response.data.meal_plan });
      return response.data;
    } catch (error) {
      console.error("Error generating meal plan", error);
    }
  },
}));

export default useMealPlan;