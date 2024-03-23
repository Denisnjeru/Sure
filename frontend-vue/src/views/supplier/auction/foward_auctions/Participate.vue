<template> 
    <div class="risk_job_reports">
        <div class="page__head">
            <span class="page__head--title">
                Foward Auction
            </span>


            <div class="page__head--title">
                <router-link to="/buyer/add/risk-management">
                    <a class="page__head--link button button-link">
                        <span class="button-link__button-text">Download Items Template</span><font-awesome-icon icon="chevron-down"/>
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">{{ auct.name }}</p>
                    <p class="column-details__head--desc">Foward Auction</p>
                </div>
                <div class="column-details__content">
                    <p class="custom_detail"><strong>Auction:</strong> {{ auct.name }}</p>
                    <hr>
                    <p class="custom_detail"><strong>Type:</strong> Foward Auction</p>
                    <hr>
                    <p class="custom_detail"><strong>Pricing Method:</strong> {{ auct.pricing_method }}</p>
                    <hr>
                    <p class="custom_detail"><strong>Opening Time:</strong> {{ auct.opening_date | moment }}</p>
                    <hr>
                    <p class="custom_detail"><strong>Closing Time:</strong> {{ auct.closing_date | moment }}</p>
                    <hr>
                    <p class="custom_detail"><strong>Status:</strong>
                        <span v-if="auct.is_open">Open</span>
                        <span v-else>Closed</span>
                    </p>
                </div>
            </div>
            <div class="column column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Items in this Auction</p>
                    <p class="column-details__head--desc">Please download items template</p>
                </div>
                <div class="column-details__content">
                    <div class="table-search">
                        <p class="table-search__title">
                            <!-- Card Title Header -->
                        </p>
                        <div class="table-search__search">
                            <font-awesome-icon class="table-search__search--icon" icon="search"/>
                            <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                        </div>
                    </div>
                    <v-client-table :data="displayedRecords" :columns="columns" :options="options">
                        <p class="link" slot="Item Name" slot-scope="{row}" @click="onRowClick(row)">
                            {{row.name}}
                        </p>

                        <p class="link_3" slot="Reserve Price" slot-scope="{row}">
                            {{row.currency}} {{row.reserve_price}}
                        </p>
                    </v-client-table>
                    <div class="page__pagination">
                        <pagination style="padding: 0 10px !important" :records="auct.auction_items.length" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                        </pagination>
                    </div>
                    <span class="proceed">
                        <a class="button proceed-link" @click="ProceedToBid()">
                            <span class="proceed-link__proceed-text">Proceed to participate</span>
                        </a>
                    </span>
                </div>
            </div>
        </div>
    </div>   
</template>

<script>
import auctions from '../../../../services/company/auction'
import moment from 'moment'

export default {
    name: 'risk-auction-participate-supplier',
    data () {
        return{
            columns: ['Item Name', 'Reserve Price'],
            auct: {
                "id": 0,
                "name": '',
                "auction_type": '',
                "category_type": '',
                "pricing_method": '',
                "closed_auction": false,
                "closing_date": '',
                "opening_date": '',
                "company": '',
                "is_open": false,
                "created_by": '',
                "created_at": '',
                "overtime_count": 0,
                "overtime_duration": 0,
                "auction_items": []
            },
            options: {
                headings : {

                },
                sortable:['Item Name', 'Reserve Price'],
                sortIcon: {
                    is: "glyphicon-sort",
                    base: "glyphicon",
                    up: "glyphicon-chevron-up",
                    down: "glyphicon-chevron-down"
                },
            },
            page: 1,
            dataPerPage: 10,
        }
    },    
    filters: {
        moment: function (date) {
            return moment(date).format('MMMM Do YYYY, h:mm:ss a');
        }
    },
    mounted(){
        this.getFowardAuction()
    },
    computed:{
        // Return the computed list per page
        displayedRecords(){
            const startIndex = this.dataPerPage * (this.page - 1);
            const endIndex = startIndex + this.dataPerPage;
            return this.auct.auction_items.slice(startIndex, endIndex);
        }
    },
    methods:{
        async ProceedToBid(){
            if(this.auct.is_open){
                this.$router.push('/supplier/bid/'+ this.auct.id +'/foward/auction')
            }else{
                window.toast.fire({icon: 'error', title: "Auction is closed"})
            }
        },
        async getFowardAuction(){
            try{
                const response = await auctions.getSupplierAuction(this.$route.params.auctionId)
                this.auct = response.data
                console.log(this.auct)
            }catch(error){
                console.log(error)
            }
        },
        callback: function(page) {
            // no need for callback here since you have all your data loaded already
            console.log(page)
        }
    }
}
</script>

