import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface DataPoint {
  frequency: number;
  magnitude: number;
}

// Generate some dummy data for visualization
const data: DataPoint[] = Array.from({ length: 50 }, (_, i) => ({
  frequency: i,
  magnitude: Math.abs(Math.sin(i * 0.2) * 50 + Math.random() * 10),
}));

export default function FFTChart() {
  const dominantPeak = data.reduce((prev, current) =>
    (prev.magnitude > current.magnitude) ? prev : current
  );

  return (
    <div className="w-full h-80 bg-white p-4 rounded-lg shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-gray-800">Frequency Spectrum</h2>
        <div className="text-sm font-medium text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
          Dominant Frequency: <span className="text-indigo-600">{dominantPeak.frequency.toFixed(1)} Hz</span>
        </div>
      </div>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="frequency" stroke="#9ca3af" />
          <YAxis stroke="#9ca3af" />
          <Tooltip />
          <Line type="monotone" dataKey="magnitude" stroke="#4f46e5" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
