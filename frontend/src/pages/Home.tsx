import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { evaluateText, EvaluateResponse } from '../api';
import ResultCard from '../components/ResultCard';

export default function Home() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<EvaluateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleEvaluate = async () => {
    if (!text.trim()) {
      setError('Please enter some text to evaluate');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await evaluateText(text, true);
      setResult(response);
      // Navigate to dashboard with result
      navigate('/dashboard', { state: { result: response, text } });
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to evaluate text');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Contextual Coherence Graph Transformer
        </h1>
        <p className="text-gray-600 mb-6">
          Evaluate the coherence of your text by analyzing semantic relationships
          and discourse flow between sentences.
        </p>

        <div className="mb-6">
          <label htmlFor="text-input" className="block text-sm font-medium text-gray-700 mb-2">
            Enter your text paragraph
          </label>
          <textarea
            id="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste or type your paragraph here... For example: 'This is a sample paragraph. It contains multiple sentences. Each sentence should flow coherently to the next.'"
            className="w-full h-48 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={loading}
          />
          <p className="mt-2 text-sm text-gray-500">
            {text.length} characters, {text.split(/\s+/).filter(w => w).length} words
          </p>
        </div>

        <button
          onClick={handleEvaluate}
          disabled={loading || !text.trim()}
          className="w-full bg-primary-600 text-white py-3 px-6 rounded-md font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Evaluating...' : 'Evaluate Coherence'}
        </button>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {result && !error && (
          <div className="mt-6">
            <ResultCard result={result} />
          </div>
        )}
      </div>
    </div>
  );
}

