import { useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { GraphData } from '../api';

interface LineGraphProps {
  graph: GraphData;
}

export default function LineGraph({ graph }: LineGraphProps) {
  const data = useMemo(() => {
    return (graph.nodes || []).map((n, idx) => {
      const contribution = typeof n.importance_score === 'number' ? n.importance_score : (1 - (n.entropy ?? 0));
      const clamped = Math.max(0, Math.min(1, contribution));
      return { idx: idx + 1, contribution: clamped };
    });
  }, [graph]);

  return (
    <div className="w-full" style={{ height: 300 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="idx" label={{ value: 'Sentence', position: 'insideBottom', offset: -5 }} />
          <YAxis domain={[0, 1]} tickFormatter={(v) => `${Math.round(v * 100)}%`} />
          <Tooltip formatter={(v: any) => [`${(v as number).toFixed(3)}`, 'Contribution']} labelFormatter={(l: any) => `Sentence ${l}`} />
          <Line
            type="monotone"
            dataKey="contribution"
            stroke="#10b981"
            strokeWidth={2.5}
            dot={false}
            isAnimationActive
            animationDuration={800}
            strokeDasharray="2000 0"
          />
        </LineChart>
      </ResponsiveContainer>
      <div className="mt-2 text-sm text-gray-600">Higher values indicate stronger positive contribution to coherence.</div>
    </div>
  );
}


