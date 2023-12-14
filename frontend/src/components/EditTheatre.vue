<template>
    <div class="add-theatre">
        <h2>Edit Theatre</h2>
        <form @submit.prevent="updateTheatre">
            <label>Name:</label>
            <input v-model="name" type="text" required />

            <label>Location:</label>
            <input v-model="location" type="text" required />

            <label>Capacity:</label>
            <input v-model.number="capacity" type="number" required />

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
        location: "",
        capacity: "",
      };
    },
    methods: {
      async updateTheatre() {
        try {
          const response = await axios.put(`http://localhost:5000/theatres/${this.$route.params.id}`, {
            name: this.name,
            location: this.location,
            capacity: this.capacity,
          });
          console.log(response.data.message);
            this.name = "";
            this.location = "";
            this.capacity = "";
          this.$router.push("/adminDashboard");
        } catch (error) {
          console.error("Error registering user:", error);
        }
      },
    },
  };
  </script>
  
<style scoped>
.add-theatre {
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
  