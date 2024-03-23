<template> 
    <article class="item">
        {{ item.description }}
        <div class="myslider">
                <VueSlickCarousel 
                    :lazyLoad="ondemand"
                    :arrows="false" 
                    :dots="true" 
                    :autoplay="true" 
                    :autoplayspeed="3000" 
                    class="myslider__carousel"
                    >
                    <div 
                        v-for="(image, index) in item.auction_item_images"
                        :key="image.id"
                        class="myslider__carousel--item"
                        @click="activeImage(index)"
                        >
                        <img :src="image.thumbnail">
                    </div>
                </VueSlickCarousel>
            </div>
        <div class="lot-single">
            <!-- {{ item.name }} -->
            <!-- <Carousel
                :starting-image="0"
                :images="item.auction_item_images"
                :auto-slide-interval="1500"
                :show-progress-bar="true"
            ></Carousel> -->
            <!-- <div class="thumb">
                <div class="image-carousel-container slick-slider">
                    <div @click="prev" class="slick-prev slick-arrow">
                        &#8249;
                    </div>
                    <div class="slick-list draggable">
                        <div class="slick-track">
                            <div class="slick-slide">
                                <a href="#">
                                    <img :src="currentImage" class="slide-in">
                                    <span class="no-image">
                                        <span>No Image</span>
                                        <img alt="No Image" src="#">
                                    </span> 
                                </a>
                            </div>
                        </div> 
                    </div>
                    <div @click="next" class="slick-next slick-arrow">
                        &#8250; 
                    </div>
                </div>
            </div> -->

        </div>
    </article>
</template>

<script>

// import Carousel from './Carousel.vue'

export default {
    name: 'AuctionItem',
    props: ['auctionitem'],
    data(){
        return{
            //Index of the active image
            activeImage: 0,  
            item: this.auctionitem,
            currentImage: ''
        }
    },
    components: {
        // Carousel,
    },

    created(){
        // Setting the starting image
        this.activeImage = 0;
        if(this.auctionitem.auction_item_images.length > 0){
            this.currentImage = this.auctionitem.auction_item_images[this.activeImage].thumbnail
        }
    },
    watch: {
        activeImage(index){
            // console.log('Image has been changed to next !')
            // this.currentImage =  this.item.auction_item_images[this.activeImage].thumbnail
            console.log(index)
            console.log('The above image was selected !')
        }
    },
    methods: {
        next(){
            console.log('yes')
            console.log(this.activeImage)
            var active = this.activeImage + 1;
            if (active >= this.item.auction_item_images.length){
                active = 0;
            }
            this.activateImage(active)
        },
        prev(){
            var active = this.activeImage  - 1;
            if(active < 0){
                active = this.item.auction_item_images.length - 1;
            }
            this.activateImage(active)
        },
        activateImage(imageIndex) {
            this.activeImage = imageIndex;
        },

    }
}

</script>

<style lang="scss" scoped>
.item{
    -webkit-box-flex: 1;
    box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05),
            4px 4px 10px rgba(0, 0, 0, 0.05);
    border-radius: 15px;
    display: block;
    width: 30%;
    max-width: 30%;
    flex: initial;
    text-align: inherit;
    margin-bottom: 3%;
    height: 70vh;
    background-color: blue;
    

    &:first-child{
        margin: auto;
    }

    &:nth-child(ln){
        margin-right: 0%;
        float: left;
    }

    &:nth-child(ln+1){
        clear: both;
    }
}
.item::after{
    content: '';
    display: table;
}
.item::before{
    content: '';
    display: table;
}

.lot-single{
  -webkit-box-orient: horizontal;
  flex-direction: row;
  width: 100%; 
  border-radius: 15px;
  display: flex;
  height: 100%;
  padding: 0;
  margin: 0 auto;
  box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05),
            4px 4px 10px rgba(0, 0, 0, 0.05);

}

