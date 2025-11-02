import { EvaluateResponse } from '../api';

interface ResultCardProps {
  result: EvaluateResponse;
}

export default function ResultCard({ result }: ResultCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 0.7) return 'text-green-600 bg-green-50';
    if (score >= 0.5) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 0.8) return 'Highly Coherent';
    if (score >= 0.6) return 'Moderately Coherent';
    if (score >= 0.4) return 'Somewhat Coherent';
    return 'Low Coherence';
  };

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Coherence Score</h2>
      <div className={`rounded-lg p-6 ${getScoreColor(result.coherence_score)}`}>
        <div className="text-4xl font-bold mb-2">
          {(result.coherence_score * 100).toFixed(1)}%
        </div>
        <div className="text-lg font-medium mb-4">
          {getScoreLabel(result.coherence_score)}
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className={`h-3 rounded-full ${
              result.coherence_score >= 0.7
                ? 'bg-green-500'
                : result.coherence_score >= 0.5
                ? 'bg-yellow-500'
                : 'bg-red-500'
            }`}
            style={{ width: `${result.coherence_percent}%` }}
          />
        </div>
      </div>
      <div className="mt-4 text-sm text-gray-600">
        Raw score: {result.coherence_score.toFixed(4)}
      </div>
    </div>
  );
}