<style lang="scss" scoped>
@include page;

.page{
    height: 100vh;

    .column{
        display: flex;
        flex-basis: 0;
        flex-grow: 1;
        flex-shrink: 1;
        flex-direction: column;
    }

    .column-details {
        margin: 0 6px;
    }

    &__content{
        width: 100%;
        padding: $line-height $line-height;

        .column-details {
            margin: 0 $line-height/4;
            box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
            border-radius: $line-height/2;
            padding: 0;
            // margin-bottom: $line-height/2;
            height: 100%;

            @media screen and (min-width: 1400px) {
                height: 100%;
            }


            &__head {
                background: $color-baby-blue;
                padding: $line-height/4 $line-height;
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
                // margin-bottom: $line-height*20;

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

                    &__button-detail {

                        width: 200px;
                        color: $color-blue-main;
                        font-size: $font-size-text;
                        background-color: $color-white-main;
                        border: 1px solid $color-blue-main;
                        border-radius: 5px;
                        transform: rotate(0.02deg);

                        &__button-text{
                            display: inline;
                            margin-right: 1em;
                        }

                        &:hover, :focus {
                            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                            transform: translateY(-0.25em);
                        }
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
            }
            &__content_documents{
                padding: $line-height*2 0;
                margin-bottom: $line-height;
                display: block;
                text-align: center;


                .detail_button {
                    padding: $line-height $line-height*2;

                    .button-detail {
                        width: 300.51px;
                        color: $color-white-main;
                        background-color: $color-blue-main;
                        border: none;                
                        font-size: $font-size-text;
                        border-radius: 5px;
                        box-sizing: border-box;
                        transform: rotate(0.02deg);


                        &:hover, :focus {
                            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                            transform: translateY(-0.25em);
                        }
                    }
                }
            }
        }
    }

    .row-link{
        text-align: center;

        &__link{
            display: inline;
            margin-right: 0.5em;
            color: #4CAF50;
        }

        &__text{
            display: inline;
            color: $color-blue-main;
        }

        &__button-detail {
            width: 300.51px;
            color: $color-white-main;
            background-color: $color-blue-main;
            border: none;                
            font-size: $font-size-text;
            border-radius: 5px;
            box-sizing: border-box;
            transform: rotate(0.02deg);

            &__button-text{
                display: inline;
                margin-right: 1em;
            }

            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                transform: translateY(-0.25em);
            }
        }
    }
    .button-link{
        width: 300.51px;
        color: $color-white-main;
        background-color: $color-blue-main;
        border: none;                
        font-size: $font-size-text;
        border-radius: 5px;
        box-sizing: border-box;
        transform: rotate(0.02deg);

        &__button-text{
            display: inline;
            margin-right: 1em;
        }

        &:hover, :focus {
            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
            transform: translateY(-0.25em);
        }
    }
    .link_3{
        color: $color-lightblue-text;
        font-weight: 500;
        cursor: pointer;
        font-size: $font-size-text;
    }
}


.proceed{
    display: grid; 
    justify-content: center;
    .proceed-link{
        width: 300.51px;
        color: $color-white-main;
        background-color: $color-blue-main;
        border: none;                
        font-size: $font-size-text;
        border-radius: 5px;
        box-sizing: border-box;
        transform: rotate(0.02deg);

        &__proceed-text{
            display: inline;
        }

        &:hover, :focus {
            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
            transform: translateY(-0.25em);
            color: $color-white-main;
        }
    }
}

.VueTables__table head {
    background-color: white;
}
hr {
  margin: 0.5rem 0 !important;
}
.column-details-height-custom{
    height: 24vh;
}
.custom_detail{
    padding: $line-height 0;
}
</style>