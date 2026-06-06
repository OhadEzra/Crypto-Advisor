import { useEffect, useMemo, useState, type ReactNode } from 'react';
import {
  RefreshCw,
  Star,
  Newspaper,
  ThumbsUp,
  ThumbsDown,
  TrendingUp,
  TrendingDown,
  Sparkles,
  ShieldCheck,
} from 'lucide-react';
import Navbar from '../components/Navbar';
import VoteButtons from '../components/VoteButtons';
import { api } from '../services/api';

type AIRecommendation = {
  id: string;
  title: string;
  asset: string;
  type: string;
  confidence: number;
  reason: string;
  action: string;
};

type DashboardData = {
  user: {
    name: string;
    investorType: string;
    assets: string[];
    contentTypes: string[];
  };
  stats?: {
    watchlistCount: number;
    newsCount: number;
    feedbackCount: number;
    likes: number;
    dislikes: number;
  };
  feedbackSummary?: {
    totalVotes: number;
    likes: number;
    dislikes: number;
    likedSections: string[];
    dislikedSections: string[];
  };
  aiAdvisor?: {
    sentiment: {
      label: string;
      score: number;
      summary: string;
    };
    portfolioScore: {
  score: number;
  strengths: string[];
  weaknesses: string[];
};
    riskProfile: {
      level: string;
      summary: string;
      suggestion: string;
    };
    recommendations: AIRecommendation[];
  };
  sections: {
    prices: { id: string; name: string; price: number; change24h: number }[];
    news: { id: string; title: string; source: string; summary: string; url: string }[];
    insight: { id: string; text: string };
    meme: { id: string; title: string; image: string; source?: string };
    watchlist?: string[];
  };
};

