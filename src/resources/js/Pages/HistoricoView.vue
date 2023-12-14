<script setup>
import axios from 'axios';
import {onMounted, ref } from 'vue';

// Create an Axios instance with custom options
const instance = axios.create({
  httpsAgent: false,
});

const dados = ref([]); //REATIVO
const resposta = ref("");
const mostrarErro = ref(false);

// Quando o componente for montado execute isso:
onMounted(async () => {
  try {
    const response = await instance.get('http://localhost/campainhaint/public/api/historico');
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
    <section class="contain">
        <article v-for="(item,index) of dados"  class="border-1 rounded m-1 p-1 flex justify-evenly items-center">
            <div class="imgwrapper bg-slate-800 ">
                <img :src="item.img" width="140">
            </div>
            <div class="textcontent">
                <h2 class="persontitle text-center text-slate-500"><strong>Nome:</strong> <span>{{ item.pessoa }}</span></h2>
                <p class="datahora text-left text-slate-600"><strong>Horário:</strong> <span>{{  item.dh_evento }}</span></p>
            </div>
            
        </article>
    </section>
</main>
</template>

<style scoped>
</style>