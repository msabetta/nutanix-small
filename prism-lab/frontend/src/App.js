import { useEffect, useState } from "react";
import "./styles.css";

export default function App() {
  const [vms, setVms] = useState([]);
  const [summary, setSummary] = useState({});

  useEffect(() => {
    fetch("/api/v1/vms")
      .then(r => r.json())
      .then(d => setVms(d.vms));

    fetch("/api/v1/summary")
      .then(r => r.json())
      .then(d => setSummary(d));
  }, []);

  return (
    <div className="layout">

      {/* SIDEBAR */}
      <div className="sidebar">
        <h2>PRISM LAB</h2>
        <nav>
          <p>Dashboard</p>
          <p>VMs</p>
          <p>Clusters</p>
          <p>Alerts</p>
        </nav>
      </div>

      {/* MAIN */}
      <div className="main">

        <h1>Infrastructure Overview</h1>

        {/* CARDS */}
        <div className="cards">
          <div className="card">
            <h3>Total VM</h3>
            <p>{summary.total}</p>
          </div>

          <div className="card">
            <h3>Running</h3>
            <p>{vms.filter(v => v.status === "running").length}</p>
          </div>

          <div className="card">
            <h3>Stopped</h3>
            <p>{vms.filter(v => v.status === "stopped").length}</p>
          </div>
        </div>

        {/* TABLE */}
        <div className="table">
          <h2>Virtual Machines</h2>

          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {vms.map((vm, i) => (
                <li key={i}>
                {vm.name} -
                <span style={{ color: vm.status === "running" ? "green" : "red" }}>
                    {vm.status}
                </span>
                </li>
              ))}
            </tbody>

          </table>
        </div>

      </div>
    </div>
  );
}