const quickAssets = ['Bitcoin', 'Ethereum', 'Solana', 'Dogecoin', 'Cardano', 'Polygon'];

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [customAsset, setCustomAsset] = useState('');

  async function loadDashboard() {
    setLoading(true);
    setError('');

    try {
      const res = await api.get('/dashboard');
      setData(res.data);
    } catch {
      setError('Could not load dashboard');
    } finally {
      setLoading(false);
    }
  }

  async function addAsset(asset: string) {
    const cleanAsset = asset.trim();
    if (!cleanAsset) return;

    await api.post(`/dashboard/watchlist/${cleanAsset}`);
    setCustomAsset('');
    await loadDashboard();
  }

  async function removeAsset(asset: string) {
    await api.delete(`/dashboard/watchlist/${asset}`);
    await loadDashboard();
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  const stats = useMemo(() => {
    if (!data) return null;

    return data.stats || {
      watchlistCount: data.sections.watchlist?.length || data.user.assets.length,
      newsCount: data.sections.news.length,
      feedbackCount: 0,
      likes: 0,
      dislikes: 0,
    };
  }, [data]);

  if (error) {
    return (
      <main className="min-h-screen grid place-items-center px-6 text-center">
        <div className="card max-w-md">
          <h2 className="text-2xl font-black text-red-300 mb-2">Dashboard failed to load</h2>
          <p className="text-slate-300 mb-5">{error}</p>
          <button onClick={loadDashboard} className="btn">
            Try again
          </button>
        </div>
      </main>
    );
  }

  if (!data || !stats) {
    return (
      <main className="min-h-screen grid place-items-center text-slate-300">
        <div className="text-center">
          <RefreshCw className="animate-spin mx-auto mb-4 text-cyan-300" />
          Loading your crypto intelligence...
        </div>
      </main>
    );
  }

  const watchlist = data.sections.watchlist || data.user.assets;

  return (
    <main className="max-w-7xl mx-auto px-4 lg:px-6 pb-10 space-y-5">
      <Navbar />

      <section className="card mb-5 overflow-hidden relative bg-gradient-to-br from-cyan-400/10 via-slate-900 to-purple-500/10">
        <div className="absolute -top-24 -right-24 h-64 w-64 rounded-full bg-cyan-400/10 blur-3xl" />

        <div className="relative flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
          <div>
            <p className="badge inline-flex items-center gap-2 mb-3">
              <Sparkles size={14} />
              AI Crypto Advisor
            </p>

            <h2 className="text-2xl lg:text-3xl font-black tracking-tight">
              Welcome back, {data.user.name} 👋
            </h2>

            <p className="text-slate-300 mt-3 max-w-2xl">
              Track your watchlist, scan market updates, and get a personalized daily crypto brief built around your investor profile.
            </p>

            <div className="flex flex-wrap gap-2 mt-5">
              <span className="badge text-cyan-300">
                {data.user.investorType} investor
              </span>

              
            </div>
          </div>

          <button
            onClick={loadDashboard}
            disabled={loading}
            className="btn flex items-center justify-center gap-2 min-w-44"
          >
            <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
            {loading ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>
      </section>

      <section className="grid md:grid-cols-5 gap-4 mb-6">
        <StatCard icon={<Star size={18} />} label="Tracked Assets" value={stats.watchlistCount} hint="Personal watchlist" />
        <StatCard icon={<Newspaper size={18} />} label="Market Briefs" value={stats.newsCount} hint="Curated updates" />
        <StatCard icon={<ThumbsUp size={18} />} label="Positive Signals" value={stats.likes} hint="Liked content" />
        <StatCard icon={<ThumbsDown size={18} />} label="Negative Signals" value={stats.dislikes} hint="Disliked content" />
        <StatCard icon={<ShieldCheck size={18} />} label="Learning Signals" value={stats.feedbackCount} hint="Feedback stored" />
      </section>

      {data.aiAdvisor && (
  <section className="grid lg:grid-cols-3 gap-4 mb-6 items-start">
    <div className="card">
      <p className="badge mb-3">Market Sentiment</p>

      <h3 className="text-3xl font-black">
        {data.aiAdvisor.sentiment.label}
      </h3>

      <p className="text-cyan-300 text-xl mt-2">
        {data.aiAdvisor.sentiment.score}%
      </p>

      <p className="text-slate-400 mt-3">
        {data.aiAdvisor.sentiment.summary}
      </p>
    </div>

    <div className="card">
      <p className="badge mb-3">Risk Profile</p>

      <h3 className="text-3xl font-black">
        {data.aiAdvisor.riskProfile.level}
      </h3>

      <p className="text-slate-300 mt-3">
        {data.aiAdvisor.riskProfile.summary}
      </p>

      <p className="text-cyan-300 text-sm mt-4">
        {data.aiAdvisor.riskProfile.suggestion}
      </p>
    </div>

    <div className="card">
      <p className="badge mb-3">Portfolio Health</p>

      <h3 className="text-4xl font-black text-cyan-300">
        {data.aiAdvisor.portfolioScore.score}/100
      </h3>

      <div className="mt-4">
        <p className="text-emerald-300 font-bold text-sm mb-2">Strengths</p>

        {data.aiAdvisor.portfolioScore.strengths.length ? (
          <ul className="space-y-1">
            {data.aiAdvisor.portfolioScore.strengths.map(item => (
              <li key={item} className="text-slate-300 text-sm">
                ✓ {item}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-slate-500 text-sm">No clear strengths yet.</p>
        )}
      </div>

      <div className="mt-4">
        <p className="text-red-300 font-bold text-sm mb-2">Weaknesses</p>

        {data.aiAdvisor.portfolioScore.weaknesses.length ? (
          <ul className="space-y-1">
            {data.aiAdvisor.portfolioScore.weaknesses.map(item => (
              <li key={item} className="text-slate-300 text-sm">
                • {item}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-slate-500 text-sm">No major weaknesses detected.</p>
        )}
      </div>
    </div>

    <div className="card lg:col-span-3">
  <p className="badge mb-3">AI Recommendations</p>

      <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-3">
        {data.aiAdvisor.recommendations.map(rec => (
          <div
            key={rec.id}
            className="rounded-xl bg-slate-900/70 p-3 border border-white/5"
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <h4 className="font-bold">{rec.title}</h4>
                <p className="text-xs text-slate-500 mt-1">
                  {rec.type} · {rec.asset}
                </p>
              </div>

              <span className="badge text-cyan-300">
                {rec.confidence}%
              </span>
            </div>

            <p className="text-slate-400 text-sm mt-2">
              {rec.reason}
            </p>

            <p className="text-slate-300 text-sm mt-2">
              Suggested action: {rec.action}
            </p>
          </div>
        ))}
      </div>
    </div>
  </section>
)}

      {data.feedbackSummary && (
        <section className="card mb-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-5">
            <div>
              <p className="badge inline-flex items-center gap-2 mb-3">
                <Sparkles size={14} />
                AI Learning Engine
              </p>

              <h3 className="text-2xl font-black">
                Your advisor is learning from your feedback
              </h3>

              <p className="text-slate-400 mt-2">
                Every like and dislike helps personalize future recommendations.
              </p>
            </div>

            <div className="text-left lg:text-right">
              <p className="text-4xl font-black text-cyan-300">
                {data.feedbackSummary.totalVotes}
              </p>
              <p className="text-slate-400 text-sm">
                total feedback signals
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="rounded-2xl bg-slate-900/70 p-4 border border-white/5">
              <p className="text-emerald-300 font-bold mb-3">
                Preferred content
              </p>

              {data.feedbackSummary.likedSections.length ? (
                <div className="flex flex-wrap gap-2">
                  {data.feedbackSummary.likedSections.map(section => (
                    <span key={section} className="badge">
                      {section}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-slate-400">
                  No strong preferences yet. Start liking content to train the advisor.
                </p>
              )}
            </div>

            <div className="rounded-2xl bg-slate-900/70 p-4 border border-white/5">
              <p className="text-red-300 font-bold mb-3">
                Less relevant content
              </p>

              {data.feedbackSummary.dislikedSections.length ? (
                <div className="flex flex-wrap gap-2">
                  {data.feedbackSummary.dislikedSections.map(section => (
                    <span key={section} className="badge">
                      {section}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-slate-400">
                  No disliked patterns yet.
                </p>
              )}
            </div>
          </div>
        </section>
      )}

      <section className="grid lg:grid-cols-3 gap-6 mb-6">
        <section className="card lg:col-span-2">
          <div className="flex items-start justify-between gap-4 mb-5">
            <div>
              <h3 className="text-2xl font-black">Market Prices</h3>
              <p className="text-slate-400 text-sm mt-1">
                Live-style pricing view for your selected crypto assets.
              </p>
            </div>

            <span className="badge">
              {data.sections.prices.length} assets
            </span>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            {data.sections.prices.map(price => {
              const isUp = price.change24h >= 0;

              return (
                <div
                  key={price.id}
                  className="rounded-2xl bg-slate-900/70 p-4 border border-white/5"
                >
                  <div className="flex justify-between gap-4">
                    <div>
                      <strong className="text-lg">{price.name}</strong>
                      <p className="text-slate-500 text-sm">{price.id}</p>
                    </div>

                    <div className="text-right">
                      <p className="font-black">
                        ${Number(price.price).toLocaleString()}
                      </p>

                      <p className={isUp ? 'text-emerald-300 text-sm' : 'text-red-300 text-sm'}>
                        {isUp ? (
                          <TrendingUp size={14} className="inline mr-1" />
                        ) : (
                          <TrendingDown size={14} className="inline mr-1" />
                        )}
                        {price.change24h?.toFixed(2)}%
                      </p>
                    </div>
                  </div>

                  <VoteButtons section="prices" itemId={price.id} />
                </div>
              );
            })}
          </div>
        </section>

        <section className="card bg-gradient-to-br from-purple-500/10 to-cyan-400/10">
          <p className="badge inline-flex items-center gap-2 mb-3">
            <Sparkles size={14} />
            Market Intelligence
          </p>

          <h3 className="text-2xl font-black mb-4">
            AI Insight of the Day
          </h3>

         <div className="space-y-3">
  {data.sections.insight.text.split('\n\n').map((block, index) => (
    <div
      key={index}
      className="rounded-2xl bg-slate-950/60 border border-white/5 p-4"
    >
      <p className="text-slate-200 leading-7 text-sm whitespace-pre-line">
        {block}
      </p>
    </div>
  ))}
</div>

          <p className="text-xs text-slate-400 mt-5">
            Educational content only. Not financial advice.
          </p>

          <VoteButtons section="insight" itemId={data.sections.insight.id} />
        </section>
      </section>

      <section className="card mb-6">
        <h3 className="text-2xl font-black mb-2">Tracked Assets</h3>

        <p className="text-slate-300 mb-4">
          Manage the assets used for market analysis and personalized recommendations.
        </p>

        <div className="flex flex-wrap gap-2 mb-5">
          {watchlist.length ? (
            watchlist.map(asset => (
              <button
                key={asset}
                onClick={() => removeAsset(asset)}
                className="badge hover:bg-red-500/20 transition"
                title="Click to remove"
              >
                {asset} ✕
              </button>
            ))
          ) : (
            <p className="text-slate-400">
              No assets yet. Add one below.
            </p>
          )}
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {quickAssets.map(asset => (
            <button
              key={asset}
              onClick={() => addAsset(asset)}
              className="secondary-btn"
            >
              + {asset}
            </button>
          ))}
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <input
            className="input flex-1"
            placeholder="Add custom asset e.g. Avalanche"
            value={customAsset}
            onChange={e => setCustomAsset(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter') addAsset(customAsset);
            }}
          />

          <button onClick={() => addAsset(customAsset)} className="btn">
            Add Asset
          </button>
        </div>
      </section>

      <div className="grid lg:grid-cols-2 gap-6">
        <section className="card">
          <h3 className="text-2xl font-black mb-4">Market News</h3>

          <div className="space-y-4">
            {data.sections.news.map(item => (
              <article
                key={item.id}
                className="rounded-2xl bg-slate-900/70 p-4 border border-white/5"
              >
                <p className="text-sm text-cyan-300">
                  {item.source}
                </p>

                <h4 className="font-bold mt-1">
                  {item.title}
                </h4>

                <p className="text-slate-300 mt-2">
                  {item.summary}
                </p>

                {item.url !== '#' && (
                  <a
                    className="btn inline-block mt-4 text-sm"
                    href={item.url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Read Full Article →
                  </a>
                )}

                <VoteButtons section="news" itemId={item.id} />
              </article>
            ))}
          </div>
        </section>

        <section className="card">
          <h3 className="text-2xl font-black mb-4">Fun Crypto Meme</h3>

          <div className="rounded-2xl overflow-hidden bg-slate-900/70 border border-white/5">
            <img
  className="w-full h-80 object-contain bg-slate-950/40"
              src={data.sections.meme.image}
              alt={data.sections.meme.title}
            />

            <div className="p-4">
              <h4 className="font-bold">
                {data.sections.meme.title}
              </h4>
            <p className="text-sm text-cyan-300 mt-1">
  {data.sections.meme.source || 'Crypto Meme Library'}
</p>
              <VoteButtons section="meme" itemId={data.sections.meme.id} />
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}

function StatCard({
  icon,
  label,
  value,
  hint,
}: {
  icon: ReactNode;
  label: string;
  value: number;
  hint: string;
}) {
  return (
    <div className="card p-5 group">
      <div className="flex items-center justify-between mb-4">
        <div className="text-cyan-300 group-hover:scale-110 transition-transform">
          {icon}
        </div>
        <span className="text-[11px] text-slate-500">{hint}</span>
      </div>

      <p className="text-3xl font-black">{value}</p>
      <p className="text-slate-300 text-sm mt-1">{label}</p>
    </div>
  );
}