<template>
    <nav>
        <div class="logo">
            <router-link v-if="isAdmin" to="/admindashboard">BookMyShow</router-link>
        </div>
        <div class="logo">
            <router-link v-if="!isAdmin" to="/">BookMyShow</router-link>
        </div>
        <form @submit.prevent="search" class="form-inline my-2 my-lg-0">
            <input class="form-control mr-sm-2" v-model="data" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-primary my-2 my-sm-0" type="submit">Search</button>
        </form>
        <ul class="nav-links">
            <li>
                <router-link v-if="!isAuthenticated" to="/">Home</router-link>
            </li>
            <li>
                <router-link v-if="isAuthenticated && !isAdmin" to="/">Welcome {{ user['username'] }}</router-link>
            </li>
            <li>
                <router-link v-if="isAuthenticated && isAdmin" to="/admindashboard">Welcome {{ user['username']
                }}</router-link>
            </li>
            <li>
                <router-link v-if="!isAuthenticated" to="/login">Login</router-link>
            </li>
            <li>
                <router-link v-if="!isAuthenticated" to="/register">Register</router-link>
            </li>
            <li>
                <router-link v-if="isAuthenticated" to="/profile">Profile</router-link>
            </li>
            <li>
                <router-link v-if="isAuthenticated" to="/logout" @click="logout">Logout</router-link>
            </li>
        </ul>
    </nav>
</template>
  
<script>
export default {
    name: 'NavBar',
    data() {
        return {
            isAuthenticated: false,
            isAdmin: false,
            user: {},
            data: '',
            shows: [],
            theatres: [],
        };
    },
    created() {
        this.isAuthenticated = localStorage.getItem('token') !== null;
        this.user = JSON.parse(localStorage.getItem('user'));
        if (this.user) {
            this.isAdmin = this.user['role'][0] === 'admin';
        } else {
            this.isAdmin = false;
        }
    },
    methods: {
        search() {
            this.$router.push(`/search/${this.data}`);
        },
        logout() {
            var user = JSON.parse(localStorage.getItem('user'));
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            this.$router.push('/');
            if (user['role'] === 'admin') {
                this.$router.push('/');
            } else {
                this.$router.push('/');
                window.location.reload();
            }
        }
    }
};
</script>

<style scoped>
nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #282c34;
    color: white;
    font-family: 'Montserrat', sans-serif;
    padding: 0.5rem 2rem;
}

form {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

form input:focus {
    outline: none;
    border: none;
    border: 1px solid blue;
    font-family: 'Montserrat', sans-serif;
}

nav .logo {
    font-weight: bold;
    font-size: 1.5rem;
}

a {
    color: white;
    text-decoration: none;
}

.nav-links {
    display: flex;
    justify-content: space-around;
    width: 30%;
}

.nav-links li {
    list-style: none;
}

.nav-links a {
    color: white;
    text-decoration: none;
    letter-spacing: 3px;
    font-weight: bold;
    font-size: 14px;
}
</style>
  