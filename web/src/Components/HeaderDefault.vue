<script setup>
import {RouterLink} from 'vue-router';
import HeaderLogo from '@/Components/HeaderLogo.vue';
</script>

<template>
    <header>
        <div class="d-flex align-items-center justify-content-between headerbg">
            <HeaderLogo></HeaderLogo>
            <nav class="d-flex gap-3 mx-2">
                <RouterLink class="seila" :to="{name: 'index'}">Home</RouterLink>
                <RouterLink class="seila" :to="{name: 'camera'}">Camera</RouterLink>
                <RouterLink class="seila" :to="{name: 'eventos'}">Eventos</RouterLink>
                <RouterLink class="seila" :to="{name: 'pessoas'}">Pessoas</RouterLink>
            </nav>
        </div>
    </header>
</template>

<style scoped>
.headerbg{
    background-color: #3970e9;
}
.seila{
    color: white;
    text-decoration: none;
}
</style>