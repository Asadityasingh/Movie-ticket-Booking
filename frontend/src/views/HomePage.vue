<template>
    <NavBar />
    <div class="container">
        <div v-for="theatre in theatres" :key="theatre.id">
            <h3>{{ theatre.name }}</h3>
            <div class="show-container">
                <div v-for="show in filteredShows(theatre.id)" :key="show.id" class="card">
                    <h4>{{ show.name }}</h4>
                    <p>Rating: {{ show.rating }}</p>
                    <p>Ticket Price: {{ show.ticket_price }}</p>
                    <p>Start Time: {{ show.start_time }}</p>
                    <p>End Time: {{ show.end_time }}</p>
                    <div class="btns">
                        <form v-if="isAuthenticated" class="bookshowbtn" @submit.prevent="bookShow(show.id)">
                            <input v-model.number="seats" class="inputSeats" placeholder="No of seats" type="number" />
                            <button class="btn btn-primary" type="submit">Book Show</button>
                        </form>
                        <router-link v-if="!isAuthenticated" class="bookshowbtn btn btn-primary" to="/login">Login to Book</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import axios from "axios";
import jwtDecode from "jwt-decode";

export default {
    name: "HomePage",
    components: {
        NavBar,
    },
    data() {
        return {
            theatres: [],
            shows: [],
            isAuthenticated: false,
        };
    },
    created() {
        this.isAuthenticated = localStorage.getItem('token') !== null;
    },
    computed: {
        filteredShows() {
            return (theatreId) => {
                let res = []
                for (let i = 0; i < this.shows.length; i++) {
                    for (let j = 0; j < this.shows[i].theatres.length; j++) {
                        if (this.shows[i].theatres[j].id == theatreId) {
                            res.push(this.shows[i])
                        }
                    }
                }
                return res
            };
        },
    },
    mounted() {
        this.fetchTheatres();
        this.fetchShows();
    },
    methods: {
        async fetchTheatres() {
            try {
                const response = await axios.get("http://localhost:5000/theatres");
                this.theatres = response.data;
            } catch (error) {
                console.error("Error fetching theatres:", error);
            }
        },
        async fetchShows() {
            try {
                const response = await axios.get("http://localhost:5000/shows");
                this.shows = response.data;
            } catch (error) {
                console.error("Error fetching shows:", error);
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
.show-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-evenly;
    align-items: center;
    gap: 10px;
}

.inputSeats {
    width: 90px;
}

.card {
    margin: 10px;
    width: 25%;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    padding: 10px;
    border: none;
}

.bookshowbtn{
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
}
</style>
