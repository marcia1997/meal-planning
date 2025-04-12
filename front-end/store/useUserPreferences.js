import { create } from "zustand";
import axios from "axios";

const useUserPreferences = create((set) => ({
  preferences: { dietary_preferences: "", allergies: "", health_goals: "" },
  setPreferences: (preferences) => set({ preferences }),
  updatePreferences: async (newPreferences) => {
    try {
      const response = await axios.put("/api/users/preferences", newPreferences);
      set({ preferences: newPreferences });
      return response.data;
    } catch (error) {
      console.error("Error updating preferences", error);
    }
  },
}));

export default useUserPreferences;
