<template>
    <div class="foward_auction">
        <div class="page__head">
            <span class="page__head--title">
                Foward Auctions
            </span>

            <div class="page__head--links">
                <router-link to="/buyer/add/foward/auction">
                    <a class="page__head--link button button-link">
                        New Foward Auction
                    </a>
                </router-link>
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
                <v-client-table :data="displayedRecords" :columns="columns" :options="options">
                    <p slot="Title" slot-scope="{row}">
                        {{row.name}}
                    </p>
                    <p slot="Items" slot-scope="{row}">
                        {{row.items}}
                    </p>
                    <p slot="Opening Date" slot-scope="{row}">
                        {{row.opening_date | moment }}
                    </p>
                    <p slot="Closing Date" slot-scope="{row}">
                        {{row.closing_date | moment }}
                    </p>
                    <p slot="Status" slot-scope="{row}">
                        <span v-if="row.is_open">Open</span >
                        <span v-else>Closed</span>
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
                                    <template v-if="row.is_open === false && row.has_bidding_activity === false">
                                        <a class="dropdown-item" style="margin-right: 2px;">
                                            <span><font-awesome-icon class="view__icon" icon="trash-alt"/> Delete</span>
                                        </a>
                                        <hr class="dropdown-divider">
                                    </template>
                                    <template v-if="row.is_open === false">
                                        <router-link :to="'/buyer/edit/'+row.id+'/foward/auction'" class="dropdown-item" style="margin-right: 2px;">
                                            <span><font-awesome-icon class="view__icon" icon="pencil-alt" /> Edit</span>
                                        </router-link>
                                        <hr class="dropdown-divider">
                                    </template>
                                    <a @click="onRowClick(row)" class="dropdown-item">
                                        <font-awesome-icon class="view__icon" icon="eye"/>
                                        Items
                                    </a>
                                </div>
                            </div>
                        </div>
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination">
                    <pagination :records="foward_auctions.length" v-model="page" :per-page="dataPerPage" @paginate="callback">
                    </pagination>
            </div>
        </div>
    </div>
</template>

<script>
import auctions from '../../../../services/company/auction'
import moment from 'moment'

export default {
    name: 'foward-auction-list-buyer',
    data () {
        return{
            columns: ['Title', 'Items', 'Opening Date', 'Closing Date', 'Status', 'Actions'],
            foward_auctions: [],
            options: {
                headings : {

                },
                editableColumns:['#', 'Title', 'Items', 'Opening Time', 'Closing Time', 'Status'],
                sortable:['Job Title', 'Job Code', 'status', ''],
                sortIcon: {
                    is: "glyphicon-sort",
                    base: "glyphicon",
                    up: "glyphicon-chevron-up",
                    down: "glyphicon-chevron-down"
                },
            },
            page: 1,
            dataPerPage: 20,
        }
    },
    filters: {
        moment: function (date) {
            return moment(date).format('MMMM Do YYYY, h:mm:ss a');
        }
    },
    mounted(){
    },
    created(){
        this.getFowardAuctions()
    },
    computed: {
        // Return the computed list per page
        displayedRecords(){
            const startIndex = this.dataPerPage * (this.page - 1);
            const endIndex = startIndex + this.dataPerPage;
            return this.foward_auctions.slice(startIndex, endIndex);
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
        async onRowClick(auc) {
            this.$router.push('/buyer/'+ auc.id +'/foward/auction')
        },
        async getFowardAuctions(){
            try{
                const response = await auctions.fowardAuctions()
                console.log(response.data)
                this.foward_auctions = response.data.data
            } catch(error){
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
    &__head {
        @include grid_row;
        align-items: center;
        width: 100%;
        padding: $line-height/3 $line-height;
        
        &--title {
            font-size: 25px;
            color: rgba(18, 31, 62, 0.8);
            font-weight: 600;
        }

    }
    &__content{
        margin: 0 !important;
        @include grid_column;
        width: 100%;
        padding: $line-height $line-height;
    }

    .row-link{
        text-align: center;
        
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
    .link_3{
        color: $color-lightblue-text;
        font-weight: 500;
        cursor: pointer;
        font-size: $font-size-text;
    }
    
    // DropDown css
    .dropdown-content {
      position: fixed !important;
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
}
</style>