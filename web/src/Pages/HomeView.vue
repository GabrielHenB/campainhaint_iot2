<script setup>
import {RouterLink} from 'vue-router';
</script>

<template>
    <main class="grid grid-cols-3 m-1">
           <div class="border-2 rounded m-2 text-center">
            <RouterLink to="camera">
                <img class="mx-auto" src="https://cdn-icons-png.flaticon.com/512/2933/2933760.png" width="80">
            
                Camera
            </RouterLink>
           </div>
           <div class="border-2 rounded m-2 text-center">
            <RouterLink to="eventos">
                <img class="mx-auto" src="https://www.svgrepo.com/show/116114/alert.svg" width="80">
                Eventos
            </RouterLink>
           </div>
           <div class="border-2 rounded m-2 text-center">
            <RouterLink to="historico">
                <img class="mx-auto" src="https://uxwing.com/wp-content/themes/uxwing/download/web-app-development/database-line-icon.png" width="80">
                Histórico
            </RouterLink>
           </div>
           <div class="border-2 rounded m-2 text-center">
            <RouterLink to="configuracoes">
                <img class="mx-auto" src="https://cdn-icons-png.flaticon.com/512/93/93800.png" width="80">
                Configurações
            </RouterLink>
           </div>
    </main>
</template>