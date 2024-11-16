import React, { useState, useRef } from "react";
import "./App.css"; // Assuming you use an external CSS file for styles

const App = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [expandedRows, setExpandedRows] = useState({});
  const [sortConfig, setSortConfig] = useState({
    key: null, // key will be 'cvss_score' or 'publish_date'
    direction: "asc", // 'asc' for ascending, 'desc' for descending
  });

  // Refs to dynamically measure content height
  const descriptionRefs = useRef({});

  const fetchVulnerabilities = async () => {
    setLoading(true);
    setResults([]); // Clear previous results
    try {
      const response = await fetch(
        `http://192.168.0.108:5000/api/cves?query=${query}`
      );
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const toggleExpandRow = (index) => {
    setExpandedRows((prev) => ({
      ...prev,
      [index]: !prev[index], // Toggle the expanded state of the row
    }));
  };

  // Set up dynamic height for collapsed/expanded states
  const getHeight = (index) => {
    const element = descriptionRefs.current[index];
    return element ? element.scrollHeight : 0; // Dynamically get content height
  };

  const handleSort = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc"; // Toggle the sorting direction if already sorted by the same key
    }
    setSortConfig({ key, direction });
  };

  const sortedResults = React.useMemo(() => {
    const sortedData = [...results];
    if (sortConfig.key) {
      sortedData.sort((a, b) => {
        if (sortConfig.key === "cvss_score") {
          // Sort CVSS Score numerically
          return sortConfig.direction === "asc"
            ? a.cvss_score - b.cvss_score
            : b.cvss_score - a.cvss_score;
        } else if (sortConfig.key === "publish_date") {
          // Sort Publish Date chronologically
          return sortConfig.direction === "asc"
            ? new Date(a.publish_date) - new Date(b.publish_date)
            : new Date(b.publish_date) - new Date(a.publish_date);
        }
        return 0;
      });
    }
    return sortedData;
  }, [results, sortConfig]);

  return (
    <div className="app-container">
      <h1 className="app-title">Vulnerability Search</h1>
      <div className="search-container">
        <input
          type="text"
          className="search-input"
          placeholder="Enter query (e.g., 'mysql')"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          className="search-button"
          onClick={fetchVulnerabilities}
          disabled={loading}
        >
          {loading ? "Loading..." : "Search"}
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <div className="table-container">
          <table className="results-table">
            <thead>
              <tr>
                <th onClick={() => handleSort("cve_id")} className="sortable">
                  CVE ID
                </th>
                <th
                  onClick={() => handleSort("cvss_score")}
                  className="sortable"
                >
                  CVSS Score
                </th>
                <th>Description</th>
                <th
                  onClick={() => handleSort("publish_date")}
                  className="sortable"
                >
                  Publish Date
                </th>
              </tr>
            </thead>
            <tbody>
              {sortedResults.length > 0 ? (
                sortedResults.map((result, index) => (
                  <tr
                    key={index}
                    className={`result-row ${
                      result.cvss_score >= 7
                        ? "high-severity"
                        : result.cvss_score >= 4
                        ? "medium-severity"
                        : "low-severity"
                    }`}
                  >
                    <td className="cve-id">{result.cve_id}</td>
                    <td>{result.cvss_score}</td>
                    <td>
                      <div className="description-container">
                        <div
                          ref={(el) => (descriptionRefs.current[index] = el)}
                          className={`description-text ${
                            expandedRows[index] ? "expanded" : "collapsed"
                          }`}
                          style={{
                            height: expandedRows[index]
                              ? getHeight(index)
                              : "100px", // Height of collapsed text (can be adjusted)
                            transition: "height 0.5s ease-in-out",
                            overflow: "hidden", // Ensure hidden content doesn't overflow
                          }}
                        >
                          {result.description}
                        </div>
                        <button
                          className="expand-button"
                          onClick={() => toggleExpandRow(index)}
                        >
                          {expandedRows[index] ? "Read Less" : "Read More"}
                        </button>
                      </div>
                    </td>
                    <td>{result.publish_date}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="no-results">
                    No results found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default App;
