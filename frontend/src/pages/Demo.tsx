import { useState } from 'react';
import { evaluateText, EvaluateResponse } from '../api';
import GraphViz from '../components/GraphViz';
import ResultCard from '../components/ResultCard';
import Footer from '../components/Footer';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function DemoPage() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<EvaluateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

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
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to evaluate text');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Live Demo</h1>
      <div className="bg-white rounded-2xl shadow-lg p-6 mb-6 max-w-3xl mx-auto">
        <label className="block text-sm font-medium text-gray-700 mb-2">Enter your text</label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full h-40 border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          placeholder="Paste a paragraph to analyze coherence..."
        />
        <div className="mt-2 text-sm text-gray-500">{text.split(/\s+/).filter(Boolean).length} words</div>
        <button
          onClick={handleEvaluate}
          disabled={loading || !text.trim()}
          className="mt-4 px-6 py-3 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {loading ? 'Evaluating...' : 'Evaluate Coherence'}
        </button>
        {error && <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded text-red-700">{error}</div>}
      </div>

      {result && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <ResultCard result={result} />
            </div>
            {result.graph && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Coherence Graph</h2>
                <GraphViz graph={result.graph} />
              </div>
            )}
          </div>

          {/* Sentence-level scores */}
          {result.graph && result.graph.nodes && (
            <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Sentence-Level Coherence Scores</h2>
              <div className="overflow-x-auto mb-6">
                <table className="w-full text-sm text-left text-gray-600">
                  <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                    <tr>
                      <th className="px-4 py-3">Sentence</th>
                      <th className="px-4 py-3">Text Snippet</th>
                      <th className="px-4 py-3">Importance Score</th>
                      <th className="px-4 py-3">Entropy</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.graph.nodes.map((node, idx) => (
                      <tr key={node.id} className="border-b hover:bg-gray-50">
                        <td className="px-4 py-3 font-medium text-gray-800">{idx + 1}</td>
                        <td className="px-4 py-3 max-w-md truncate">{node.text_snippet || `Sentence ${idx + 1}`}</td>
                        <td className="px-4 py-3">{(node.importance_score ?? 0).toFixed(3)}</td>
                        <td className="px-4 py-3">{(node.entropy ?? 0).toFixed(3)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Line Graph */}
              <div className="mt-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Coherence Score Trend</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart
                    data={result.graph.nodes.map((node, idx) => ({
                      sentence: idx + 1,
                      score: node.importance_score ?? (1 - (node.entropy ?? 0)),
                    }))}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="sentence" label={{ value: 'Sentence', position: 'insideBottom', offset: -5 }} />
                    <YAxis domain={[0, 1]} tickFormatter={(v) => v.toFixed(2)} />
                    <Tooltip formatter={(value: any) => value.toFixed(3)} labelFormatter={(label) => `Sentence ${label}`} />
                    <Line type="monotone" dataKey="score" stroke="#6366F1" strokeWidth={3} dot={{ r: 4 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </>
      )}

      <Footer />
    </div>
  );
}


