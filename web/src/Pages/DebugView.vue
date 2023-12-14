<script setup>
import axios from 'axios';
import {onMounted, ref } from 'vue';

// Create an Axios instance with custom options
const instance = axios.create({
  httpsAgent: false,
});

const dados = ref(null); //REATIVO
const resposta = ref("");
const mostrarErro = ref(false);

function anexar(evento){
    const arquivo = evento.target.files[0];
    if(arquivo){
        console.log(arquivo); //apagar depois
        dados.value = arquivo;
    }
}

async function submitForm() {
      try {
        // Create a FormData object and append the image file
        const formData = new FormData();
        formData.append('imagem', this.theImage);

        // Make a POST request to your server endpoint
        const response = await axios.post('/upload', formData);

        // Handle the response as needed
        console.log('Server response:', response.data);
      } catch (error) {
        // Handle errors
        console.error('Error submitting form:', error);
      }
    }
</script>

<template>
<main>
    <div v-if="mostrarErro" class="warning border-2 rounded m-2 p-1">
      Ocorreu um erro na requisição. <br> <span class="text-red-600">{{ resposta}}</span> <br>
      <span v-on:click="mostrarErro = false" class="text-center text-slate-800">Fechar</span>
    </div>
    <section class="contain">
        <form @submit.prevent="submitForm">
            <label for="imageInput">Select Image:</label>
            <input
            type="file"
            id="imageInput"
            accept="image/*"
            @change="anexar"
            />
            <button type="submit">Submit</button>
        </form>
    </section>
</main>
</template>

<style scoped>
</style>