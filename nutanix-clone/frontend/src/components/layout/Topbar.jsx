export default function Topbar() {
  return (
    <div className="h-14 border-b border-gray-800 flex items-center justify-between px-6">
      <h1 className="text-lg font-semibold">Cluster Dashboard</h1>

      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-400">Admin</span>
        <div className="w-8 h-8 bg-blue-500 rounded-full"></div>
      </div>
    </div>
  );
}