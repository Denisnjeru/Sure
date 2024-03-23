<template>
    <div class="add_action_item">
        <div class="page__head">
            <span class="page__head--title">
                <span class="left nav-links__link">
                    <router-link
                        to="{this.router.go(-1)}"
                    >
                        <font-awesome-icon icon="chevron-left" />  <span class="text">Back</span>
                    </router-link>
                </span>
            </span>
        </div>
        <div class="page__content">
            <div class="columns is-centered">
                <div class="column-details column is-12">
                    <form v-on:submit.prevent="create_foward_auction_item()" enctype="multipart/form-data">
                        <div class="column-details__head">
                            <p class="column-details__head--title">Create a Foward Auction Item</p>
                            <p class="column-details__head--desc">Fill in the required details</p>
                        </div>
                        <!-- Form Details -->
                        <div class="column-details__content">
                            <div class="columns">
                                <div class="column">
                                    <div class="field">
                                        <label class="label">Item Name <span class="required">*</span></label>
                                        <div class="control">
                                            <input class="input" type="text" placeholder="Enter item name" v-model="item_foward_auction.name" required>
                                        </div>
                                    </div>
                                    <div class="field">
                                        <label class="label">Description <span class="required">*</span></label>
                                        <div class="control">
                                            <input class="input" type="text" placeholder="Enter category name" v-model="item_foward_auction.description" required>
                                        </div>
                                    </div>
                                    <div class="field">
                                        <label class="label">Short Description </label>
                                        <div class="control">
                                            <input class="input" type="text" placeholder="Enter category name" v-model="item_foward_auction.short_description">
                                        </div>
                                    </div>
                                    <div class="field">
                                        <label class="label">Reserve Prices </label>
                                        <div class="control">
                                            <input class="input" type="number" step="any" v-model="item_foward_auction.reserve_prices" required/>
                                        </div>
                                    </div>
                                </div>
                                <div class="column">
                                    <div class="field">
                                        <label class="label">Minimum Price </label>
                                        <div class="control">
                                            <input class="input" type="number" step="any" v-model="item_foward_auction.minimum_price" required/>
                                        </div>
                                    </div>
                                    <div class="field">
                                        <label class="label">Minimum Increment <span class="required">*</span></label>
                                        <div class="control">
                                            <input class="input" type="number" step="any" v-model="item_foward_auction.minimum_increment"/>
                                        </div>
                                    </div>
                                    <div class="document">
                                        <p class="document__title">
                                            <span class="document__title--name">Main Image</span>
                                            <span class="document__title--icon">
                                                <font-awesome-icon class="icon" icon="folder-plus" />
                                            </span>
                                        </p>
                                        <span v-if="MainimageFilesNames[0]" class="document__name">
                                            <span class="document__name--text">
                                                <img src="@/assets/support_doc.png" class="icon">
                                                <span class="name">{{ MainimageFilesNames[0] }}</span>
                                            </span>
                                            <span class="document__name--delete" @click="removemainimage()">
                                                <span class="selected__icon">
                                                    <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                                                </span> 
                                            </span>
                                        </span>
                                        <div class="file has-name">
                                            <label class="file-label">
                                                <input class="file-input" type="file" name="resume" @change="selectMainImage($event)">
                                                <span class="file-cta">
                                                <span class="file-icon">
                                                    <i class="fas fa-upload"></i>
                                                </span>
                                                <span class="file-label">
                                                    Choose an Image…
                                                </span>
                                                </span>
                                                <span v-if="MainimageFilesNames[0]" class="file-name">{{ MainimageFilesNames[0] }}</span>
                                                <span v-else class="file-name">Upload Main Image</span>
                                            </label>
                                        </div>
                                    </div>
                                    <div class="risk_submit">
                                        <input type="submit" class="button button-submit" value="Create">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import auctions from '@/services/company/auction';

    export default {
        name: 'foward-auction-add-item-buyer',
        data(){
            return{
                item_foward_auction: {
                    "name": '',
                    "description": '',
                    "short_description": '',
                    "reserve_prices": '',
                    "minimum_price": '',
                    "minimum_increment": '',
                    "main_image": null        
                },
                error_text: '',
                MainimageFilesNames: []
            }
        },
        components:{
        },
        mounted:{
        },
        created:{
        },
        computed:{
        },
        methods:{
            removemainimage(){
                this.MainimageFilesNames = []
            },
            selectMainImage(event){
                let fieldName = event.target.name;
                let fileList =  event.target.files;

                if (!fileList.length) return;
                this.item_foward_auction.main_image = event.target.files[0]

                const fd = new FormData()
                Array
                .from(Array(fileList.length).keys())
                .map( x => {
                    fd.append(fieldName, fileList[x], fileList[x].name)
                });

                Array
                .from(Array(fileList.length).keys())
                .map(x =>{
                    this.MainimageFilesNames.push(fileList[x].name);
                });

                console.log(this.MainimageFilesNames)
                console.log(this.item_foward_auction.main_image)
            },
            async create_foward_auction_item(){
                try {

                    const fd = new FormData()
                    fd.append('name',this.item_foward_auction.name)
                    fd.append('description',this.item_foward_auction.description)
                    fd.append('short_description',this.item_foward_auction.short_description)
                    fd.append('reserve_prices',this.item_foward_auction.reserve_prices)
                    fd.append('minimum_price',this.item_foward_auction.minimum_price)
                    fd.append('minimum_decrement',this.item_foward_auction.minimum_decrement)

                    if (this.item_foward_auction.main_image !== null){
                        fd.append('main_image',this.item_foward_auction.main_image)
                    }
                    const response = await auctions.addAuctionItem(this.$route.params.auctionId, fd)
                    console.log(response.status)
                    if(response.status == 201){
                        console.log(response.data)
                        window.toast.fire({icon: 'success', title: "Auction item created successfully"})
                        // this.$router.push('/buyer/category/'+ this.$route.params.riskId +'/'+response.data['id'] + '/risk-management/')
                    }
                }catch(error){
                    console.log('Logging the error')
                    console.log(error.response)
                    window.toast.fire({icon: 'error', title: error.response.data['error']})
                }
            }
        }
    }
