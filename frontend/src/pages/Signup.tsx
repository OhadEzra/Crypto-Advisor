import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthShell from '../components/AuthShell';
import { api, saveAuth } from '../services/api';

export default function Signup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  async function submit(e: FormEvent) {
    e.preventDefault();
    setError('');
    try {
      const { data } = await api.post('/auth/signup', { name, email, password });
      saveAuth(data.access_token, data.name, data.is_onboarded);
      navigate('/onboarding');
    } catch {
      setError('Could not create account. Try another email.');
    }
  }

  return <AuthShell title="Create account" subtitle="Start with a quick onboarding quiz.">
    <form onSubmit={submit} className="space-y-4">
      <input className="input" placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
      <input className="input" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input className="input" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      {error && <p className="text-red-300">{error}</p>}
      <button className="btn w-full">Sign up</button>
      <p className="text-center text-slate-300">Already registered? <Link className="text-cyan-300" to="/login">Login</Link></p>
    </form>
  </AuthShell>;
}
