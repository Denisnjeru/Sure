<template>
    <div class="document">
        <iframe ref="documentiframe" class="document__frame" @load="iframeIsLoaded" v-if="documentUrl && loaded === true" :src="'https://docs.google.com/gview?url=' + documentUrl + '&embedded=true'" frameBorder="0"></iframe>
        <span v-else>Loading...</span>
    </div>
</template>

<script>
export default {
    props: ['documentUrl',],
    data() {
        return {
            loaded: false,
            timerInterval: null
        }
    },
    mounted() {
        this.loaded = true
        // this.$refs['documentiframe'].contentWindow.location.href = this.$refs['documentiframe'].src;
    },
    methods: {
        iframeIsLoaded () {            
            console.log('iframe loaded')            
        }
    }
}
</script>

<style lang="scss">
.document {
    width: 100%;

    &__frame {
        position: relative; 
        height: 100%; 
        min-height: 100vh;
        width: 100%;
    }
}
</style>