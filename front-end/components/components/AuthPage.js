import { useState } from 'react';
import { useRouter } from 'next/router';
import axios from '../utils/axiosInstance'; 

export default function AuthPage({ isRegister }) {
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState(null);
  const router = useRouter();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Set the correct endpoint based on isRegister flag
    const endpoint = isRegister ? '/auth/register' : '/auth/login';
    console.log("🚀 Calling endpoint:", endpoint); // Log the endpoint being called

    try {
      const response = await axios.post(endpoint, form);
      console.log(response.data); // Log the response for debugging

      // Handle success
      if (!isRegister) {
        localStorage.setItem('token', response.data.access_token); // Store token in localStorage
        router.push('/dashboard');
      } else {
        router.push('/login');
      }
    } catch (err) {
      console.error("🚨 Error:", err);
      setError(err.response?.data?.detail || 'Something went wrong'); // Show error message
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-2xl font-semibold text-center mb-4">
          {isRegister ? 'Register' : 'Login'}
        </h2>
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input 
            type="text" 
            name="username" 
            placeholder="Username" 
            className="w-full p-2 border rounded"
            value={form.username}
            onChange={handleChange}
            required
          />
          {isRegister && (
            <input 
              type="email" 
              name="email" 
              placeholder="Email" 
              className="w-full p-2 border rounded"
              value={form.email}
              onChange={handleChange}
              required
            />
          )}
          <input 
            type="password" 
            name="password" 
            placeholder="Password" 
            className="w-full p-2 border rounded"
            value={form.password}
            onChange={handleChange}
            required
          />
          <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">
            {isRegister ? 'Register' : 'Login'}
          </button>
        </form>
        <p className="text-center text-sm mt-4">
          {isRegister ? 'Already have an account?' : "Don't have an account?"} 
          <a href={isRegister ? '/login' : '/register'} className="text-blue-500"> 
            {isRegister ? 'Login' : 'Register'}
          </a>
        </p>
      </div>
    </div>
  );
}
