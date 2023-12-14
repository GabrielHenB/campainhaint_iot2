<script setup>
import {RouterLink } from 'vue-router';
</script>

<template>
<footer>
    <div class="flex justify-between mt-2 pt-2 bg-cyan-800 text-slate-50">
        <h2 class="m-2 text-lg">CampainhaInt, sua campainha, mais inteligente!</h2>
        <div class="grid grid-cols-2 gap-2 m-2">
            <RouterLink :to="{name: 'index'}" class="pl-1">Home</RouterLink>
            <RouterLink to="about" class="pl-1">About Us</RouterLink>
            <RouterLink to="configuracoes" class="pl-1">Configuration</RouterLink>
            <a href="#" class="pl-1">Info</a>
        </div>
    </div>
</footer>
</template>
