import React, { useEffect, useState, useContext, useRef } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';

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

      // Fetch due counts for each deck
      fetchDueCount(''); // All cards
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
      fetchData(); // Refresh data
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
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Top Stats */}
      <div className="grid lg:grid-cols-4 mt-2 md:grid-cols-2 grid-cols-1 gap-6">
        <div className="stats shadow bg-base-100">
          <div className="stat">
            <div className="stat-figure text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-8 h-8"><path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" /></svg>
            </div>
            <div className="stat-title text-base-content/70">Total Reviews</div>
            <div className="stat-value text-primary">{analytics?.total_reviews || 0}</div>
            <div className="stat-desc font-bold text-success">Keep it up!</div>
          </div>
        </div>

        <div className="stats shadow bg-base-100">
          <div className="stat">
            <div className="stat-figure text-secondary">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-8 h-8"><path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" /></svg>
            </div>
            <div className="stat-title text-base-content/70">SmartDecks</div>
            <div className="stat-value text-secondary">{smartDecks.length}</div>
            <div className="stat-desc text-base-content/60">Custom Filters</div>
          </div>
        </div>

        <div className="stats shadow bg-base-100">
          <div className="stat">
            <div className="stat-figure text-accent">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-8 h-8"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            </div>
            <div className="stat-title text-base-content/70">Hardest Topic</div>
            <div className="stat-value text-accent text-xl">{hardestTopic}</div>
            <div className="stat-desc text-base-content/60">Needs attention</div>
          </div>
        </div>

        <div className="stats shadow bg-base-100 cursor-pointer hover:shadow-lg transition-shadow" onClick={() => modalRef.current.showModal()}>
          <div className="stat flex flex-col items-center justify-center h-full">
            <div className="text-primary opacity-80">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-10 h-10"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
            </div>
            <div className="stat-title font-semibold text-primary mt-1">Create SmartDeck</div>
          </div>
        </div>
      </div>

      {/* SmartDecks Grid */}
      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4 text-base-content">Study Queues</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {allDecksToRender.map(deck => {
            const count = dueCounts[deck.id];
            const isLoaded = count !== undefined;
            const hasCards = isLoaded && count > 0;

            return (
              <div key={deck.id || 'all'} className="card bg-base-100 shadow-md border border-base-200 hover:shadow-lg transition-shadow">
                <div className="card-body p-6">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="card-title text-base-content">{deck.name}</h3>
                    <div className="badge badge-ghost badge-sm">{deck.isAll ? 'System' : 'Custom'}</div>
                  </div>

                  <p className="text-sm text-base-content/60 mb-4 flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-4 h-4"><path strokeLinecap="round" strokeLinejoin="round" d="M21 11.25v8.25a1.5 1.5 0 01-1.5 1.5H5.25a1.5 1.5 0 01-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 109.375 7.5H12m0-2.625V7.5m0-2.625A2.625 2.625 0 1114.625 7.5H12m0 0V21m-8.625-9.75h18c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125h-18c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" /></svg>
                    Due Today:
                    {!isLoaded ? (
                      <span className="loading loading-dots loading-xs ml-1"></span>
                    ) : (
                      <span className="font-bold text-md text-secondary ml-1">{count}</span>
                    )}
                  </p>
                  <div className="card-actions mt-auto pt-2 border-t border-base-200">
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
            <h3 className="card-title text-lg mb-2 font-normal text-base-content/80">Avg. Hesitation (Seconds) by Topic</h3>
            <div className="w-full h-64">
              <Bar data={chartData} options={chartOptions} />
            </div>
          </div>
        </div>

        <div className="card bg-base-100 shadow-md">
          <div className="card-body">
            <h3 className="card-title text-lg mb-2 font-normal text-base-content/80">Cards You Struggle With (Lowest Ratings)</h3>
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
                        <td><span className="badge badge-error badge-sm">{card.avg_rating}</span></td>
                        <td className="text-sm truncate max-w-xs">{card.card_front}</td>
                      </tr>
                    ))
                  ) : (
                    <tr><td colSpan="2" className="text-success">No data available yet. Keep studying!</td></tr>
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
              <button type="button" className="btn btn-primary" onClick={handleCreateSmartDeck}>Save SmartDeck</button>
            </form>
          </div>
        </div>
        <form method="dialog" className="modal-backdrop">
          <button>close</button>
        </form>
      </dialog>
    </div>
  );
}

export default Dashboard;
