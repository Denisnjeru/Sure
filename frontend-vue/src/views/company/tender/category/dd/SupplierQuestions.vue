<template>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Due Diligence > {{ participant.supplier.company_name }} > Questions
            </span>

            <div class="page__head--links">
                    <router-link :to="'/company/tender/dd/add/supplier/questions/'+$route.params.category_id+'/'+$route.params.participant_id" class="button is-primary">
                        New Due Diligence Question
                    </router-link>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                      Due Diligence
                    </p>
                    <div class="table-search__search">
<!--                        <font-awesome-icon class="table-search__search&#45;&#45;icon" icon="search" />-->
<!--                        <input @keyup.enter="search()" class="table-search__search&#45;&#45;input" type="text" placeholder="Search here">-->
                    </div>
                </div>

              <v-client-table :columns="columns" :options="options" :data="questions">
                <span slot="Question" slot-scope="{row}">
                    <span> {{ row.question }}</span>
                </span>

                <span slot="Response" slot-scope="{row}">
                    <span> {{ row.due_diligence_response }}</span>
                </span>

                <span slot="Actions" slot-scope="{row}">
                  <router-link :to="'/company/tender/dd/conduct/'+$route.params.category_id+'/'+$route.params.participant_id+'/'+row.id" class="button is-primary is-small">
                    <p><font-awesome-icon class="view__icon" icon="pencil-alt"></font-awesome-icon> Update Response</p>
                  </router-link>
                </span>
              </v-client-table>

            </div>
            <div class="page__pagination">
                <pagination :records="dataCount" v-model="page" :per-page="dataPerPage" @paginate="fetchData()">
                </pagination>
            </div>
        </div>
    </div>
</template>

<script>
import tender from "@/services/company/tender";

export default {
  name: "SupplierQuestions",
  components:{
  },
  data () {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Question', 'Response', 'Actions'],
      options: {
        sortable: ['Question',],
        perPageValues: [20],
        filterable: false,
      },
      questions: [],
      participant: [],
    }
  },
  methods: {
    async search() {
      console.log('search');
    },
    async fetchData() {
        console.log('this.page');
    },
    // async get_participant(){
    //   try{
    //     let response = await tender.supplier(
    //         this.$route.params.category_id, this.$route.params.participant_id
    //     )
    //     this.questions = response.data['data']
    //     this.dataCount = response.data['count']
    //     this.dataPerPage = response.data['count']
    //   }catch (err){
    //     window.toast.fire({icon: 'error', title: err})
    //   }
    // },
    async get_participant_questions(){
      try{
        let response = await tender.dd_participant_questions(
            this.$route.params.category_id, this.$route.params.participant_id
        )
        this.questions = response.data['questions']
        this.participant = response.data['participant']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    // this.get_participant()
    this.get_participant_questions()
  }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
    margin: 0 !important;
    @include grid_column;
}
.VueTables__table tbody td {
    padding: 5px 24px;
}
.is-primary{
  background-color: #073A82 !important;
}
</style>