import React, { Component } from 'react';
import io from 'socket.io-client';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import 'chartjs-adapter-moment';
import './LiveStockChart.css';
import { toast } from 'react-toastify';


const withRouter = WrappedComponent => props => {
  const params = useParams();
  return (
    <WrappedComponent
      {...props}
      params={params}
    />
  );
};

class LiveStockChart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stockData: [],
      timestamps: [],
      showModal: false, 
      alertType: 'above',
      alertPrice: '',
      socket : io('http://localhost:5000/',{autoConnect:false})
    };
  }

  async componentDidMount() {
    const { symbol } = this.props.params; // Get the stock symbol from the URL params

    const response = await axios.get(`http://localhost:5000/api/stock/${symbol}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem("token")}` },
    });

    const stock_history = response.data.price_history;
    const market_open = response.data.market_open;


    this.setState((prevState) => ({
      stockData: [...prevState.stockData, ...Object.values(stock_history)],
      timestamps: [...prevState.timestamps, ...Object.keys(stock_history)],
    }));

    // Only connect and subscribe if market is open
    if (market_open) {
      this.state.socket.connect();
      // Listen for stock data updates
      this.state.socket.on('stock_update', (data) => {
        const { price, timestamp } = data;

        // Append new data to the arrays
        this.setState((prevState) => ({
          stockData: [...prevState.stockData, price],
          timestamps: [...prevState.timestamps, timestamp],
        }));
      });

      // Subscribe to stock symbol when component mounts
      this.state.socket.emit('subscribe_to_stock', { stock_symbol: symbol, start_timestamp: this.state.timestamps.at(-1) });
    }
  }

  componentWillUnmount() {
      this.state.socket.off('stock_update');
      this.state.socket.disconnect();
  }

  toggleModal = () => {
    this.setState({ showModal: !this.state.showModal });
  }

  handleAlertSubmit = async (e) => {
    e.preventDefault();
    const { alertType, alertPrice } = this.state;
    const data = {
      "stock_symbol":this.props.params.symbol,
      "alert_type":alertType,
      "price_threshold":alertPrice,

    }
    const response = await axios.post('http://localhost:5000/api/alerts',data ,{
      headers: { 'Authorization': `Bearer ${localStorage.getItem("token")}` },
    }).then((res)=>{
      toast.success("Alert created successfully",{"position":"top-right"})
    })


    this.toggleModal(); 
  }

  render() {
    const { symbol } = this.props.params; // Get the stock symbol from the URL params
    const { stockData, timestamps, showModal, alertType, alertPrice } = this.state;

    // Data and options for the Chart.js line chart
    const chartData = {
      labels: timestamps,  // Timestamps for the X-axis
      datasets: [
        {
          label: `Stock Price (${symbol})`,
          data: stockData,  // Stock prices for the Y-axis
          borderColor: 'rgba(75,192,192,1)',
          backgroundColor: 'rgba(75,192,192,0.2)',
          fill: true,
          tension: 0.1,
        },
      ],
    };

    const chartOptions = {
      responsive: true,
      scales: {
        x: {
          type: 'time',  // Time-based X-axis
          time: {
            unit: 'minute', 
          },
        },
        y: {
          beginAtZero: false,
        },
      },
    };

    return (
      <div>
        <div className="chart-container">
          <h2 className="chart-header">Live Stock Chart: {symbol}</h2>

          <button onClick={this.toggleModal} className="alert-button">
            Create Alert
          </button>

          <div className="chart-wrapper">
            <Line data={chartData} options={chartOptions} />
          </div>

          {showModal && (
            <div className="modal">
              <div className="modal-content">
                <h3>Create Alert</h3>
                <form onSubmit={this.handleAlertSubmit}>
                  <label>
                    Alert Type:
                    <select
                      value={alertType}
                      onChange={(e) => this.setState({ alertType: e.target.value })}
                    >
                      <option value="above">Above</option>
                      <option value="below">Below</option>
                    </select>
                  </label>
                  <br />
                  <label>
                    Price:
                    <input
                      type="number"
                      value={alertPrice}
                      onChange={(e) => this.setState({ alertPrice: e.target.value })}
                      required
                    />
                  </label>
                  <br />
                  <button type="submit" className="save-button">Save Alert</button>
                  <button type="button" onClick={this.toggleModal} className="cancel-button">
                    Cancel
                  </button>
                </form>
              </div>
            </div>
          )}
        </div>
      </div>
      
    );
  }
}

export default withRouter(LiveStockChart);
