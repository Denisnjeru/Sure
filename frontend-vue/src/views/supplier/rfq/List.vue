<template>
    <div class="risk">
        <div class="page__head">
            <span class="page__head--title">
                List of Request for Quotation Jobs
            </span>
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
                <v-client-table :data="rfqs" :columns="columns" :options="options">
                    <span slot="Buyer" slot-scope="{row}">
                        <span> {{ row.company_name }}</span>
                    </span>

                    <span slot="Job" slot-scope="{row}">
                        <span> {{ row.job }}</span>
                    </span>

                    <span slot="Category" slot-scope="{row}">
                        <span> {{ row.name }}</span>
                    </span>

                    <span slot="Category Code" slot-scope="{row}">
                        <span> {{ row.unique_reference }}</span>
                    </span>

                    <span slot="Closing Time" slot-scope="{row}">
                        <span> {{ row.closing_date }}</span>
                    </span>

                    <span class="actions" slot="Action" slot-scope="{row}" >
                        <template v-if="row.rfq_type == 'basic'">
                            <template v-if="row.supplier_participation_status">
                                <button @click="updateRfq(row)" class="button is-primary is-small">
                                <p><font-awesome-icon class="view__icon" icon="pencil-alt"></font-awesome-icon> Update</p>
                                </button>
                            </template>
                            <template v-else>
                                <button @click="applyRfq(row)" class="button is-primary is-small">
                                <p><font-awesome-icon class="view__icon" icon="pencil-alt"></font-awesome-icon> Bid</p>
                                </button>
                            </template>
                        </template>
                        <template v-else-if="row.rfq_type == 'advanced'">
                            
                            <router-link :to="'/supplier/apply/rfq/advanced/'+row.id" class="button is-primary is-small">
                                <p v-if="row.supplier_participation_status"><font-awesome-icon class="view__icon" icon="pencil-alt"></font-awesome-icon> Update</p>
                                <p v-else><font-awesome-icon class="view__icon" icon="pencil-alt"></font-awesome-icon> Bid</p>
                            </router-link>
                        </template>
                         
                    </span>
                    
                </v-client-table>
                <div class="page__pagination">
                    <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                    </pagination>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import supplierRfq from "@/services/supplier/rfq";

export default {
    name: 'supplierRFQList',
    data () {
        return{
            columns: ['Buyer', 'Job', 'Category', 'Category Code', 'Closing Time','Action'],
            options: {
                headings : {

                },
                sortable:['Job', 'Job Code', 'status', ''],
                sortIcon: {
                    is: "glyphicon-sort",
                    base: "glyphicon",
                    up: "glyphicon-chevron-up",
                    down: "glyphicon-chevron-down"
                },
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            rfqs:[],
            supplierParticipationStatus: false,
        }
    },
    computed: {
        ...mapGetters('Auth',['authUser', 'authStatus', 'authError']),
        ...mapGetters('User',['userData',]),
    },
    methods: {
        applyRfq(row){
            //Redirect to apply RFQ based on RFQ Type
            // Basic = 1
            // Advanced =2
            if(row.rfq_type === 2){
                this.$router.push(`/supplier/apply/rfq/advanced/${row.id}`)
            }else{
                this.$router.push(`/supplier/apply/rfq/${row.id}`)
            }
            
        },
        updateRfq(row){
            if(row.rfq_type === 2){
                this.$router.push(`/supplier/apply/rfq/advanced/${row.id}`)
            }
            else{
                this.$router.push(`/supplier/apply/rfq/${row.id}`)
            }
            
        },
        async fetchData(){
            console.log(this.page)
        },
        async search(){
            console.log('search')
        },
        async getSupplierRfqs(){
            try{
                let response = await supplierRfq.rfqs(this.page)
                this.rfqs = response.data['results']
                this.dataCount = response.data['count']
                this.dataPerPage = response.data['count']
                console.log(this.rfqs)
            }catch (err){
                window.toast.fire({icon: 'error', title: err})
            }
        },
    },
    mounted() {
        this.getSupplierRfqs()
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
            font-size:$font-size-title;
            color: rgba(18, 31, 62, 0.8);
            font-weight: 600;
        }

    }
    &__content{
        margin: 0 !important;
        @include grid_column;
        width: 100%;
        // padding: $line-height $line-height;
    }

    .row-link{
        color: rgba(18, 31, 62, 0.8);
        flex-flow: row nowrap;
        justify-content: space-evenly;
        
        &__text{
            text-decoration-line: underline;
        }
        &__arrow{
            display: inline;
            border-radius: 5px;
        }
    }
}
.VueTables__table tbody td {
    padding: 5px 24px;
}
.is-primary{
  background-color: #073A82 !important;
}
</style>