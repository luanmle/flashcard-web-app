import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { useParams, useSearchParams, useNavigate } from 'react-router-dom';

function Study() {
  const { userId } = useContext(AuthContext);
  const { userId: urlUserId } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const smartDeckId = searchParams.get('smart_deck_id');

  const [cards, setCards] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [loading, setLoading] = useState(true);
  const [statusMsg, setStatusMsg] = useState('');

  useEffect(() => {
    // If not logged in, or URL ID doesn't match context ID
    if (!userId || userId !== urlUserId) {
      navigate('/login');
      return;
    }
    fetchCards();
  }, [userId, urlUserId, smartDeckId]);

  const fetchCards = async () => {
    setLoading(true);
    try {
      const url = smartDeckId ? `/api/study/due/${userId}?smart_deck_id=${smartDeckId}` : `/api/study/due/${userId}`;
      const res = await axios.get(url);
      setCards(res.data);
      if (res.data.length > 0) {
        setStartTime(Date.now());
      }
    } catch (e) {
      console.error(e);
      setStatusMsg("Failed to load cards.");
    } finally {
      setLoading(false);
    }
  };

  const handleShowAnswer = () => {
    setShowAnswer(true);
  };

  const submitReview = async (rating) => {
    const currentCard = cards[currentIndex];
    const durationMs = Date.now() - startTime;
    const durationSec = Math.floor(durationMs / 1000);

    try {
      await axios.post('/api/reviews/', {
        user_id: userId,
        card_id: currentCard.id,
        rating: rating,
        duration_seconds: durationSec
      });

      // Move to next card
      if (currentIndex + 1 < cards.length) {
        setCurrentIndex(currentIndex + 1);
        setShowAnswer(false);
        setStartTime(Date.now());
      } else {
        setStatusMsg("You have finished all due cards for today!");
      }
    } catch (e) {
      console.error("Failed to submit review", e);
      alert("Error submitting review");
    }
  };

  if (loading) {
    return <div className="text-center mt-20"><span className="loading loading-spinner loading-lg text-primary"></span></div>;
  }

  if (statusMsg) {
    return (
      <div className="max-w-2xl mx-auto mt-10">
        <div className="alert alert-success shadow-md text-center">
          <span className="font-bold text-lg">{statusMsg}</span>
        </div>
        <button className="btn btn-primary mt-6 w-full" onClick={() => navigate('/dashboard')}>Back to Dashboard</button>
      </div>
    );
  }

  if (cards.length === 0) {
    return (
      <div className="max-w-2xl mx-auto mt-10 text-center">
        <h2 className="text-2xl font-bold mb-4">No cards due!</h2>
        <button className="btn btn-primary" onClick={() => navigate('/dashboard')}>Back to Dashboard</button>
      </div>
    );
  }

  const currentCard = cards[currentIndex];

  // Render cloze content
  const renderFront = (text, type) => {
    if (type === 'cloze') {
      const parts = text.split(/(\{\{c1::.*?\}\})/g);
      return parts.map((part, i) => {
        if (part.startsWith('{{c1::') && part.endsWith('}}')) {
          return showAnswer ?
            <span key={i} className="text-primary font-bold">{part.slice(6, -2)}</span> :
            <span key={i} className="bg-base-300 text-transparent select-none px-2 rounded">[...]</span>;
        }
        return <span key={i}>{part}</span>;
      });
    }
    return text;
  };

  return (
    <div className="max-w-3xl mx-auto mt-10">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Study Session</h2>
        <span className="badge badge-primary">{currentIndex + 1} / {cards.length}</span>
      </div>

      <div className="card bg-base-100 shadow-xl border border-base-200 min-h-[300px]">
        <div className="card-body text-center flex flex-col justify-center">

          <div className="text-2xl mb-8 whitespace-pre-wrap">
            {renderFront(currentCard.front_content, currentCard.card_type)}
          </div>

          <div className={`mt-4 pt-6 border-t border-base-200 transition-opacity duration-300 ${showAnswer ? 'opacity-100' : 'opacity-0 hidden'}`}>
            <h3 className="text-sm font-semibold text-base-content/60 uppercase mb-2">Answer</h3>
            <div className="text-xl whitespace-pre-wrap">{currentCard.back_content}</div>
          </div>

        </div>
      </div>

      <div className="mt-8 flex justify-center gap-4">
        {!showAnswer ? (
          <button className="btn btn-primary btn-lg w-full max-w-md" onClick={handleShowAnswer}>
            Show Answer
          </button>
        ) : (
          <div className="grid grid-cols-4 gap-4 w-full">
            <button className="btn btn-error" onClick={() => submitReview(1)}>1 - Again</button>
            <button className="btn btn-warning" onClick={() => submitReview(2)}>2 - Hard</button>
            <button className="btn btn-success" onClick={() => submitReview(3)}>3 - Good</button>
            <button className="btn btn-info" onClick={() => submitReview(4)}>4 - Easy</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default Study;
