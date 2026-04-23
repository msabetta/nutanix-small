import { useEffect, useState } from "react";
import { getVMs } from "../api";

export default function VMTable({ vms }) {
  return (
    <div className="bg-gray-900 rounded-xl border border-gray-800">
      <table className="w-full text-left">
        <thead className="border-b border-gray-800">
          <tr>
            <th className="p-3">Name</th>
            <th>Status</th>
            <th>CPU</th>
            <th>RAM</th>
          </tr>
        </thead>
        <tbody>
          {vms.map(vm => (
            <tr key={vm.id} className="border-b border-gray-800 hover:bg-gray-800">
              <td className="p-3">{vm.name}</td>
              <td>{vm.status}</td>
              <td>{vm.cpu}</td>
              <td>{vm.ram}GB</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}