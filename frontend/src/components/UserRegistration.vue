<template>
  <div>
    <form @submit.prevent="registerUser" class="register-container">
      <h2>Sign Up Form</h2>
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" placeholder="Enter your username">
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" placeholder="Enter your email">
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" placeholder="Enter your password">
      </div>
      <div class="form-group">
        <button type="submit">Sign Up</button>
        <strong>Already a member </strong><router-link to="/login">Login</router-link>
      </div>
    </form>
  </div>
</template>
  
<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post("http://localhost:5000/users", {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        console.log(response.data.message);
        this.$router.push("/login");
      } catch (error) {
        console.error("Error registering user:", error);
      }
    },
  },
};
</script>
  
<style>

    .register-container {
        background-color: #fff;
        margin: auto;
        margin-top: 50px;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
        width: 300px;
    }

    .register-container h2 {
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