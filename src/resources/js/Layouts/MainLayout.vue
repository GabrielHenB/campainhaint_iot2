<script setup>
import HeaderDefault from '@/Components/HeaderDefault.vue';
import FooterDefault from '@/Components/FooterDefault.vue';

</script>

<template>
    <HeaderDefault />
    <div id="content">
        <slot />
    </div>
    <FooterDefault />
</template>

<style>
#content{
    min-height: 100vh;
}
</style>