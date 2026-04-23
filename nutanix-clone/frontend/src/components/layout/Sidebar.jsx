import { Home, Server, Activity } from "lucide-react";
import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="w-64 bg-gray-900 border-r border-gray-800 p-4">
      <h2 className="text-lg font-bold mb-6">Prism Clone</h2>

      <nav className="space-y-2">
        <Link to="/" className="flex items-center gap-2 p-2 hover:bg-gray-800 rounded">
          <Home size={18}/> Dashboard
        </Link>

        <Link to="/vms" className="flex items-center gap-2 p-2 hover:bg-gray-800 rounded">
          <Server size={18}/> VM
        </Link>

        <Link to="/metrics" className="flex items-center gap-2 p-2 hover:bg-gray-800 rounded">
          <Activity size={18}/> Metrics
        </Link>
      </nav>
    </div>
  );
}