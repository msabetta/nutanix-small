import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

const data = [
  { name: "1", cpu: 30 },
  { name: "2", cpu: 50 },
  { name: "3", cpu: 70 },
  { name: "4", cpu: 60 },
];

export default function Dashboard() {
  return (
    <div className="grid grid-cols-3 gap-6">

      {/* Cards */}
      <div className="bg-gray-900 p-4 rounded-xl border border-gray-800">
        <p className="text-gray-400">CPU Usage</p>
        <h2 className="text-2xl font-bold">65%</h2>
      </div>

      <div className="bg-gray-900 p-4 rounded-xl border border-gray-800">
        <p className="text-gray-400">RAM Usage</p>
        <h2 className="text-2xl font-bold">70%</h2>
      </div>

      <div className="bg-gray-900 p-4 rounded-xl border border-gray-800">
        <p className="text-gray-400">VMs</p>
        <h2 className="text-2xl font-bold">12</h2>
      </div>

      {/* Chart */}
      <div className="col-span-3 bg-gray-900 p-4 rounded-xl border border-gray-800">
        <h2 className="mb-4">CPU Trend</h2>
        <LineChart width={600} height={250} data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="cpu" stroke="#3b82f6" />
        </LineChart>
      </div>

    </div>
  );
}