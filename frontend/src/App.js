import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import LiveStockChart from './components/LiveStockChart';
import { getCurrentUser } from './services/authService';
import Home from './components/Home';
import "./App.css"
import NavBar from './components/NavBar';
import AlertsList from './components/AlertsList';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isAuthenticated: !!getCurrentUser(),
    };
  }

  setAuth = (isAuthenticated) => {
    this.setState({ isAuthenticated });
  };

  handleLogout = () => {
    localStorage.removeItem('token');
    window.location = '/' // Redirect to login
  };

  render() {
    const { isAuthenticated } = this.state;

    return (
      <Router>
        <NavBar onLogout={this.handleLogout} isAuthenticated={this.state.isAuthenticated}/>
        <div className="app-container">
          {/* Show Login by default */}
          <Routes>
            {/* Public Routes */}
            <Route
              path="/login"
              element={
                <>
                  <Login setAuth={this.setAuth} />
                  <p className="signup-text">
                    Don't have an account? <Link to="/register">Sign up.</Link>
                  </p>
                </>
              }
            />
            <Route path="/register" element={
                <>
                  <Register />
                  <p className="signup-text">
                    Already Signed Up? <Link to="/login">Log In.</Link>
                  </p>
                </>
              }
            />

            {/* Protected Routes */}
            {isAuthenticated && (
              <>
                <Route path="/" element={<Home />} />
                <Route path="/live-stock/:symbol" element={<LiveStockChart />} />
                <Route path="/alerts" element={<AlertsList />} /> {/* New route for alerts */}
              </>
            )}
            {/* Redirect to login if the user is not authenticated */}
            <Route
              path="/"
              element={
                <>
                  <Login setAuth={this.setAuth} />
                  <p className="signup-text">
                    Don't have an account? <Link to="/register">Sign up.</Link>
                  </p>
                </>
              }
            />
          </Routes>
        </div>
      </Router>
    );
  }
}

export default App;
