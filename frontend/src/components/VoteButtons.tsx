import { useState } from 'react';
import { ThumbsDown, ThumbsUp } from 'lucide-react';
import { api } from '../services/api';

export default function VoteButtons({
  section,
  itemId,
}: {
  section: string;
  itemId: string;
}) {
  const [selectedVote, setSelectedVote] = useState<1 | -1 | null>(null);
  const [saved, setSaved] = useState(false);

  async function sendVote(vote: 1 | -1) {
    try {
      await api.post('/dashboard/vote', {
        section,
        item_id: itemId,
        vote,
      });

      setSelectedVote(vote);
      setSaved(true);

      setTimeout(() => {
        setSaved(false);
      }, 2000);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="flex items-center gap-2 pt-3">
      <button
        onClick={() => sendVote(1)}
        className={`secondary-btn transition-all duration-300 ${
          selectedVote === 1
            ? 'bg-cyan-500/20 border-cyan-400 text-cyan-300'
            : ''
        }`}
      >
        <ThumbsUp size={16} />
      </button>

      <button
        onClick={() => sendVote(-1)}
        className={`secondary-btn transition-all duration-300 ${
          selectedVote === -1
            ? 'bg-red-500/20 border-red-400 text-red-300'
            : ''
        }`}
      >
        <ThumbsDown size={16} />
      </button>

      {saved && (
        <span className="text-xs text-cyan-300 animate-pulse">
          ✓ Feedback saved
        </span>
      )}
    </div>
  );
}