import { LogOut } from 'lucide-react';
import { logout } from '../services/api';

export default function Navbar() {
  return <header className="flex items-center justify-between py-6">
    <div>
      <p className="text-sm text-cyan-300">Moveo Coding Task</p>
      <h1 className="text-2xl font-black">AI Crypto Advisor</h1>
    </div>
    <button onClick={logout} className="secondary-btn flex items-center gap-2"><LogOut size={16}/> Logout</button>
  </header>;
}
