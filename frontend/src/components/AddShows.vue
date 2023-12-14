<template>
    <div class="add-show">
        <h2>Add Show</h2>
        <form @submit.prevent="addShow">
            <label>Name:</label>
            <input v-model="name" type="text" required />

            <label>Rating:</label>
            <input v-model.number="rating" type="number" step="0.1" min="0" max="5" required />

            <label>Ticket Price:</label>
            <input v-model.number="ticket_price" type="number" step="0.01" required />

            <label>Start Time:</label>
            <input v-model="start_time" type="time" required />

            <label>End Time:</label>
            <input v-model="end_time" type="time" required />

            <button type="submit">Add</button>
        </form>
    </div>
</template>
  
<script>
  import axios from "axios";
  
  export default {
    data() {
        return {
            name: "",
            rating: 0,
            ticket_price: 0,
            start_time: "",
            end_time: "",
            theatre_id: "",
            theatres: [], // Add this line to define theatres
        };
    },
    mounted() {
        this.fetchTheatres();
    },
    methods: {
      async addShow() {
        const theatreId = this.$route.params.id;
        const response = await axios.post(`http://localhost:5000/shows?theatre_id=${theatreId}`, {
            name: this.name,
            rating: this.rating,
            ticket_price: this.ticket_price,
            start_time: this.start_time,
            end_time: this.end_time
        });
        console.log(response.data.message);
        this.$router.push("/adminDashboard");
      },
      async fetchTheatres() {
        try {
          const response = await axios.get("http://localhost:5000/theatres");
          this.theatres = response.data;
          console.log(this.theatres)
        } catch (error) {
          console.error(error);
        }
      },
    },
  };
  </script>
  
<style scoped>
.add-show {
    max-width: 400px;
    margin: 0 auto;
}

form {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

label {
    font-weight: bold;
}

button {
    align-self: flex-start;
}
</style>
  