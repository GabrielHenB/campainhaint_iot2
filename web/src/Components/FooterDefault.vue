<script setup>
import {RouterLink } from 'vue-router';
</script>

<template>
<footer class="footerbg py-4 px-1 text-light">
    <div class="d-flex justify-content-center">
        
        <div class="d-flex align-items-center gap-5">
            <RouterLink :to="{name: 'index'}" class="text-decoration-none text-light">
                <i class="fs-2 bi bi-house-door-fill"></i>
            </RouterLink>
            <RouterLink :to="{name: 'pessoas'}" class="text-decoration-none text-light">
                <i class="fs-2 bi bi-file-person-fill"></i>
            </RouterLink>
            <RouterLink :to="{name: 'eventos'}" class="text-decoration-none text-light">
                <i class="fs-2 bi bi-clock-history"></i>
            </RouterLink>
            <RouterLink :to="{name: 'configuracoes'}" class="text-decoration-none text-light">
                <i class="fs-2 bi bi-gear-fill"></i>
            </RouterLink>
        </div>
    </div>
</footer>
</template>
<style scoped>
i:hover{
    color: #9ae2ff;
}
.footerbg{
    background-color: #040404;
    position: fixed;
    width: 100%;
    bottom: 0;
}
</style>