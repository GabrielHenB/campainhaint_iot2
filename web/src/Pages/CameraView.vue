<script setup>
import axios from 'axios';
import {URL_UPLOAD} from '@/api.js';
import {onMounted, ref } from 'vue';

// Create an Axios instance with custom options
const instanciaAxios = axios.create({
  httpsAgent: false,
});

const coisa = ref(""); //REATIVO
const resposta = ref("");
const mostrarErro = ref(false);

function handleSubmit(ev){
        
            const impute = ev.target.querySelector('input[type="file"]').files[0];
            
            if(impute){
                const dados = new FormData(ev.target); //Consiste nos dados do form
                fetch(URL_UPLOAD, {
                    method: 'POST',
                    body: dados
                }).then(resposta => {
                    if(resposta.ok) console.log("Sucesso");
                    else{
                        console.log("Ocorreu um erro durante o envio");
                        return resposta.json();
                    }
                }).then(dados => {
                    if(dados) throw new Error("| " + dados.status + " de mensagem: " + dados.msg)
                }).catch(err =>  {
                    console.log("Erro Fetcher: " + err);
                    renderError(err);
                });
                //ev.target.submit();
            }
            else
                console.log("Formulario vazio");
}

function renderError(msg){
  resposta.value=msg;
  mostrarErro.value=true;
}

</script>

<template>

<main>
    <div v-if="mostrarErro" class="warning border-2 rounded m-2 p-1">
      Ocorreu um erro na requisição. <br> <span class="text-red-600">{{ resposta}}</span> <br>
      <span v-on:click="mostrarErro = false" class="text-center text-slate-800">Fechar</span>
    </div>
    <div class="border-1 rounded text-bg-gray">
        <p class="text-center">
            <strong>Selecione uma foto para enviar ao sistema</strong>
        </p>
    </div>
    <div>
      <form @submit.prevent="handleSubmit" class="text-center" id="inputMain" action="/upload" method="POST">
        <div class="input-group mb-3">
            <input type="file" class="form-control" name="imagem" id="inputImagem">
            <label class="input-group-text" for="inputImagem">Upload</label>
        </div>
        
        <input type="hidden" name="csrf" value="teste" />
        <input class="btn btn-primary" type="submit" value="Enviar">
    </form>
    </div>
</main>
</template>

<style scoped>
</style>