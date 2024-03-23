<template>
    <div class="risk_job_details">
        <div class="page__head">
            <div class="page__head--title">
                <span class="left nav-links__link">
                    <font-awesome-icon icon="chevron-left" /> <span class="text">Back</span>
                </span>
            </div>
        </div>
        <div class="page__content columns top_content" style="align-items: inherit !important;">
            <div class="column-details column">
                <div class="column-details__head">
                    <p class="column-details__head--title">Auction: {{ auction.name }}</p>
                </div>
                <div class="column-details__content">
                    <p><strong>Type:</strong> Reverse Auction</p>
                    <hr>
                    <p><strong>Opening Time:</strong> {{auction.opening_date | moment }}</p>
                    <hr>
                    <p><strong>Closing Time:</strong> {{auction.closing_date | moment }}</p>
                    <hr>
                    <p><strong>Status:</strong> {{status}}</p>
                    <hr>
                    <p><strong>Created on:</strong> {{auction.created_at | moment }}</p>
                    <hr>
                    <p><strong>Created by:</strong> {{ auction.created_by }}</p>
                    <hr>
                    <p class="detail">
                        <span class="detail__title">Download Items Template:</span>                                            
                        <a href="#" @click="downloadExcelTemplate()" class="button detail__button-detail">
                            <span class="detail__button-detail__button-text">Items Template</span><font-awesome-icon  class="detail__button-detail__button-text" icon="inbox"/>
                        </a>
                    </p>
                    <div class="document">
                        <span class="detail__title">Import Items from Excel:</span>                                            
                        <span v-if="ExcelfileNames[0]" class="document__name">
                            <span class="document__name--text">
                                <img src="@/assets/excel.png" class="icon">
                                <span class="name">{{ExcelfileNames[0]}}</span>
                            </span>
                            <span class="document__name--delete" @click="removeexcelfile()">
                                <span class="selected__icon">
                                    <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                                </span> 
                            </span>
                        </span>
                        <div class="file has-name" style="width: 85% !important;">
                            <label class="file-label">
                                <input class="file-input" type="file" @change="selectExcelDocument($event)" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
                                 <span class="file-cta">
                                <span class="file-icon">
                                    <i class="fas fa-upload"></i>
                                </span>
                                <span class="file-label">
                                    Choose a file…
                                </span>
                                </span>
                                <span v-if="ExcelfileNames[0]" class="file-name">{{ExcelfileNames[0]}}</span>
                                <span v-else class="file-name">Upload Items Template</span>
                            </label>
                        </div>
                    </div>
                </div>
            </div>
            <div class="column-details column">
                <div class="column-details__head" style="background: white;">
                    <p class="column-details__head--title">Actions</p>
                    <p class="column-details__head--desc">Job Actions </p>
                    <hr>
                </div>
                <div class="column-details__content">
                    <div class="columns document">
                        <div class="column is-2"></div>
                        <div class="column is-8">
                            <a @click="uploadmultipleimages()" class="button is-block is-primary">
                                View Reports
                            </a>
                        </div>
                        <div class="column is-2"></div>
                    </div>
                    <div class="columns detail">
                        <div class="column is-2"></div>
                        <div class="column is-8">    
                        <router-link :to="'/buyer/inivited/suppliers/'+auction.id+'/reverse/auction'" class="button is-block is-primary">
                            Invited Participants
                        </router-link>
                        </div>
                        <div class="column is-2"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="page__head">
            <span class="page__head--title">
                Items in this auction 
            </span>

            <div class="page__head--links">
                <a class="page__head--link button button-link" @click="addAuctionItem()">
                    Add Item
                </a>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__title">
                        <!-- Card Title Header -->
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search"/>
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :data="auction.auction_items" :columns="columns" :options="options">                    
                    <p slot="Item Name" slot-scope="{row}">
                        {{row.name}}
                    </p>

                    <p  slot="Reserve Price" slot-scope="{row}">
                        {{row.currency}} {{row.reserve_price}}
                    </p>
                    <p  slot="Best Bidder" slot-scope="{row}">
                        <span v-if="row.best_bidder != '' && row.best_bid_price > 0.00">
                        {{row.best_bidder}}
                        </span>
                        <span v-else>---</span>
                    </p>
                    <p  slot="Best Bid Price" slot-scope="{row}">
                        <span v-if="row.best_bid_price > 0">
                            {{row.currency}} {{row.best_bid_price}}
                        </span>
                        <span v-else>{{row.best_bid_price}}</span>
                    </p>
                    <span slot="Actions" slot-scope="{row}">
                        <div class="dropdown" :id="'row_'+row.id">
                            <div class="dropdown-trigger">
                                <button class="button is-primary is-small" @click="show_item_options(row)" aria-haspopup="true"
                                    aria-controls="dropdown-menu3">
                                    <span> Actions <font-awesome-icon class="view__icon" icon="angle-down"/></span>
                                    <span class="icon is-small"><i class="angle-down" aria-hidden="true"></i></span>
                                </button>
                            </div>
                            <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                                <div class="dropdown-content">
                                    <template v-if="auction.is_open === false && row.has_bidding_activity === false">
                                        <a class="dropdown-item" style="margin-right: 2px;">
                                            <span><font-awesome-icon class="view__icon" icon="trash-alt"/> Delete</span>
                                        </a>
                                        <hr class="dropdown-divider">
                                    </template>
                                    <template v-if="auction.is_open === false">
                                        <router-link :to="'/buyer/reverse/'+auction.id+'/'+row.id+'/auction/edit/item'" class="dropdown-item" style="margin-right: 2px;">
                                            <span><font-awesome-icon class="view__icon" icon="pencil-alt" /> Edit</span>
                                        </router-link>
                                        <hr class="dropdown-divider">
                                    </template>
                                    <a @click="onRowClick(row)" class="dropdown-item">
                                        <font-awesome-icon class="view__icon" icon="eye"/>
                                        View
                                    </a>
                                </div>
                            </div>
                        </div>
                    </span>
                </v-client-table>
                <div class="page__pagination">
                    <pagination style="padding: 0 20px !important" :records="auction.auction_items.length" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                    </pagination>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import auctions from '@/services/company/auction'
