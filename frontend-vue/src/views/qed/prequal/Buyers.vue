<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Prequal > Buyers
            </span>

            <div class="page__head--links">
               
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Select buyer company
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="buyers" :options="options" class="hasRowNo hasNoWrap">
                    <p class="row-no" v-if="buyers.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>
                    <span class="actions" slot="actions" slot-scope="{row}">
                        <span @click="selectBuyer(row)" class="actions__select">
                            Select
                        </span>
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination" v-if="buyers.length > 0">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getBuyers()">
                </pagination>
            </div>
        </div>     
    </div>
</template>

<script>
import buyer from '@/services/qed/buyer'

export default {
    name: 'QedDashboardJobsBuyers',
    data() {
        return {
            columns: ['#', 'company_name', 'buyer_initials', 'actions'],
            options: {
                sortable: ['company', 'job'],
                editableColumns:[],
                pagination: {show: true, dropdown: true},
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            buyers: [],
        }
    },
    components: {
        
    },
    computed: {

    },
    mounted() {
        this.getBuyers()
    },
    methods: {
        selectBuyer: function(buyer) {
            this.$store.dispatch('Qed/setSelectedBuyer', {buyer})
            this.$router.push('/qed/prequalifications')
        },
        async getBuyers() {
            try {
                const response = await buyer.buyers(this.page, this.dataPerPage)
                this.dataCount = response.data.count
                this.buyers = response.data.results
            } catch (err) {
                console.log(err)
            }
        },
        async search() {
            console.log('search');
        }
    }
}
</script>

<style lang="scss" scoped>
@include page;


.dashboard {
    position: relative;
}

.page__content {
    margin: 0 !important;
    @include grid_column;
}


.popup {
    position: absolute; 
    top: 0vh;
    width: 100%;
    height: 100%; 
    z-index: 90;
    // background-color: rgba(0, 0, 0, 0.2); 
    @include grid_row;
    align-items: flex-start;
    transition: opacity .3s;
    
    &__details {
        // position: sticky;
        // top: 20vh;
        min-height: 70vh;
        background-color: $color-white-main;
        $width: 97%;
        width: $width;
        margin: 0.5vh calc((100% - #{$width})/2);
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: $line-height/2;
        padding: $line-height $line-height/3;

        .page__content {
            padding-top: $line-height*2;
        }

        .column-page {
            box-shadow: none;
            padding: 0 $line-height;
            border-radius: 0;
            
            &:first-child {
                border-right: 1px solid $color-gray-medium;
            }
        }
    }
}

</style>
