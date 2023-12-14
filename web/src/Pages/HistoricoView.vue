<script setup>
import axios from 'axios';
import {URL_EVENTOS, URL_SALVAR, API_BASE} from '@/api.js';
import {onMounted, ref } from 'vue';

// Create an Axios instance with custom options
const instance = axios.create({
  httpsAgent: false,
});

const dados = ref([]); //REATIVO
const resposta = ref("");
const mostrarErro = ref(false);
const descricao = ref("");
const temAcesso = ref(false);

// Quando o componente for montado execute isso:
onMounted(async () => {
  try {
    const res = await instance.get(URL_EVENTOS).then(response => {
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

function handle(ev, index){
  // Construir os dados a partir do evento e do indice em dados
  const a_descricao = dados.value[index].descricao;
  const o_nome = dados.value[index].nome;
  const o_acesso = dados.value[index].tem_acesso;
  const id_evento = dados.value[index].id_evento;
  // Construir o FormData
  const formData = new FormData();
  formData.append('descricao', a_descricao);
  formData.append('nome', o_nome);
  formData.append('tem_acesso', o_acesso);
  formData.append('id_evento', id_evento);
  if(id_evento && o_acesso != null && o_nome){
    instance.post(URL_SALVAR, formData).then(response => {
      //console.log(response);
      mostrarSucesso.value = true;
    }).catch(err => {
      console.error(err, err.message);
      resposta.value = err.response.data.msg; // Se estiver em duvida o JSON
      mostrarErro.value = true;
    });
  }else{
    renderError("Um dos valores não foi encontrado!");
  }
}

function renderError(msg){
  resposta.value=msg;
  mostrarErro.value=true;
}

</script>

<template>
<main>
    <div v-if="mostrarErro" class="warning border-2 rounded m-2 p-1">
      Ocorreu um erro na requisição. <br> <span class="text-danger">{{ resposta}}</span> <br>
      <span v-on:click="mostrarErro = !mostrarErro" class="text-center text-danger">Fechar</span>
    </div>
    <div v-if="dados.length === 0">Nenhum evento foi registrado</div>
    <section class="contain">
        <article v-for="(item,index) of dados"  class="border-1 rounded m-1 p-1 flex justify-evenly items-center">
            <div class="imgwrapper bg-slate-800 ">
                <img :src="API_BASE+item.photo_path" width="140">
            </div>
            <div class="textcontent">
                <h2 class="persontitle text-center text-slate-500"><strong>Nome:</strong> <span>{{ item.nome }}</span></h2>
                <p class="datahora text-left text-slate-600"><strong>Descrição:</strong> <textarea v-model="item.descricao"></textarea></p>
                <label for="inputTemAcesso">Tem Acesso = {{ item.tem_acesso }}</label>
                <input type="checkbox" name="tem_acesso" id="inputTemAcesso" v-model="item.tem_acesso">
                <p class="datahora text-left text-slate-600"><strong>Horário:</strong> <span>{{  item.data }}</span></p>
                <div class="ml-2">
                  <img src="https://cdn0.iconfinder.com/data/icons/game-ui-casual-chunky/533/IconsByAndreaFryer_GameUI_Chunky_Save-512.png" width="40">
                  <button @click="handle($event, index)" class="btn btn-primary">Salvar Rosto</button>
                </div>
            </div>
            
        </article>
    </section>
</main>
</template>

<style scoped>
</style>