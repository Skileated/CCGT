import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { EvaluateResponse } from '../api';
import GraphViz from '../components/GraphViz';
import ResultCard from '../components/ResultCard';
import LineGraph from '../components/LineGraph';

export default function Dashboard() {
  const location = useLocation();
  const [result, setResult] = useState<EvaluateResponse | null>(
    location.state?.result || null
  );

  useEffect(() => {
    if (location.state?.result) {
      setResult(location.state.result);
    }
  }, [location.state]);

  if (!result) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-gray-600">No evaluation results available. Go to Home to evaluate text.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Evaluation Dashboard</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <ResultCard result={result} />
        </div>

        {result.graph && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Coherence Graph</h2>
            <GraphViz graph={result.graph} />
          </div>
        )}
      </div>

      {result.graph && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Sentence Contribution Line Graph</h2>
          <LineGraph graph={result.graph} />
        </div>
      )}

      {result.disruption_report && result.disruption_report.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Disruption Report</h2>
          <div className="space-y-3">
            {result.disruption_report.map((disruption, idx) => (
              <div
                key={idx}
                className="p-4 border border-yellow-200 bg-yellow-50 rounded-md"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-900">
                    Sentence {disruption.from_idx + 1} → Sentence {disruption.to_idx + 1}
                  </span>
                  <span className="text-sm text-gray-600">Score: {disruption.score.toFixed(3)}</span>
                </div>
                <p className="text-sm text-gray-700">
                  Reason: {disruption.reason.replace('_', ' ')}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

