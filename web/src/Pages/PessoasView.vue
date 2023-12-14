<script setup>
import axios from 'axios';
import {URL_PESSOAS, API_BASE} from '@/api.js';
import {onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

// Create an Axios instance with custom options
const instance = axios.create({
  httpsAgent: false,
});

const dados = ref([]); //REATIVO
const resposta = ref("");
const mostrarErro = ref(false);
const router = useRouter();

// Quando o componente for montado execute isso:
onMounted(async () => {
  try {
    const response = await instance.get(URL_PESSOAS).then(response => {
        if(response.status >= 200 && response.status < 300 && response.data){
          //console.log(response.data.data);
          dados.value = response.data.data; // Se duvida olhar JSON de eventos
        }
        else{
          this.error = "Formato de resposta inválido da requisição!";
        }
    });
  } catch (error) {
    console.error('Error fetching data:', error);
    resposta.value = "Erro: " + error.message;
    mostrarErro.value = true;
  }
});

function redirecionar(query){
  router.push({
    name: 'pessoas_update',
    params: {id: query}
  });
}

</script>

<template>
<main>
    <div v-if="mostrarErro" class="warning border-2 rounded m-2 p-1">
      Ocorreu um erro na requisição. <br> <span class="text-red-600">{{ resposta}}</span> <br>
      <span v-on:click="mostrarErro = false" class="text-center text-slate-800">Fechar</span>
    </div>
    <div v-if="dados.length === 0">Nenhuma pessoa foi registrada</div>
    <section class="contain">
        <article v-for="(item,index) of dados"  class="border-1 rounded m-1 p-1 flex justify-evenly items-center">
            <div class="imgwrapper bg-slate-800 ">
                <img :src="item.img" width="140">
            </div>
            <div class="textcontent">
                <h2 class="persontitle text-center text-slate-500"><strong>Nome:</strong> <span>{{ item.nome }}</span></h2>
                <p class="datahora text-left text-slate-600"><strong>Tem Acesso:</strong> <span>{{  item.tem_acesso }}</span></p>
                <button v-on:click="redirecionar(item.id)" class="btn btn-primary">Modificar</button>
            </div>
            
        </article>
    </section>
</main>
</template>

<style scoped>
</style>