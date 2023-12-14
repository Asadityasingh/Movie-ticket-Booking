<template>
  <form @submit.prevent="login" class="login-container">
    <h2>Login Form</h2>
    <div class="form-group">
      <label for="username">Username</label>
      <input type="text" id="username" v-model="username" placeholder="Enter your username">
    </div>
    <div class="form-group">
      <label for="password">Password</label>
      <input type="password" id="password" v-model="password" placeholder="Enter your password">
    </div>
    <div class="form-group">
      <button type="submit">Login</button>
      <strong>Not a member </strong><router-link to="/register">Regiser</router-link>
    </div>
  </form>
</template>
    
<script>
import { mapActions } from 'vuex';
import axios from 'axios';
import jwtDecode from 'jwt-decode';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    ...mapActions(['login']),
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/login', {
          username: this.username,
          password: this.password,
        });
        const token = response.data.access_token;
        console.log('Token:', token);
        const decodeToken = jwtDecode(token);
        const user_resoponse = await axios.get(`http://localhost:5000/users/${decodeToken.sub}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user_resoponse.data));
        if (user_resoponse.data.role[0] === 'admin') {
          this.$router.push('/admindashboard');
        } else {
          this.$router.push('/');
        }

      } catch (error) {
        console.error('Login error:', error);
      }
    },
  },
};
</script>
  
<style>
.login-container {
  background-color: #fff;
  padding: 20px;
  margin: auto;
  margin-top: 50px;
  border-radius: 5px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
  width: 300px;
}

.login-container h2 {
  margin: 0;
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.form-group button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.form-group button:hover {
  background-color: #0056b3;
}
</style>