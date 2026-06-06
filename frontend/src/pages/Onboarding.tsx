import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';

const assets = ['Bitcoin', 'Ethereum', 'Solana', 'Dogecoin', 'Cardano', 'Polygon'];
const investorTypes = ['HODLer', 'Day Trader', 'NFT Collector', 'DeFi Investor'];
const contentTypes = ['Market News', 'Charts', 'Social', 'Fun'];

export default function Onboarding() {
  const [selectedAssets, setSelectedAssets] = useState<string[]>(['Bitcoin', 'Ethereum']);
  const [investorType, setInvestorType] = useState('HODLer');
  const [selectedContent, setSelectedContent] = useState<string[]>(['Market News', 'Charts']);
  const navigate = useNavigate();

  function toggle(value: string, values: string[], setter: (next: string[]) => void) {
    setter(values.includes(value) ? values.filter(v => v !== value) : [...values, value]);
  }

  async function submit() {
    await api.post('/users/preferences', { assets: selectedAssets, investor_type: investorType, content_types: selectedContent });
    localStorage.setItem('isOnboarded', 'true');
    navigate('/dashboard');
  }

  return <main className="min-h-screen px-6 py-10 max-w-5xl mx-auto">
    <section className="card">
      <p className="badge inline-block mb-4">Personalization quiz</p>
      <h1 className="text-4xl font-black">Tune your advisor</h1>
      <p className="text-slate-300 mt-2">Your answers shape the dashboard and future recommendations.</p>

      <div className="mt-8 space-y-8">
        <Question title="Which crypto assets are you interested in?" items={assets} selected={selectedAssets} onClick={(v) => toggle(v, selectedAssets, setSelectedAssets)} />
        <div>
          <h2 className="font-bold mb-3">What type of investor are you?</h2>
          <div className="flex flex-wrap gap-3">{investorTypes.map(type => <button key={type} onClick={() => setInvestorType(type)} className={type === investorType ? 'btn' : 'secondary-btn'}>{type}</button>)}</div>
        </div>
        <Question title="What kind of content would you like to see?" items={contentTypes} selected={selectedContent} onClick={(v) => toggle(v, selectedContent, setSelectedContent)} />
        <button onClick={submit} className="btn">Build my dashboard</button>
      </div>
    </section>
  </main>;
}

function Question({ title, items, selected, onClick }: { title: string; items: string[]; selected: string[]; onClick: (value: string) => void }) {
  return <div>
    <h2 className="font-bold mb-3">{title}</h2>
    <div className="flex flex-wrap gap-3">{items.map(item => <button key={item} onClick={() => onClick(item)} className={selected.includes(item) ? 'btn' : 'secondary-btn'}>{item}</button>)}</div>
  </div>;
}
