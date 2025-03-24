import React, { useEffect, useState } from 'react';
import { fetchPipelineStatus, fetchPipelineLogs } from '../services/api';
import { onMessage } from '../utils/websocket';
import { Line, Bar, Pie } from 'react-chartjs-2';
import 'chart.js/auto';

const Dashboard = () => {
  const [status, setStatus] = useState([]);
  const [logs, setLogs] = useState([]);
  const [data, setData] = useState([]);
  const [rawData, setRawData] = useState([]);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const loadPipelineStatus = async () => {
      try {
        const statusData = await fetchPipelineStatus();
        setStatus(statusData);
      } catch (error) {
        console.error('Failed to load pipeline status', error);
      }
    };

    const loadPipelineLogs = async () => {
      try {
        const logsData = await fetchPipelineLogs();
        setLogs(logsData);
      } catch (error) {
        console.error('Failed to load pipeline logs', error);
      }
    };

    loadPipelineStatus();
    loadPipelineLogs();

    onMessage((message) => {
      setStatus((prevStatus) => [...prevStatus, message]);
    });
  }, []);

  useEffect(() => {
    // Fetch transformed data from API endpoint
    fetch('/api/transformed-data')
      .then(response => response.json())
      .then(data => setData(data));

    // Fetch raw data from API endpoint
    fetch('/api/raw-data')
      .then(response => response.json())
      .then(rawData => setRawData(rawData));
  }, []);

  const lineChartData = {
    labels: data.map(d => d.timestamp),
    datasets: [
      {
        label: 'Transformed Data',
        data: data.map(d => d.value),
        fill: false,
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  const barChartData = {
    labels: data.map(d => d.timestamp),
    datasets: [
      {
        label: 'Transformed Data',
        data: data.map(d => d.value),
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  const pieChartData = {
    labels: data.map(d => d.timestamp),
    datasets: [
      {
        label: 'Transformed Data',
        data: data.map(d => d.value),
        backgroundColor: data.map((_, idx) => `hsl(${idx * 30}, 70%, 50%)`),
        borderColor: data.map((_, idx) => `hsl(${idx * 30}, 70%, 30%)`),
      },
    ],
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <div className={`container mx-auto p-4 ${darkMode ? 'dark' : ''}`}>
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold mb-4">ETL Pipeline Dashboard</h1>
        <button
          onClick={toggleDarkMode}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 transition"
        >
          Toggle Dark Mode
        </button>
      </div>
      <div className="mb-4">
        <h2 className="text-xl font-semibold">Pipeline Status</h2>
        <ul className="list-disc pl-5">
          {status.map((s, idx) => (
            <li key={idx} className="hover:underline" title={s}>{s}</li>
          ))}
        </ul>
      </div>
      <div className="mb-4">
        <h2 className="text-xl font-semibold">Pipeline Logs</h2>
        <pre className="bg-gray-100 p-2 rounded dark:bg-gray-800 dark:text-white">{logs.join('\n')}</pre>
      </div>
      <div className="mb-4">
        <h2 className="text-xl font-semibold">Transformed Data (Line Chart)</h2>
        <Line data={lineChartData} />
      </div>
      <div className="mb-4">
        <h2 className="text-xl font-semibold">Transformed Data (Bar Chart)</h2>
        <Bar data={barChartData} />
      </div>
      <div className="mb-4">
        <h2 className="text-xl font-semibold">Transformed Data (Pie Chart)</h2>
        <Pie data={pieChartData} />
      </div>
      <div className="mb-4">
        <h2 className="text-xl font-semibold">Raw Data</h2>
        <table className="min-w-full bg-white dark:bg-gray-900 dark:text-white">
          <thead>
            <tr>
              <th className="py-2">Timestamp</th>
              <th className="py-2">Value</th>
            </tr>
          </thead>
          <tbody>
            {rawData.map((row, idx) => (
              <tr key={idx} className="hover:bg-gray-100 dark:hover:bg-gray-700">
                <td className="border px-4 py-2">{row.timestamp}</td>
                <td className="border px-4 py-2">{row.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;