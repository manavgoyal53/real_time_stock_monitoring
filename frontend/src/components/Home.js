import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Home.css'; // Import the CSS file
import NavBar from './NavBar';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stocks: [],
      loading: true,
    };
  }

  async componentDidMount() {
    const fetchStockData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/', {
          headers: { 'Authorization': `Bearer ${localStorage.getItem("token")}` },
        });
        console.log(response);

        this.setState({
          stocks: response.data.nifty50_tickers,
          loading: false,
        });
      } catch (error) {
        console.error('Error fetching stock data:', error);
        this.setState({ loading: false });
      }
    };

    await fetchStockData();
  }

  render() {
    const { stocks, loading } = this.state;

    if (loading) {
      return <p className="loading-message">Loading stock data...</p>;
    }

    return (
      <div className="home-container">
        <h2 className="home-title">Nifty 50 Trading Stocks</h2>
        <div>
          <ul className="stock-list">
            {stocks.map((stock) => (
              <li key={stock}>
                <Link to={`/live-stock/${stock}`} className="stock-link">{stock} -- View Details</Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }
}

export default Home;
