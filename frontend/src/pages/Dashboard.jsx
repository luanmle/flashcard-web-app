import React, { useEffect, useState, useContext, useRef } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import {
  UserGroupIcon,
  CreditCardIcon,
  CircleStackIcon,
  UsersIcon,
  PlusCircleIcon,
  ListBulletIcon,
  ExclamationCircleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function Dashboard() {
  const { userId } = useContext(AuthContext);
  const navigate = useNavigate();

  const [smartDecks, setSmartDecks] = useState([]);
  const [dueCounts, setDueCounts] = useState({});
  const [analytics, setAnalytics] = useState(null);
  const [topics, setTopics] = useState([]);

  // Modal state
  const [newSdName, setNewSdName] = useState('');
  const [newSdTopic, setNewSdTopic] = useState('');
  const [newSdTags, setNewSdTags] = useState('');
  const modalRef = useRef(null);

  useEffect(() => {
    if (!userId) {
      navigate('/login');
      return;
    }
    fetchData();
  }, [userId]);

  const fetchData = async () => {
    try {
      const [sdRes, analyticsRes, topicsRes] = await Promise.all([
        axios.get(`/api/smart-decks/user/${userId}`),
        axios.get(`/api/analytics/${userId}`),
        axios.get('/api/topics/')
      ]);

      setSmartDecks(sdRes.data);
      setAnalytics(analyticsRes.data);
      setTopics(topicsRes.data);

      fetchDueCount('');
      sdRes.data.forEach(deck => fetchDueCount(deck.id));

    } catch (err) {
      console.error("Failed to fetch dashboard data", err);
    }
  };

  const fetchDueCount = async (deckId) => {
    try {
      const url = deckId ? `/api/study/due/${userId}?smart_deck_id=${deckId}` : `/api/study/due/${userId}`;
      const res = await axios.get(url);
      setDueCounts(prev => ({ ...prev, [deckId]: res.data.length }));
    } catch (err) {
      console.error("Failed to fetch due count", err);
      setDueCounts(prev => ({ ...prev, [deckId]: "Error" }));
    }
  };

  const handleCreateSmartDeck = async () => {
    if (!newSdName) {
      alert("SmartDeck name is required.");
      return;
    }

    let filter_criteria = {};
    if (newSdTopic) filter_criteria.topics = [newSdTopic];
    if (newSdTags) filter_criteria.tags = newSdTags.split(',').map(t => t.trim()).filter(t => t);

    try {
      await axios.post('/api/smart-decks/', {
        user_id: userId,
        name: newSdName,
        filter_criteria: filter_criteria
      });

      modalRef.current.close();
      setNewSdName('');
      setNewSdTopic('');
      setNewSdTags('');
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || "Error creating SmartDeck");
    }
  };

  // Prepare chart data
  let chartData = { labels: ['No Data'], datasets: [{ data: [0] }] };
  let hardestTopic = "N/A";

  if (analytics && analytics.avg_duration_by_topic) {
    const topicsList = Object.keys(analytics.avg_duration_by_topic);
    const durationsList = Object.values(analytics.avg_duration_by_topic);

    if (topicsList.length > 0) {
      chartData = {
        labels: topicsList,
        datasets: [{
          label: 'Avg Duration (s)',
          data: durationsList,
          backgroundColor: 'rgba(59, 130, 246, 0.8)',
          borderRadius: 6
        }]
      };

      let maxDur = 0;
      topicsList.forEach((t, i) => {
        if (durationsList[i] > maxDur) {
          maxDur = durationsList[i];
          hardestTopic = t;
        }
      });
      if (hardestTopic.length > 12) hardestTopic = hardestTopic.substring(0, 10) + '...';
    }
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { grid: { display: false } },
      y: { beginAtZero: true }
    }
  };

  const allCardsDeck = { id: '', name: 'All Cards (No Filter)', isAll: true };
  const allDecksToRender = [allCardsDeck, ...smartDecks];

  return (
    <>
      {/* Top Stats */}
      <div className="grid lg:grid-cols-4 mt-2 md:grid-cols-2 grid-cols-1 gap-6">

        <div className="stats shadow">
          <div className="stat">
            <div className="stat-figure dark:text-slate-300 text-primary">
              <CheckCircleIcon className='w-8 h-8'/>
            </div>
            <div className="stat-title dark:text-slate-300">Total Reviews</div>
            <div className="stat-value dark:text-slate-300 text-primary">{analytics?.total_reviews || 0}</div>
            <div className="stat-desc font-bold text-green-700 dark:text-green-300">Keep it up!</div>
          </div>
        </div>

        <div className="stats shadow">
          <div className="stat">
            <div className="stat-figure dark:text-slate-300 text-secondary">
              <RectangleStackIcon className='w-8 h-8'/>
            </div>
            <div className="stat-title dark:text-slate-300">SmartDecks</div>
            <div className="stat-value dark:text-slate-300 text-secondary">{smartDecks.length}</div>
            <div className="stat-desc">Custom Filters active</div>
          </div>
        </div>

        <div className="stats shadow">
          <div className="stat">
            <div className="stat-figure dark:text-slate-300 text-accent">
              <ExclamationCircleIcon className='w-8 h-8'/>
            </div>
            <div className="stat-title dark:text-slate-300">Hardest Topic</div>
            <div className="stat-value dark:text-slate-300 text-accent text-xl mt-1">{hardestTopic}</div>
            <div className="stat-desc font-bold text-rose-500 dark:text-red-400">Needs attention</div>
          </div>
        </div>

        <div className="stats shadow cursor-pointer hover:shadow-lg transition-shadow bg-primary text-primary-content" onClick={() => modalRef.current.showModal()}>
          <div className="stat flex flex-col items-center justify-center h-full">
            <div className="opacity-90">
              <PlusCircleIcon className="w-10 h-10" />
            </div>
            <div className="stat-title font-semibold mt-1 text-primary-content opacity-100">Create SmartDeck</div>
          </div>
        </div>
      </div>

      {/* SmartDecks Grid */}
      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4 text-base-content flex items-center gap-2">
          <ListBulletIcon className="w-6 h-6"/> Study Queues
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {allDecksToRender.map(deck => {
            const count = dueCounts[deck.id];
            const isLoaded = count !== undefined;
            const hasCards = isLoaded && count > 0;

            return (
              <div key={deck.id || 'all'} className="card bg-base-100 shadow-md border border-base-200 hover:shadow-lg transition-shadow">
                <div className="card-body p-6">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="card-title text-base-content font-bold">{deck.name}</h3>
                    <div className="badge badge-ghost badge-sm font-semibold">{deck.isAll ? 'System' : 'Custom'}</div>
                  </div>

                  <div className="text-sm text-base-content/60 mb-4 flex flex-col">
                    <span className="font-semibold mb-1">Due Today:</span>
                    {!isLoaded ? (
                      <span className="loading loading-dots loading-xs"></span>
                    ) : (
                      <span className="font-bold text-3xl text-secondary">{count}</span>
                    )}
                  </div>
                  <div className="card-actions mt-auto pt-4 border-t border-base-200">
                    <button
                      onClick={() => navigate(deck.id ? `/study/${userId}?smart_deck_id=${deck.id}` : `/study/${userId}`)}
                      className={`btn btn-sm w-full ${hasCards ? 'btn-primary' : 'btn-ghost'}`}
                      disabled={!hasCards}
                    >
                      {isLoaded ? (hasCards ? "Study Now" : "No cards due") : "Loading..."}
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Charts & Analytics */}
      <div className="grid lg:grid-cols-2 mt-8 grid-cols-1 gap-6">
        <div className="card bg-base-100 shadow-md">
          <div className="card-body">
            <h3 className="card-title text-lg mb-2 font-semibold">Avg. Hesitation (s) by Topic</h3>
            <div className="w-full h-64">
              <Bar data={chartData} options={chartOptions} />
            </div>
          </div>
        </div>

        <div className="card bg-base-100 shadow-md">
          <div className="card-body">
            <h3 className="card-title text-lg mb-2 font-semibold text-rose-500">Lowest Rated Cards</h3>
            <div className="overflow-x-auto">
              <table className="table table-zebra w-full">
                <thead>
                  <tr>
                    <th>Rating</th>
                    <th>Front Content</th>
                  </tr>
                </thead>
                <tbody>
                  {analytics?.hardest_cards?.length > 0 ? (
                    analytics.hardest_cards.map((card, i) => (
                      <tr key={i}>
                        <td><span className="badge badge-error badge-sm font-semibold">{card.avg_rating}</span></td>
                        <td className="text-sm truncate max-w-xs">{card.card_front}</td>
                      </tr>
                    ))
                  ) : (
                    <tr><td colSpan="2" className="text-success font-semibold">No data available yet. Keep studying!</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {/* Modal */}
      <dialog ref={modalRef} className="modal">
        <div className="modal-box">
          <h3 className="font-bold text-lg mb-4">Create a New SmartDeck</h3>
          <div className="space-y-4">
            <div className="form-control">
              <label className="label"><span className="label-text">SmartDeck Name</span></label>
              <input type="text" value={newSdName} onChange={(e)=>setNewSdName(e.target.value)} placeholder="e.g. My Math Deck" className="input input-bordered w-full" />
            </div>
            <div className="form-control">
              <label className="label"><span className="label-text">Filter by Topic (Optional)</span></label>
              <select value={newSdTopic} onChange={(e)=>setNewSdTopic(e.target.value)} className="select select-bordered w-full">
                <option value="">-- All Topics --</option>
                {topics.map(t => <option key={t.id} value={t.name}>{t.name}</option>)}
              </select>
            </div>
            <div className="form-control">
              <label className="label"><span className="label-text">Filter by Tags (Optional)</span></label>
              <input type="text" value={newSdTags} onChange={(e)=>setNewSdTags(e.target.value)} placeholder="e.g. hard, math, algebra" className="input input-bordered w-full" />
              <label className="label"><span className="label-text-alt text-base-content/60">Comma-separated</span></label>
            </div>
          </div>
          <div className="modal-action">
            <form method="dialog">
              <button className="btn btn-ghost mr-2">Cancel</button>
              <button type="button" className="btn btn-primary" onClick={handleCreateSmartDeck}>Save</button>
            </form>
          </div>
        </div>
        <form method="dialog" className="modal-backdrop">
          <button>close</button>
        </form>
      </dialog>
    </>
  );
}

export default Dashboard;
