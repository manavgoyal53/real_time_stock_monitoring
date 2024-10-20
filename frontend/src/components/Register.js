import React from 'react';
import { register } from '../services/authService';
import './Register.css'; // Import CSS for styling

class Register extends React.Component {
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
    const res = await register({ email, password });
    if (res){
      window.location = "/"
    }
      
  };

  render() {
    return (
      <div className="register-container">
        <h2 className="register-title">Register</h2>
        <form onSubmit={this.handleSubmit} className="register-form">
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={this.state.email}
            onChange={this.handleChange}
            required
            className="register-input"
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={this.state.password}
            onChange={this.handleChange}
            required
            className="register-input"
          />
          <button type="submit" className="register-button">Register</button>
        </form>
      </div>
    );
  }
}

export default Register;
