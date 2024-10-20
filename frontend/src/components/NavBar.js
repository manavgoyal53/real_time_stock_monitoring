// components/NavBar.js
import React, { Component } from 'react';
import './NavBar.css';
import { logout } from '../services/authService';

class NavBar extends Component {

    constructor(props) {
        super(props);
    }
    handleViewAlerts = () => {
        window.location = "/alerts"
    };

    handleViewHome = () => {
      window.location = "/"
    };

    handleLogout = async () => {
      await logout();
      window.location = '/' // Redirect to login
    };

    render() {
      return (
        <nav className="nav-bar">
          <div className="nav-left">
              <h3 onClick={this.handleViewHome}>Stock Monitoring</h3>
          </div>
          {this.props.isAuthenticated && (
              <div className="nav-right">
              <button className="view-alerts-button" onClick={this.handleViewAlerts}>
                  View Alerts
              </button>
              <button className="logout-button" onClick={this.handleLogout}>
                  Log Out
              </button>
          </div>
          )}
          
        </nav>
      );
    }
}

export default NavBar;
