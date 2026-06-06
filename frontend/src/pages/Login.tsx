import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthShell from '../components/AuthShell';
import { api, saveAuth } from '../services/api';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  async function submit(e: FormEvent) {
    e.preventDefault();
    setError('');
    try {
      const { data } = await api.post('/auth/login', { email, password });
      saveAuth(data.access_token, data.name, data.is_onboarded);
      navigate(data.is_onboarded ? '/dashboard' : '/onboarding');
    } catch {
      setError('Invalid email or password');
    }
  }

  return <AuthShell title="Welcome back" subtitle="Login to your personalized crypto dashboard.">
    <form onSubmit={submit} className="space-y-4">
      <input className="input" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input className="input" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      {error && <p className="text-red-300">{error}</p>}
      <button className="btn w-full">Login</button>
      <p className="text-center text-slate-300">No account? <Link className="text-cyan-300" to="/signup">Create one</Link></p>
    </form>
  </AuthShell>;
}
