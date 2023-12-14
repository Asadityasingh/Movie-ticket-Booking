<template>
    <div>
        <NavBar />
        <router-link to="/addtheatre" class="btn btn-primary btn-addtheatre"><i class="bi bi-plus"></i></router-link>

        <div class="theatre-grid">
            <div v-for="theatre in theatres" :key="theatre.id" class="card" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">{{ theatre.name }}</h5> 
                    <h6 class="card-subtitle mb-2 text-body-secondary">Location: {{ theatre.location }}</h6>
                    <h6 class="card-subtitle mb-2 text-body-secondary">Capacity: {{ theatre.capacity }}</h6>
                </div>
                <div class="card-goot">
                    <router-link :to="'/addshow/'+theatre.id" class="btn btn-primary btn-sm me-2"> Add Show </router-link>
                    <router-link :to="'/viewshow/'+theatre.id" class="btn btn-secondary btn-sm me-2"> View Show </router-link>
                    <router-link :to="'/editTheatre/'+theatre.id" class="btn btn-success btn-sm me-2"> <i class="bi bi-pencil-fill"></i> </router-link>
                    <button @click="deleteTheatre(theatre.id)" class="btn btn-danger btn-sm"> <i class="bi bi-trash-fill"></i> </button>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import NavBar from "@/components/NavBar.vue";
import axios from "axios";

export default {
    name: "AdminDashboard",
    components: {
        NavBar,
    },
    data() {
        return {
            theatres: [],
        };
    },
    mounted() {
        this.fetchTheatres();
    },
    methods: {
        async fetchTheatres() {
            try {
                const response = await axios.get("http://localhost:5000/theatres");
                this.theatres = response.data;
                console.log(this.theatres)
            } catch (error) {
                console.error("Error fetching theatres:", error);
            }
        },
        async deleteTheatre(id) {
            try {
                const response = await axios.delete("http://localhost:5000/theatres/" + id);
                console.log(response.data);
                this.fetchTheatres();
            } catch (error) {
                console.error("Error deleting theatre:", error);
            }
        },
    },
};
</script>

<style scoped>
.btn-addtheatre {
    position: absolute;
    bottom: 40px;
    right: 30px;
    font-size: 30px;
    padding: 0;
    width: 90px;
}

.theatre-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    padding: 20px;
}

.card{
    border: none;
    width: fit-content;
    border-radius: 5px;
    padding: 10px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}
</style>
