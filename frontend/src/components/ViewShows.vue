<template>
    <div>
        <NavBar />
        <div class="show-grid">
            <div v-for="show in shows" :key="show.id" class="card" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">{{ show.name }}</h5>
                    <h6 class="card-subtitle mb-2 text-body-secondary">Start Time: {{ show.start_time }}</h6>
                    <h6 class="card-subtitle mb-2 text-body-secondary">End Time: {{ show.end_time }}</h6>
                    <h6 class="card-subtitle mb-2 text-body-secondary">Ticket Price: {{ show.ticket_price }}</h6>
                    <h6 class="card-subtitle mb-2 text-body-secondary">Rating: {{ show.rating }}</h6>
                </div>
                <div v-if="isAdmin" class="card-goot">
                    <router-link :to="'/eidtshow/' + show.id" class="btn btn-primary btn-sm me-2">Edit Show</router-link>
                    <button @click="deleteShow(show.id)" class="btn btn-danger btn-sm">Delete</button>
                </div>
                <form v-if="!isAdmin" class="bookshowbtn" @submit.prevent="bookShow(show.id)">
                    <input v-model.number="seats" class="inputSeats" placeholder="No of seats" type="number" />
                    <button class="btn btn-primary" type="submit">Book Show</button>
                </form>
            </div>
        </div>
    </div>
</template>


<script>
import NavBar from "@/components/NavBar.vue";
import axios from "axios";
import jwtDecode from "jwt-decode";

export default {
    name: "ViewShows",
    components: {
        NavBar,
    },
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
    mounted() {
        this.fetchShows();
    },
    methods: {
        async fetchShows() {
            // const theatreId = this.$route.params.id;
            try {
                const response = await axios.get("http://localhost:5000/shows");
                console.log(response.data);
                for (let i = 0; i < response.data.length; i++) {
                    for (let j = 0; j < response.data[i].theatres.length; j++) {
                        if (response.data[i].theatres[j].id == this.$route.params.id) {
                            this.shows.push(response.data[i])
                        }
                    }
                }
                console.log(this.shows)
            } catch (error) {
                console.error("Er;ror fetching shows:", error);
            }
        },
        async deleteShow(id) {
            try {
                const response = await axios.delete(`http://localhost:5000/shows/${id}`);
                console.log(response.data);
                this.shows = this.shows.filter((show) => show.id !== id);
            } catch (error) {
                console.error("Error deleting show:", error);
            }
        },
        bookShow(id) {
            const user_id = jwtDecode(localStorage.getItem('token')).sub;
            if (user_id === undefined){
                this.$router.push('/login');
                return
            }
            let seats = this.seats;
            axios.post("http://localhost:5000/bookings", {
                show_id: id,
                user_id: user_id,
                seats: seats,
            }).then((response) => {
                console.log(response.data);
                // this.$router.push('/bookings');
                alert('Booking Successful')
            }).catch((error) => {
                console.error("Error booking show:", error);
            });
        },
    },
};
</script>

<style scoped>
.bookshowbtn {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
}
.show-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 20px;
    padding: 20px;
}

.card {
    border: none;
    width: fit-content;
    border-radius: 5px;
    padding: 10px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}
</style>