import moment from 'moment'


export default {
    name: 'reverse-auction-details-buyer',
    data () {
        return{
            columns: ['Item Name', 'Reserve Price', 'Best Bidder', 'Best Bid Price', 'Actions'],
            options: {
                headings : {

                },
                sortable:['#','Category Name', 'Bid Fee', 'Category Type', 'Status', 'Actions', 'More Actions'],
                sortIcon: {
                    is: "glyphicon-sort",
                    base: "glyphicon",
                    up: "glyphicon-chevron-up",
                    down: "glyphicon-chevron-down"
                },
            },
            page: 1,
            dataPerPage: 10,
            auction: {
                "id": '',
                "name": '',
                "auction_type": '',
                "opening_date": '',
                "closing_date": '',
                "closed_auction": '',
                "category_type": '',
                "overtine_count": '',
                "overtime_duration": '',
                "is_open": '',
                "created_by": '',
                "created_at": '',
                "auction_items":[]
            },
            excel_template: null,
            error_text: '',
            ExcelfileNames: [],
            SupportingfileNames: [],
            ExceluploadedFiles: [],
            SupportinguploadedFiles: [],
        }
    },
    filters: {
        moment: function (date) {
            return moment(date).format('MMMM Do YYYY, h:mm:ss a');
        }
    },
    mounted() {
        this.getReverse()
    },
    computed:{
        status(){
            return this.auction ? 'Open': 'Closed'
        },
        // Return the computed list per page
        displayedRecords(){
            const startIndex = this.dataPerPage * (this.page - 1);
            const endIndex = startIndex + this.dataPerPage;
            return this.auction.auction_items.slice(startIndex, endIndex);
        }
    },
    methods:{
        show_item_options(row) {
            let element = document.getElementById('row_' + row.id)
            if (element.classList.contains('is-active')) {
                element.classList.remove('is-active')
            } else {
                element.classList.add('is-active')
            }
        },
        addAuctionItem: function(){
            this.$router.push('/buyer/reverse/'+this.$route.params.auctionId+'/auction/add/item')
        },
        async onRowClick(actitm) {
            this.$router.push('/buyer/item/'+ this.$route.params.auctionId +'/'+ actitm.id +'/reverse/auction')
        },
        async getReverse(){
            try{
                const response = await auctions.getRetrieveAuction(this.$route.params.auctionId)
                console.log(response.data)
                console.log('Fecthed Items !')
                this.auction = response.data
            }catch(err){
                console.log(err)
            }
        },
        async downloadExcelTemplate(){
            try{
                let response = await auctions.auctionDownloadItemTemplate(this.$route.params.auctionId)
                console.log(response)
                if(response.status === 200){
                window.toast.fire({icon: 'success', title: "File download initiated"})
                this.$router.push(`/company/auction/download/progress/${response.data['task_id']}`)
                }else{
                window.toast.fire({icon: 'error', title: "Report generation error"})
                }
            }catch (err){
                window.toast.fire({icon: 'error', title: err})
            }
        },
        async selectExcelDocument(event){
            console.log('Button clicked')
            let fieldName = event.target.name;
            let fileList =  event.target.files;

            if (!fileList.length) return;            
            this.excel_template = event.target.files[0]
            
            const fd = new FormData()
            Array
            .from(Array(fileList.length).keys())
            .map(x => {
                fd.append(fieldName, fileList[x], fileList[x].name);
            });

            Array
            .from(Array(fileList.length).keys())
            .map(x => {
                this.ExcelfileNames.push(fileList[x].name);
            });

            // For submission
            let f = fileList[0]
            let form_data = new FormData()
            form_data.append('excel_file', f, f.name)
            
            try{
                let response = await auctions.upload_aution_items(this.$route.params.auctionId, form_data)
                if(response.status === 200){
                    window.toast.fire({icon: 'success', title: response.data['response_message']})
                    this.$router.push(`/company/auction/download/progress/${response.data['task_id']}`)
                }else{
                    window.toast.fire({icon: 'error', title: response.data['response_message']})
                }
            }catch (err){
                window.toast.fire({icon: 'error', title: err})
            }

            console.log(this.ExcelfileNames)
            console.log(this.excel_template)

        },
        removeexcelfile(){
            this.excel_template = null
            this.ExcelfileNames = []
        },
        callback: function(page) {
            // no need for callback here since you have all your data loaded already
            console.log(page)
        },
        async uploadmultipleimages(){
            this.$router.push('/uploadmultiple')
        }
    }
}
</script>

<style lang="scss" scoped>
@include page;

.page{
    &__content{
        width: 100%;
        // padding: $line-height $line-height;

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
                margin-bottom: $line-height*2;

                .detail {
                    border-bottom: 0;
                    padding: 0;

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
                        width: 70%;
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
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;

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
                .is-primary {
                    background-color: #073A82 !important;
                    &:hover, :focus {
                        box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                        transform: translateY(-0.25em);
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
    }
    .link_3{
        color: $color-lightblue-text;
        font-weight: 500;
        cursor: pointer;
        font-size: $font-size-text;
    }
}
.top_content{
  display: flex; justify-content: space-between; align-items: center;
}
hr {
  margin: 0.5rem 0 !important;
}
.column-details-height-custom{
    height: 24vh;
}
// DropDown css
.dropdown-content {
    position: relative !important;
}
.dropdown-item {
    padding: 0.1rem 1rem;
    font-size: 12px;
}
.dropdown-item svg:not(:root).svg-inline--fa {
    overflow: visible;
    color: green;
}
.is-primary{
    background-color: $color-blue-main !important;
}
</style>