import React, { useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    if (!username || !email) {
      setError("Please provide both username and email");
      return;
    }

    try {
      let res = await axios.post('/api/users/', { username, email });
      login(res.data.id);
      navigate('/dashboard');
    } catch (err) {
      // Fallback for MVP
      try {
        const allRes = await axios.get('/api/users/');
        const existing = allRes.data.find(u => u.username === username);
        if (existing) {
          login(existing.id);
          navigate('/dashboard');
        } else {
          setError(err.response?.data?.detail || "Error creating user");
        }
      } catch (fallbackErr) {
        setError("Error connecting to server");
      }
    }
  };

  return (
    <div className="card bg-base-100 shadow-xl border border-primary max-w-2xl mx-auto mt-10">
      <div className="card-body">
        <h2 className="card-title text-primary text-2xl mb-4">Select or Create User</h2>
        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <div className="form-control">
            <input
              type="text"
              placeholder="Enter username"
              className="input input-bordered w-full"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="form-control">
            <input
              type="email"
              placeholder="Enter email"
              className="input input-bordered w-full"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          {error && <p className="text-error text-sm">{error}</p>}
          <button type="submit" className="btn btn-primary mt-2">Set User</button>
        </form>
      </div>
    </div>
  );
}

export default Login;
