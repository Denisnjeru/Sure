<template>
    <div class="nav">
        <div class="columns is-vcentered">
            <div class="column is-8 brand">
                <router-link to="/">
                    <img class="brand__logo" src="@/assets/logo.png" alt="logo">
                </router-link>
            </div>
            <div class="column is-4 right">  
                <div class="control has-icons-left languages">
                    <div class="select">
                        <select class="languages__dropdown" v-model="$i18n.locale">
                            <option selected value="en">English (en)</option>
                            <option>Portuguese (pt)</option>
                            <option value="fr">Français (fr)</option>
                            <option>Kiswahili (sw)</option>
                            <option>Amharic (am)</option>
                        </select>
                    </div>
                    <div class="icon is-small is-left">
                        <font-awesome-icon class="main-icon" icon="globe" />
                    </div>
                </div>              
                <a href="https://www.tendersure.co.ke/tutorials/" target="_blank" class="video-link">
                    Tutorial videos
                </a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return { langs: ['en', 'fr'] }
    }
}
</script>

<style lang="scss" scoped>
.nav {
    width: 100%;
}

.brand {
    &__logo {
        height: $line-height*3;
    }
}

.right {
    @include grid_row;
    justify-content: flex-end;

    .languages {
        font-size: $font-size-text;
        margin-right: $line-height/3;
       

        .select {
            width: $line-height*6.5; 
            
            select {
                font-size: $font-size-small;  
            }         
        }

        &__dropdown {
            border: none;
            border-radius: $line-height/2;
            background: rgba(0, 0, 0, 0.05);
            padding-right: 1em !important;
            outline: none !important;
            color: $color-blue-main;

            &:focus {
                outline: none !important;
            }
        }

        .main-icon {
            font-size: $font-size-title;
            color: $color-blue-main;
        }
    }

    .video-link {
        color: $color-green-main;
        font-weight: 600;
        font-size: $font-size-title;
        padding-left: $line-height/2;
        height: 100%;
        border-left: 2px solid #E8E8E8; 
        cursor: pointer;
    }
}
</style>
