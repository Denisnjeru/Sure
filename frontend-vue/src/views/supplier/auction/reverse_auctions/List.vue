<template>
    <div class="risk">
        <div class="page__head">
            <span class="page__head--title">
                Reverse Auctions
            </span>

            <div class="page__head--links">
                <router-link to="/buyer/add/job/risk-management">
                    <a class="page__head--link button button-link">
                        My Bids
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
                    <p class="link" slot="Title" slot-scope="{row}">
                        {{row.name}}
                    </p>
                    <p class="link_3" slot="Company" slot-scope="{row}">
                        {{row.company}}
                    </p>
                    <p class="link_3" slot="Items" slot-scope="{row}">
                        {{row.items}}
                    </p>
                    <p class="link_3" slot="Opening Date" slot-scope="{row}">
                        {{row.opening_date | moment }}
                    </p>
                    <p class="link_3" slot="Closing Date" slot-scope="{row}">
                        {{row.closing_date | moment }}
                    </p>
                    <p  class="link_3" slot="Status" slot-scope="{row}">
                        <span v-if="row.is_open">Live</span >
                        <span v-else>Closed</span>
                    </p>
                    <span class="Actions" slot="Actions" slot-scope="{row}">
                        <span @click="onRowClick(row)" class="actions__select">
                            <font-awesome-icon icon="eye"/> &nbsp;View
                        </span>
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination">
                <pagination :records="reverse_auctions.length" v-model="page" :per-page="dataPerPage" @paginate="callback">
                </pagination>
            </div>
        </div>
    </div>
</template>

<script>
import auctions from '../../../../services/supplier/auction'
import moment from 'moment'

export default {
    name: 'reverse-auction-list-supplier',
    data () {
        return{
            columns: ['Title', 'Company', 'Items', 'Opening Date', 'Closing Date', 'Status', 'Actions'],
            reverse_auctions: [],
            options: {
                headings : {

                },
                editableColumns:['Title', 'Company', 'Items', 'Opening Date', 'Closing Date', 'Status'],
                sortable:['Auction Title', 'Company', 'Items', 'Opening Date', 'Closing Date', 'Status'],
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
        this.getReverseAuctions()
    },
    computed: {
        // Return the computed list per page
        displayedRecords(){
            const startIndex = this.dataPerPage * (this.page - 1);
            const endIndex = startIndex + this.dataPerPage;
            return this.reverse_auctions.slice(startIndex, endIndex);
        }
    },
    methods:{
        async onRowClick(act) {
            this.$router.push('/supplier/'+ act.id +'/reverse/auction')
        },
        async getReverseAuctions(){
            try{
                const response = await auctions.supplierReverseAuctions()
                console.log(response.data)
                this.reverse_auctions = response.data.results
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
    &__head {
        @include grid_row;
        align-items: center;
        width: 100%;
        padding: $line-height/3 $line-height;
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
}
</style>