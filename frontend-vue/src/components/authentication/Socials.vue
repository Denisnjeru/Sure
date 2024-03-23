<template>
    <div class="socials">
        <a class="socials__icon" href="https://www.facebook.com/Tendersure-101402984663438">
            <img class="socials__icon--img" src="@/assets/facebook.png" alt="">
        </a>
        <a class="socials__icon" href="https://twitter.com/tendersurekenya">
            <img class="socials__icon--img" src="@/assets/twitter.png" alt="">
        </a>
        <a  class="socials__icon" href="https://www.linkedin.com/company/tendersure/">
            <img class="socials__icon--img" src="@/assets/linkedin.png" alt="">
        </a>
        <a href="http://" class="socials__icon" @click="openWhatsApp()">
            <img class="socials__icon--img" src="@/assets/whatsapp.jpeg" alt="">
        </a>
        <a href="http://" class="socials__icon">
            <img class="socials__icon--img" src="@/assets/instagram.png" alt=""> 
        </a>
    </div>
</template>

<style lang="scss" scoped>
    .socials {
        margin-top: $line-height/2;

        &__icon {

            &--img {
                height: $line-height/1.5;
            }

            cursor: pointer;
        
            &:not(:first-child) {
                margin-left: $line-height;
            }
        }
    }
</style>

<script>
export default {
    data(){
        return {

        }
    },
    methods: {
        openWhatsApp: function() {
            window.open(
                'https://web.whatsapp.com/send?phone=2547114892485',
                '_blank'
            );
        }
    }
}
</script>
