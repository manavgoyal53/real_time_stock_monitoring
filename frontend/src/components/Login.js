import React from "react";
import { login } from '../services/authService';
import './Login.css'; // Import CSS for styling

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      password: "",
    };
  }

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  handleSubmit = async (e) => {
    e.preventDefault();
    const { email, password } = this.state;
    const res = await login({ email, password });
    if(res){
      window.location = "/"
    }
  };

  render() {
    return (
      <div className="login-container">
        <h2 className="login-title">Login</h2>
        <form onSubmit={this.handleSubmit} className="login-form">
          <input
            type="text"
            name="email"
            placeholder="Email"
            value={this.state.email}
            onChange={this.handleChange}
            required
            className="login-input"
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={this.state.password}
            onChange={this.handleChange}
            required
            className="login-input"
          />
          <button type="submit" className="login-button">Login</button>
        </form>
      </div>
    );
  }
}

export default Login;