.thumb{
    display: flex;
    a{
        padding: 0 40px;
        display: flex;
        width: 100%;
        height: 100%;
        -webkit-box-pack: center;
        justify-content: center;
        align-items: center;
    }
    img{
        max-width: 100%;

    } + .no-image{
        display: none;
        font-size: 12px;
        // background-color: #f0f0f1;
        max-width: 100%;
        width: 100px;
        height: 100px;
        text-align: center;
        position: relative;
    }

    width: 30%;
    vertical-align: top;
    position: relative;
    overflow: hidden;
    padding: 0;
    border-bottom-left-radius: 10px;
    border-top-right-radius: 0;

    @media screen and (min-width: 900px) {
        min-height: 100%;
        height: auto !important;
    }
}

.myslider {
    width: 33.3%;
    height: 100%;

    &__carousel {
        width: 100%;

        &--title {
            font-weight: 700;
            font-size: $line-height;
            margin-bottom: $line-height/2 !important;

            @media screen and (min-width: 1600px) {
                font-size: $line-height*1.5;
                margin-bottom: $line-height !important;
            }
        }


        &--desc {
            font-weight: 500;
            font-size: $font-size-normal;

            @media screen and (min-width: 1600px) {
                font-size: $font-size-title;
            }
        }

        &--item {
            width: 100%;
            height: 50vh;
            color: $color-white-main;
            @include grid_column;
            display: flex !important;
            align-items: center;
            justify-content: center;
        }

        .main-title {
            color: $color-blue-main;
            line-height: $line-height*1.5;
        }
        .item3 {
            background-position: center center;
            background-repeat: no-repeat;
            background-size: cover;
        }
    }
}


slick-track[data-v-e4caeaf8] {
    position: relative;
    top: 0;
    left: 0;
    display: block;
    -webkit-transform: translateZ(0);
    transform: translateZ(0)
}

.slick-track.slick-center[data-v-e4caeaf8] {
    margin-left: auto;
    margin-right: auto
}

.slick-track[data-v-e4caeaf8]:after,
.slick-track[data-v-e4caeaf8]:before {
    display: table;
    content: ""
}

.slick-track[data-v-e4caeaf8]:after {
    clear: both
}

.slick-loading .slick-track[data-v-e4caeaf8] {
    visibility: hidden
}

.slick-slide[data-v-e4caeaf8] {
    display: none;
    float: left;
    height: 100%;
    min-height: 1px
}

[dir=rtl] .slick-slide[data-v-e4caeaf8] {
    float: right
}

.slick-slide img[data-v-e4caeaf8] {
    display: block
}

.slick-slide.slick-loading img[data-v-e4caeaf8] {
    display: none
}

.slick-slide.dragging img[data-v-e4caeaf8] {
    pointer-events: none
}

.slick-initialized .slick-slide[data-v-e4caeaf8] {
    display: block
}

.slick-loading .slick-slide[data-v-e4caeaf8] {
    visibility: hidden
}

.slick-vertical .slick-slide[data-v-e4caeaf8] {
    display: block;
    height: auto;
    border: 1px solid transparent
}

.slick-arrow.slick-hidden[data-v-21137603] {
    display: none
}

.slick-slider[data-v-3d1a4f76] {
    position: relative;
    display: block;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-touch-callout: none;
    -khtml-user-select: none;
    -ms-touch-action: pan-y;
    touch-action: pan-y;
    -webkit-tap-highlight-color: transparent;
    background-color: yellow;
}

.slick-list[data-v-3d1a4f76] {
    height: 30vh;
    position: relative;
    display: block;
    overflow: hidden;
    margin: 0;
    padding: 0;
    -webkit-transform: translateZ(0);
    transform: translateZ(0)
}

.slick-list[data-v-3d1a4f76]:focus {
    outline: none
}

.slick-list.dragging[data-v-3d1a4f76] {
    cursor: pointer;
    cursor: hand
}

</style>