<script setup>
import axios from 'axios';
import {onMounted, ref } from 'vue';

// Create an Axios instance with custom options
const instanciaAxios = axios.create({
  httpsAgent: false,
});

const dados = ref([]); //REATIVO
const resposta = ref("");
const mostrarErro = ref(false);

// Quando o componente for montado execute isso:
onMounted(async () => {
  try {
    const response = await instanciaAxios.get('http://localhost/campainhaint/public/api/camera');
    dados.value = response.data;
    //console.log(dados.value);
  } catch (error) {
    console.error('Error fetching data:', error);
    resposta.value = "Erro: " + error.message;
    mostrarErro.value = true;
  }
});
</script>

<template>

<main>
    <div v-if="mostrarErro" class="warning border-2 rounded m-2 p-1">
      Ocorreu um erro na requisição. <br> <span class="text-red-600">{{ resposta}}</span> <br>
      <span v-on:click="mostrarErro = false" class="text-center text-slate-800">Fechar</span>
    </div>
    <div class="border-1 rounded text-bg-gray">
        <p class="text-center">
            {{ dados }}
        </p>
    </div>
    <div class="text-left ml-2">
        <img src="https://cdn0.iconfinder.com/data/icons/game-ui-casual-chunky/533/IconsByAndreaFryer_GameUI_Chunky_Save-512.png" width="40">
        <a href="#">Salvar Rosto</a>
    </div>
</main>
</template>

<style scoped>
</style>