</script>
<style lang="scss" scoped>
.page {

    .nav-links__link {
        color: $color-blue-main;

        .text {
            font-size: font-size-major;
            font-weight: 600;
        }

        &:hover {
            cursor: pointer;
        }
    }

    &__content {
        padding: $line-height 5%;
        position: relative;
        z-index: 20; 
    
    .column-details {
        margin: 0 $line-height/4;
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: $line-height/2;
        padding: 0;
        margin-bottom: $line-height/2;

        &__head {
            background: $color-baby-blue;
            padding: $line-height $line-height;
            border-radius: $line-height/2 $line-height/2 0 0;

            &--title {
                color: rgba(18, 31, 62, 0.8);
                font-size: $font-size-title;
                font-weight: 600;
                margin-bottom: $line-height/6 !important;
            }

            &--desc {
                color: $color-black-medium;
                margin: $line-height/4 0;
            }
        }

        &__content {
            padding: $line-height/2 $line-height;
            margin-bottom: 0;

            .detail {
                padding: $line-height 0;
                border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);

                &__title {
                    font-weight: 600;
                    margin-right: $line-height/2;
                    color: $color-black-main;
                }

                &__text {
                    color: $color-lightblue-text;
                }
            }

            .document {
                padding: $line-height 0;
                border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);
                position: relative;
                z-index: 1;

                &__status {
                    position: absolute;
                    z-index: 20;
                    padding: $line-height/6 $line-height/3;
                    color: $color-lightblue-text;
                    background: #F2F6FF;
                    border: 1px solid #073A82;
                    box-sizing: border-box;
                    box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
                    border-radius: 10px;
                    font-size: $font-size-small;
                    left: 60%;
                    display: none;
                }                    

                &__title {
                    width: 100%;
                    @include grid_row;

                    &--name {
                        font-weight: 600;
                        color: $color-black-main;
                    }

                    &--icon {
                        color: $color-gray-main;
                    }

                    .missing {
                        color: $color-red-main;
                    }
                }

                &__name {
                    width: 100%;
                    @include grid_row;
                    align-items: center;
                    margin-top: $line-height/3;
                    background: #F8F8F8;
                    box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
                    border-radius: $line-height/2;
                    padding: $line-height/4 $line-height/2;
                    font-size: $font-size-text;

                    &--text {
                        @include grid_row;
                        align-items: center;

                        .icon {
                            margin-right: $line-height/4;
                            height: $line-height;
                        }
                    }

                    &--delete {

                        .selected__icon {
                            margin: 0 $line-height/4;

                            &--img {
                                height: $line-height/1.2;
                                padding: $line-height/6;
                                background-color: $color-gray-main;
                                color: $color-white-main;
                                border-radius: 50%;
                                cursor: pointer;

                                &:hover {
                                    background-color: $color-red-main;
                                }
                            }
                        }
                    }
                }

                &:hover {
                    .doc-missing {
                        color: $color-red-main;
                        cursor: pointer;
                    }

                    .document__status {
                        display: block;
                    }
                }
            }

            .selected__icon {
                margin: 0 $line-height/4;

                &--img {
                    height: $line-height/1.2;
                    padding: $line-height/6;
                    background-color: $color-gray-main;
                    color: $color-white-main;
                    border-radius: 50%;
                    cursor: pointer;

                    &:hover {
                        background-color: $color-red-main;
                    }
                }
            }
            .risk_submit {
                padding: $line-height/2 0;
                // margin: $line-height/2 0;
                
                .button-submit {
                    width: 100%;
                    color: $color-white-main;
                    background-color: $color-blue-main;
                    border: none;                
                    font-size: $font-size-text;
                }
            }
            .show_bids {
                display: inline-block;
                color: $color-blue-main;

                .text {
                    font-size: $font-size-text;
                    font-weight: 600;
                    padding: 12px;
                }
            }
        }

        input[type="number"] {
            -webkit-appearance: textfield !important;
            -moz-appearance: textfield !important;
            appearance: textfield !important;
        }

        input[type=number]::-webkit-inner-spin-button,
        input[type=number]::-webkit-outer-spin-button {
            -webkit-appearance: none;
        }

        .wrapper {
            border: 2px #dcd3d3 solid;
            display: flex;
            border-radius: 15px;
        }

        .plusminus {
            height: 100%;
            width: 30%;
            background: white;
            border: none;
            font-size: 40px;
            color: #5f5fce;
        }

        .num {
            height: 10%;
            width: 10%;
            border: none;
            font-size: 30px;
        }
    }

    }

}
</style>
