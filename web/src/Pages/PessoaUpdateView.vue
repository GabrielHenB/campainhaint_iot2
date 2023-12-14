<script setup>
import axios from 'axios';
import {URL_PESSOAS,URL_PESSOAS_UP, API_BASE} from '@/api.js';
import {ref, watch} from 'vue';
import { useRouter, useRoute } from 'vue-router';

// Create an Axios instance with custom options
const instance = axios.create({
  httpsAgent: false,
});

const dados = ref([]); //REATIVO
const temAcesso = ref(false)
const resposta = ref("");
const mostrarErro = ref(false);
const mostrarSucesso = ref(false);
const router = useRouter();
const route = useRoute();

// Quando o componente for montado execute isso:
const o_id = route.params.id;

function redirecionar(){
  router.push({
    name: 'pessoas',
  });
}

function handle(ev){
  const dados = new FormData(ev.target);
  if(o_id){
    dados.append('tem_acesso', temAcesso.value);
    instance.put(URL_PESSOAS_UP+`/${o_id}`, dados).then(response => {
      //console.log(response);
      mostrarSucesso.value = true;
    }).catch(err => {
      console.error(err);
      resposta.value = err.message;
      mostrarErro.value = true;
    });
  }else{
    renderError("Um ID não foi encontrado!");
  }
}

function deletar(ev){
  if(o_id){
    instance.delete(URL_PESSOAS+'/deletar'+`/${o_id}`).then(response => {
      //console.log(response);
      mostrarSucesso.value = true;
      redirecionar();
    }).catch(err => {
      console.error(err);
      resposta.value = err.message;
      mostrarErro.value = true;
    });
  }else{
    renderError("Um ID não foi encontrado!");
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
      <span v-on:click="mostrarErro = false" class="text-center text-danger">Fechar</span>
    </div>
    <div v-if="mostrarSucesso" class="success border-2 rounded m-2 p-1">
      <span class="text-success">Alteração efetuada com sucesso! </span> <br>
      <span v-on:click="mostrarErro = false" class="text-center text-danger">Fechar</span>
    </div>
    <section class="contain">
        <article  class="border-1 rounded m-1 p-1 flex justify-evenly items-center">
            <form @submit.prevent="handle" id="inputSalvar" action="/salvar" method="POST">
                <label for="inputNome">Nome da Pessoa: </label>
                <input type="text" name="nome" id="inputNome">
                <label for="inputTemAcesso">Tem Acesso ? </label>
                <input type="checkbox" name="tem_acesso" id="inputTemAcesso" :value="temAcesso">
                <input type="hidden" name="csrf" value="teste" />
                <input type="submit" value="Atualizar">
                <button class="btn btn-danger" v-on:click="deletar">Deletar Pessoa</button>
            </form>
        </article>
    </section>
</main>
</template>

<style scoped>
</style>