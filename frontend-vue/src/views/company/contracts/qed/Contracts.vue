<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                QED Contracts
            </span>

            <div class="page__head--links">
                <router-link to="/update-profile">
                    <a class="page__head--link button button-link">
                        Upload New Contract
                    </a>
                </router-link>
            </div>
        </div>
        <div class="page__content columns">           
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                       Uploaded Contracts (Current Contracts with QED)
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>
                <v-client-table :columns="columns" :data="contracts" :options="options" class="hasRowNo hasNoWrap">
                    <p class="row-no" v-if="contracts.length !== 0" slot="#" slot-scope="props">
                        {{props.index}}
                    </p>

                    <p slot="job_title" slot-scope="{row}">
                        {{row.target.title}}
                    </p>
                    <p class="capitalize" slot="approval" slot-scope="{row}">
                        {{row.approval_status}}
                    </p>
                    <p class="capitalize" slot="status" slot-scope="{row}">
                        {{row.status}}
                    </p>
                    <span class="view" slot="contract" slot-scope="{row}" @click="viewContract(row)">
                        <font-awesome-icon class="view__icon" icon="eye" />
                        <span> View Contract</span>
                    </span>
                    <span class="actions" slot="actions" slot-scope="{row}">
                        <router-link :to="'/buyer/contracts/qed/' + row.id + '/update'">
                            <span class="actions__edit">
                                <font-awesome-icon class="actions__icon" icon="pen-alt" />
                            </span>
                        </router-link>
                        <span class="actions__delete">
                            <font-awesome-icon class="actions__icon" icon="trash-alt" />
                        </span>
                    </span>
                </v-client-table>
            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="getContracts()">
                </pagination>
            </div>
        </div>
        <div class="extras">
            <div class="popup" v-if="popContractView === true && selectedContract.target !== undefined">
                <span class="popup__details">
                    <div class="page__head">
                        <span class="page__head--title">
                            <font-awesome-icon class="page__head--back" icon="arrow-left" @click="popupContractView()" />
                            QED contract for {{selectedContract.target.title}}
                        </span>

                        <div class="page__head--links">
                            <router-link :to="'/buyer/contracts/qed/' + selectedContract.id + '/update'">
                                <a class="page__head--link button button-link">
                                    <font-awesome-icon icon="pen-alt" /> &nbsp;
                                    Edit Contract
                                </a>
                            </router-link>
                        </div>
                    </div>
                    <div class="page__content columns">
                        <div class="column is-12">
                            <documentView :documentUrl="selectedContract.document" />
                        </div>
                    </div>
                </span>
            </div> 
        </div>       
    </div>
</template>

<script>
import contracts from '@/services/company/contracts'
import documentView from '@/components/contracts/DocumentView.vue'
import { mapGetters } from 'vuex'

export default {
    name: 'QedContracts',
    data() {
        return {
            columns: ['#', 'job_title', 'contract', 'status', 'approval', 'start_date', 'end_date', 'actions'],
            options: {
                sortable: ['company', 'job_title'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            contracts: [],
            popContractView: false,
            selectedContract: {}
        }
    },
    components: {
        documentView,
    },
    computed: {
        ...mapGetters('User',['userData',]),
    },
    mounted() {
        this.getContracts()
    },
    methods: {
        popupContractView: function() {            
            this.popContractView = !this.popContractView
            this.selectedContract = {}
        },
        viewContract: function(contract) {
            this.popupContractView()
            this.selectedContract = contract            
        },
        async getContracts() {
            try {
                const response = await contracts.qedContracts(this.userData.company_id)
                this.dataCount = response.data.count
                this.contracts = response.data.results
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
