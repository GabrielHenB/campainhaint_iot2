<script setup>
import {RouterLink} from 'vue-router';
</script>

<template>
    <main class="container-fluid">
        <div class="row justify-content-start">
            <div class="col my-2">
                <RouterLink class="d-flex flex-column align-items-center d-flex flex-column justify-content-center text-decoration-none" :to="{name: 'camera'}">
                    <img class="" src="https://cdn-icons-png.flaticon.com/512/2933/2933760.png" width="80">
                    Camera
                </RouterLink>
            </div>
            <div class="col my-2">
                <RouterLink class="d-flex flex-column align-items-center d-flex flex-column justify-content-center text-decoration-none" :to="{name: 'eventos'}">
                    <img class="" src="https://www.svgrepo.com/show/116114/alert.svg" width="80">
                    Eventos
                </RouterLink>
            </div>
            <div class="col my-2">
                <RouterLink class="d-flex flex-column align-items-center d-flex flex-column justify-content-center text-decoration-none" :to="{name: 'pessoas'}">
                    <img class="" src="https://uxwing.com/wp-content/themes/uxwing/download/web-app-development/database-line-icon.png" width="80" height="80">
                    Pessoas
                </RouterLink>
            </div>
            <div class="col my-2">
                <RouterLink class="d-flex flex-column align-items-center d-flex flex-column justify-content-center text-decoration-none" :to="{name: 'configuracoes'}">
                    <img class="" src="https://cdn-icons-png.flaticon.com/512/93/93800.png" width="80">
                    Configurações
                </RouterLink>
            </div>
        </div>
    </main>
</template>