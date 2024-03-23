<template>
    <div class="risk_category_details">
        <div class="page__head">
            <div class="page__head--title">
                <span class="left nav-links__link">
                    <font-awesome-icon icon="chevron-left" /> <span class="text">Back</span>
                </span>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column-details column">
                <div class="column-details__head">
                    <p class="column-details__head--title">{{ auctionitem.name }}</p>
                </div>
                <div class="column-details__content">
                    <p><strong>Best Bidder:</strong>******************</p>
                    <hr>
                    <p><strong>Best Bid Price:</strong> KES 80.00</p>
                    <hr>
                    <p><strong>Closing Time:</strong> {{auctionitem.item_closing_time | moment }}</p>
                    <hr>
                    <p><strong>Status:</strong> {{status}}</p>
                </div>
            </div>
            <div class="column-details column">
                <div class="column-details__head" style="background: white;">
                    <p class="column-details__head--title">Actions</p>
                    <p class="column-details__head--desc">Job Actions </p>
                    <hr>
                </div>
                <div class="column-details__content_documents">
                    <p class="detail_button">
                        <router-link to="/update-profile">
                            <a class="button button-detail">
                                Supporting Documents
                            </a>
                        </router-link>
                    </p>
                    <p class="detail_button">
                        <router-link to="/update-profile">
                            <a class="button button-detail">
                                Invited Participants
                            </a>
                        </router-link>
                    </p>
                </div>
            </div>
        </div>

        <div class="page__content columns">
            <div class="column column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Bidding Activity</p>
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
                    <v-client-table :data="data" :columns="columns" :options="options">
                        <span slot="Supplier" slot-scope="{row}">
                            {{row.Supplier}}
                        </span>
                        <span slot="Bid Price" slot-scope="{row}">
                            {{row.Bid_Price}}
                        </span>
                        <span slot="Bid Time" slot-scope="{row}">
                            {{row.Bid_Time}}
                        </span>
                    </v-client-table>
                </div>
                <div class="page__pagination">
                        <pagination style="padding: 0 20px !important" :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                        </pagination>
                </div>
            </div>
            <div class="column column-details">
                <div class="column-details__content">
                    <div class="graph line">
                        <div class="line-graph">
                            <div class="line-graph__graph">
                                <LineChart :chartHeight="'120%'" />
                            </div>
                        </div>
                        <div class="line-details">
                            <p class="graph__title">Bidding Activity</p>
                            <p class="graph__desc">(+15%) increase in todays activities.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import LineChart from '@/components/charts/LineChart'
import auctions from '@/services/company/auction'
import moment from 'moment'
export default {
    name: 'foward-auction-item-details-buyer',
    data () {
        return{
            columns: ['#', 'Supplier', 'Bid Price', 'Bid Time'],
            data: [
                {
                    'Supplier':'Gathage Solutions', 
                    'Bid_Price':'KES 80',
                    'Bid_Time':'Nov. 22, 2020, 10:31 p.m.',
                },{
                    'Supplier':'Denis Suppliers', 
                    'Bid_Price':'KES 120',
                    'Bid_Time':'Nov. 22, 2020, 12:31 p.m.',
                },{
                    'Supplier':'Demo', 
                    'Bid_Price':'KES 100',
                    'Bid_Time':'Nov. 22, 2020, 10:31 p.m.',
                },
                {
                    'Supplier':'Demo', 
                    'Bid_Price':'KES 110',
                    'Bid_Time':'Nov. 22, 2020, 10:31 p.m.',
                },
            ],
            auctionitem: {
                "name": '',
                "description": '',
                "short_description": '',
                "reserve_price": '',
                "minimum_price": 0,
                "minimum_increment": 0,
                "best_bid_price": 0,
                "main_image": null,
                "item_opening_time": '',
                "item_closing_time": '',
                "item_status": null
            },
            options: {
                headings : {

                },
                sortable:['Supplier', 'Bid Price', 'Bid Time'],
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
        this.getItemDetails()
    },
    computed:{
        status(){
            return this.auctionitem.item_status ? 'Open': 'Closed'
        },
        // Return the computed list per page
        displayedRecords(){
            // const startIndex = this.dataPerPage * (this.page - 1);
            // const endIndex = startIndex + this.dataPerPage;
            // return this.auction.auction_items.slice(startIndex, endIndex);
            return null
        }
    },
    components: {
        LineChart
    },
    methods:{
        async onRowClick() {
            this.$router.push('/buyer/section/'+ 1 +'/'+ 1 +'/'+ 1 +'/risk-management/')
        },
        async onEditClick() {
            this.$router.push('/buyer/edit/section/'+ 1 +'/'+ 1 +'/'+ 1 +'/risk-management/')
        },
        async getItemDetails(){
            try {
                console.log('ghghgh')
                const response = await auctions.getAuctionItem(this.$route.params.auctionId, this.$route.params.itemId)
                console.log(response.data)
                this.auctionitem = response.data
            }catch(err){
                console.log(err)
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
    &__content{
        width: 100%;
        padding: $line-height $line-height;

        .column-details {
            margin: 0 $line-height/4;
            box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
            border-radius: $line-height/2;
            padding: 0;
            margin-bottom: $line-height/2;

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
                margin-bottom: $line-height*2;

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

        &__edit{
            display: inline;
            margin-right: 1em;
            color: #4CAF50;
            
            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                transform: translateY(-0.25em);
            }
        }

        &__delete{
            display: inline;
            color: #FF6760;
            
            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                transform: translateY(-0.25em);
            }
        }
    }

    .card_header{

        
        &__text{
            display: inline;
            color: $color-black-main;
            font-weight: 600;
            padding: 0 $line-height*10 0 0;
        }

        &__button{
            display: inline;
            margin-right: 1em;
            width: 100%;
            color: $color-white-main;
            background-color: $color-blue-main;
            border: none;                
            font-size: $font-size-text;
            border-radius: 5px;
            box-sizing: border-box;


            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em rgba(255, 255, 255, 0.05);
                transform: translateY(-0.25em);
            }

        }
    }
}
hr {
  margin: 0.5rem 0 !important;
}
.column-details-height-custom{
    height: 24vh;
}
</style>