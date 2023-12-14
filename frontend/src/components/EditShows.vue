<template>
  <div class="add-show">
    <h2>Edit Show</h2>
    <form @submit.prevent="editShow">
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

      <label>Theatre:</label>
      <select v-model="theatre_id" required>
        <option v-for="theatre in theatres" :key="theatre.id" :value="theatre.id">{{ theatre.name }}</option>
      </select>

      <button type="submit">Update</button>
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
    async editShow() {
      try {
        const response = await axios.put(`http://localhost:5000/shows/${this.$route.params.id}`, {
          name: this.name,
          rating: this.rating,
          ticket_price: this.ticket_price,
          start_time: this.start_time,
          end_time: this.end_time,
          theatre_id: this.theatre_id,
        });
        console.log(response);
        this.$router.push("/admindashboard");
      } catch (error) {
        console.error('An error occurred:', error);
      }
    }
    ,
    async fetchTheatres() {
      try {
        const response = await axios.get("http://localhost:5000/theatres");
        this.theatres = response.data;
        console.log(this.theatres)
      } catch (error) {
        console.error(error);
      }
    },
    async fetchShos() {
      try {
        const response = await axios.get(`http://localhost:5000/shows/${this.$route.params.id}`);
        this.name = response.data.name;
        this.rating = response.data.rating;
        this.ticket_price = response.data.ticket_price;
        this.start_time = response.data.start_time;
        this.end_time = response.data.end_time;
        this.theatre_id = response.data.theatre_id;
      } catch (error) {
        console.error(error);
      }
    }
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
  