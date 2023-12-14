<template>
    <NavBar />
    <div class="searchResult">
        <div v-if="shows.length">
            <h2>Shows</h2>
            <div v-for="show in shows" :key="show.id" class="card" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">{{ show.name }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">Price: ${{ show.ticket_price }}</h6>
                    <p class="card-text">Rating: {{ show.rating }}</p>
                    <p class="card-text">Start Time: {{ show.start_time }}</p>
                    <p class="card-text">End Time: {{ show.end_time }}</p>
                    <form class="bookshowbtn" @submit.prevent="bookShow(show.id)">
                        <input v-model.number="seats" class="inputSeats" placeholder="No of seats" type="number" />
                        <button class="btn btn-primary" type="submit">Book Show</button>
                    </form>
                </div>
            </div>
        </div>

        <div v-if="theatres.length">
            <h2>Theatres</h2>
            <ul>
                <li v-for="theatre in theatres" :key="theatre.id">{{ theatre.name }}</li>
            </ul>
            <div v-for="theatre in theatres" :key="theatre.id" class="card" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">{{ theatre.name }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">Theatre Location: {{ theatre.location }}</h6>
                    <p class="card-text">Theatre Capacity: {{ theatre.capacity }}</p>
                    <router-link :to="'/viewshow/'+theatre.id" class="btn btn-secondary btn-sm me-2"> View Show </router-link>
                </div>
            </div>

        </div>
    </div>
</template>
  
<script>
import NavBar from '@/components/NavBar.vue';
import jwtDecode from 'jwt-decode';
import axios from 'axios';

export default {
    name: 'SearchResult',
    components: {
        NavBar,
    },
    data() {
        return {
            shows: [],
            theatres: [],
        };
    },
    created() {
        // Call the search method on component creation
        this.search();
    },
    methods: {
        async search() {
            try {
                const search_response = await axios.get(`http://localhost:5000/search?data=${this.$route.params.data}`);
                this.shows = search_response.data.shows;
                this.theatres = search_response.data.theatres;
                console.log(this.shows)
                console.log(this.theatres)
            } catch (error) {
                console.error('Error fetching search results:', error);
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
    }
};
</script>

<style>
.searchResult{
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
    margin: 10px;
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
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}

.bookshowbtn {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
}
</style>
  