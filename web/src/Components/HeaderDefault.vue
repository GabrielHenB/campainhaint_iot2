<script setup>
import {RouterLink} from 'vue-router';
import HeaderLogo from '@/Components/HeaderLogo.vue';
</script>

<template>
    <header>
        <div class="flex justify-around items-center mb-2 pt-1 pb-2 headerbg text-slate-50">
            <HeaderLogo></HeaderLogo>
            <nav class="flex justify-between align-center">
                <RouterLink class="ml-2" to="/campainhaint/public/">Home</RouterLink>
                <RouterLink class="ml-2" to="camera">Camera</RouterLink>
                <RouterLink class="ml-2" to="historico">Histórico</RouterLink>
                <RouterLink class="ml-2" to="configuracoes">Configurações</RouterLink>
            </nav>
        </div>
    </header>
</template>

<style scoped>
.headerbg{
    background-color: #3970e9;
}
</style>