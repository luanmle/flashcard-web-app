import React, { useState, useEffect, useContext, useRef } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { InformationCircleIcon } from '@heroicons/react/24/outline';

function Studio() {
  const { userId } = useContext(AuthContext);

  const [topics, setTopics] = useState([]);
  const [subtopics, setSubtopics] = useState([]);

  const [selectedTopic, setSelectedTopic] = useState('');
  const [selectedSubtopic, setSelectedSubtopic] = useState('');

  const [newTopicName, setNewTopicName] = useState('');
  const [newSubtopicName, setNewSubtopicName] = useState('');

  const [cardType, setCardType] = useState('basic');
  const [frontContent, setFrontContent] = useState('');
  const [backContent, setBackContent] = useState('');
  const [tags, setTags] = useState('');

  const [status, setStatus] = useState({ message: '', isError: false });
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchTopics();
  }, []);

  useEffect(() => {
    if (selectedTopic) {
      fetchSubtopics(selectedTopic);
    } else {
      setSubtopics([]);
      setSelectedSubtopic('');
    }
  }, [selectedTopic]);

  const showStatus = (message, isError = false) => {
    setStatus({ message, isError });
    setTimeout(() => setStatus({ message: '', isError: false }), 5000);
  };

  const fetchTopics = async () => {
    try {
      const res = await axios.get('/api/topics/');
      setTopics(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchSubtopics = async (topicId) => {
    try {
      const res = await axios.get('/api/subtopics/');
      const filtered = res.data.filter(s => s.topic_id === topicId);
      setSubtopics(filtered);
    } catch (e) {
      console.error(e);
    }
  };

  const handleCreateTopic = async () => {
    if (!newTopicName.trim()) return;
    try {
      await axios.post('/api/topics/', { name: newTopicName });
      setNewTopicName('');
      fetchTopics();
      showStatus(`Topic '${newTopicName}' created!`);
    } catch (e) {
      showStatus(e.response?.data?.detail || "Error creating topic", true);
    }
  };

  const handleCreateSubtopic = async () => {
    if (!newSubtopicName.trim() || !selectedTopic) return;
    try {
      await axios.post('/api/subtopics/', { name: newSubtopicName, topic_id: selectedTopic });
      setNewSubtopicName('');
      fetchSubtopics(selectedTopic);
      showStatus(`Subtopic '${newSubtopicName}' created!`);
    } catch (e) {
      showStatus("Error creating subtopic", true);
    }
  };

  const handleCreateCard = async () => {
    if (!selectedSubtopic) {
      showStatus("Please select a Subtopic first.", true);
      return;
    }
    if (!frontContent.trim() || !backContent.trim()) {
      showStatus("Front and Back content are required.", true);
      return;
    }

    try {
      await axios.post('/api/cards/', {
        subtopic_id: selectedSubtopic,
        front_content: frontContent,
        back_content: backContent,
        tags: tags,
        card_type: cardType
      });
      setFrontContent('');
      setBackContent('');
      setTags('');
      showStatus("Card saved successfully! Ready for the next one.");
    } catch (e) {
      showStatus("Error saving card.", true);
    }
  };

  const handleBulkImport = async (type) => {
    const file = fileInputRef.current?.files[0];
    if (!file) {
      showStatus("Please select a file to import.", true);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);

    showStatus("Uploading and processing... This might take a few seconds.");

    try {
      const res = await axios.post(`/api/import/${type}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      const s = res.data.stats;
      showStatus(`Import success! Cards: ${s.cards_created} created, ${s.cards_skipped} skipped. Errors: ${s.errors}.`);
      fetchTopics();
    } catch (e) {
      showStatus(e.response?.data?.detail || "Import failed.", true);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">

      {status.message && (
        <div className={`alert mb-6 shadow-sm ${status.isError ? 'alert-error' : 'alert-success'}`}>
          {status.message}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* Left Column: Hierarchy Selection */}
        <div className="card bg-base-100 shadow-md">
          <div className="card-body">
            <h2 className="card-title text-xl mb-4 border-b pb-2 border-base-200">1. Select Location</h2>

            <div className="form-control mb-4">
              <label className="label"><span className="label-text font-semibold">Topic</span></label>
              <div className="flex flex-col gap-2">
                <select
                  className="select select-bordered w-full"
                  value={selectedTopic}
                  onChange={(e) => setSelectedTopic(e.target.value)}
                >
                  <option value="">-- Select a Topic --</option>
                  {topics.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
                </select>
                <div className="flex gap-2">
                  <input type="text" value={newTopicName} onChange={(e)=>setNewTopicName(e.target.value)} placeholder="New Topic Name" className="input input-bordered input-sm flex-1" />
                  <button onClick={handleCreateTopic} className="btn btn-sm btn-outline btn-primary">Create</button>
                </div>
              </div>
            </div>

            <div className="form-control mb-4">
              <label className="label"><span className="label-text font-semibold">Subtopic</span></label>
              <div className="flex flex-col gap-2">
                <select
                  className="select select-bordered w-full disabled:opacity-50"
                  value={selectedSubtopic}
                  onChange={(e) => setSelectedSubtopic(e.target.value)}
                  disabled={!selectedTopic}
                >
                  <option value="">-- Select a Subtopic --</option>
                  {subtopics.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                </select>
                <div className="flex gap-2">
                  <input type="text" value={newSubtopicName} onChange={(e)=>setNewSubtopicName(e.target.value)} placeholder="New Subtopic Name" className="input input-bordered input-sm flex-1 disabled:opacity-50" disabled={!selectedTopic} />
                  <button onClick={handleCreateSubtopic} className="btn btn-sm btn-outline btn-primary" disabled={!selectedTopic}>Create</button>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* Right Column: Card Creation */}
        <div className="card bg-base-100 shadow-md border-t-4 border-primary">
          <div className="card-body">
            <h2 className="card-title text-xl mb-4 border-b pb-2 border-base-200">2. Create Card Manually</h2>

            <div className="flex gap-6 mb-4">
              <label className="label cursor-pointer justify-start gap-2">
                <input type="radio" name="card_type" value="basic" checked={cardType === 'basic'} onChange={(e)=>setCardType(e.target.value)} className="radio radio-primary" />
                <span className="label-text font-medium">Basic</span>
              </label>
              <label className="label cursor-pointer justify-start gap-2">
                <input type="radio" name="card_type" value="cloze" checked={cardType === 'cloze'} onChange={(e)=>setCardType(e.target.value)} className="radio radio-primary" />
                <span className="label-text font-medium">Cloze Deletion</span>
              </label>
            </div>

            {cardType === 'cloze' && (
              <div className="alert alert-warning shadow-sm text-sm mb-4">
                <div>
                  <InformationCircleIcon className="flex-shrink-0 w-6 h-6 inline mr-2"/>
                  <span><strong>Tip:</strong> Use syntax <code>{`{{c1::hidden text}}`}</code> on the Front.<br/>
                  Example: <em>The capital of France is {`{{c1::Paris}}`}.</em><br/>
                  Put the answer on the Back.</span>
                </div>
              </div>
            )}

            <div className="form-control mb-4">
              <label className="label"><span className="label-text font-semibold">Front Content</span></label>
              <textarea rows="3" value={frontContent} onChange={(e)=>setFrontContent(e.target.value)} className="textarea textarea-bordered w-full" placeholder="Question or front text..."></textarea>
            </div>

            <div className="form-control mb-4">
              <label className="label"><span className="label-text font-semibold">Back Content</span></label>
              <textarea rows="3" value={backContent} onChange={(e)=>setBackContent(e.target.value)} className="textarea textarea-bordered w-full" placeholder="Answer or back text..."></textarea>
            </div>

            <div className="form-control mb-6">
              <label className="label"><span className="label-text font-semibold">Tags (Comma-separated)</span></label>
              <input type="text" value={tags} onChange={(e)=>setTags(e.target.value)} className="input input-bordered w-full" placeholder="e.g. math, algebra, hard" />
            </div>

            <div className="card-actions justify-end mt-2">
              <button onClick={handleCreateCard} className="btn btn-primary w-full md:w-auto shadow-md">
                Save Flashcard
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Bulk Import Section */}
      <div className="card bg-base-100 shadow-md mt-6">
        <div className="card-body">
          <h2 className="card-title text-xl mb-4 border-b pb-2 border-base-200">3. Bulk Import (CSV / JSON)</h2>
          <p className="text-sm text-base-content/70 mb-4">
            Upload a CSV or JSON file to automatically create Topics, Subtopics, and Cards in bulk.<br/>
            <span className="badge badge-neutral mt-2">Expected Columns/Keys:</span> <code>topic, subtopic, front, back, explanation (optional), tags (optional), card_type (basic/cloze)</code>
          </p>

          <div className="flex flex-col md:flex-row gap-6 items-center bg-base-200 p-6 rounded-lg border border-base-300 border-dashed">
            <div className="flex-1 w-full text-center">
              <input ref={fileInputRef} type="file" accept=".csv, .json" className="file-input file-input-bordered file-input-primary w-full max-w-sm" />
            </div>
            <div className="flex flex-col md:flex-row gap-3 justify-center w-full md:w-auto">
              <button onClick={() => handleBulkImport('csv')} className="btn btn-success text-white shadow">Import CSV</button>
              <button onClick={() => handleBulkImport('json')} className="btn btn-accent text-white shadow">Import JSON</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Studio;
