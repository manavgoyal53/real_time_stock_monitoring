import React, { Component } from 'react';
import axios from 'axios';
import './AlertsList.css'; // Import the CSS file for styling

class AlertsList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      alerts: [],
      loading: true,
    };
  }

  async componentDidMount() {
    this.fetchAlerts();
  }

  toggleAlert = async (alertId, currentStatus) => {
    try {
      const newStatus = !currentStatus; // Toggle the status
      await axios.put(`http://localhost:5000/api/alerts/${alertId}`, { enabled: newStatus }, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem("token")}` },
      });
      this.fetchAlerts(); // Refresh the alerts list
    } catch (error) {
      console.error('Error updating alert:', error);
    }
  };

  fetchAlerts = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/alerts', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem("token")}` },
      });
      this.setState({ alerts: response.data, loading: false });
    } catch (error) {
      console.error('Error fetching alerts:', error);
      this.setState({ loading: false });
    }
  };

  render() {
    const { alerts, loading } = this.state;

    if (loading) {
      return <p>Loading alerts...</p>;
    }

    return (
      <div className="alerts-list">
        <h2>Alerts List</h2>
        {alerts.length === 0 ? (
          <p>No alerts found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Type</th>
                <th>Price</th>
                <th>Stock Name</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map(alert => (
                <tr key={alert.id}>
                  <td>{alert.type}</td>
                  <td>{alert.price}</td>
                  <td>{alert.stock_symbol}</td>
                  <td>
                    <button onClick={() => this.toggleAlert(alert.id, alert.enabled)}>
                      {alert.enabled ? 'Dsiable' : 'Enable'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    );
  }
}

export default AlertsList;
