/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import FFTChart from './components/FFTChart';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">FFT Analysis Dashboard</h1>
        <FFTChart />
      </div>
    </div>
  );
}
