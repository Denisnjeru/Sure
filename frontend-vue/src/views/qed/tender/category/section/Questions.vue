<template>
  <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               List of Questions
            </span>

            <div class="page__head--links">
                    <router-link :to="'/qed/tender/create/question/'+$route.params.section_id" class="button is-primary">
                        New Question
                    </router-link>
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page">
                <div class="table-search">
                    <p class="table-search__instruction">
                      Prequalification Category Questions
                    </p>
                    <div class="table-search__search">
                        <font-awesome-icon class="table-search__search--icon" icon="search" />
                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                    </div>
                </div>

              <v-client-table :columns="columns" :options="options" :data="questions">
                <span slot="Question" slot-scope="{row}">
                    <span> {{ row.description|truncate(50) }} ....</span>
                </span>

                <span slot="Type" slot-scope="{row}">
                    <span> {{ row.answer_type }}</span>
                </span>

                <span slot="Must" slot-scope="{row}">
                  <p v-if="row.is_required === true"><font-awesome-icon class="view__icon" icon="check"></font-awesome-icon></p>
                </span>

                <span slot="Scored" slot-scope="{row}">
                  <p v-if="row.is_scored === true"><font-awesome-icon class="view__icon" icon="check"></font-awesome-icon></p>
                </span>

                <span slot="Max" slot-scope="{row}">
                    <span> {{ row.max_score }}</span>
                </span>

                <span slot="QA" slot-scope="{row}">
                  <p v-if="row.is_qa === true"><font-awesome-icon class="view__icon" icon="check"></font-awesome-icon></p>
                </span>

                <span slot="Actions" slot-scope="{row}">
                  <router-link :to="'/qed/tender/edit/question/'+$route.params.section_id+'/'+row.id" class="button is-primary is-small">
                    <p><font-awesome-icon class="view__icon" icon="pencil-alt"></font-awesome-icon> Edit</p>
                  </router-link>

                  <a href="#" class="button is-success is-small"
                               style="margin-left: 2px" @click="zipFiles(row.id)">
                    <p><font-awesome-icon class="view__icon" icon="download"></font-awesome-icon> Zip Files</p>
                  </a>
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
import tender from "@/services/qed/tender";
export default {
  name: "PrequalQuestions",
  components:{
  },
  data () {
    return {
      page: 1,
      dataCount: 0,
      dataPerPage: 0,
      columns: ['Question', 'Type', 'Must', 'Scored', 'Max', 'QA', 'Actions'],
      options: {
        sortable: ['Question',],
        perPageValues: [20],
        filterable: false,
      },
      questions: []
    }
  },
  methods: {
    async zipFiles(question_id){
      try{
        let response = await tender.zip_files(question_id)
        window.toast.fire({icon: 'success', title: response.data['response_message']})
        this.$router.push(`/qed/tender/zip/files/progress/`+response.data['task_id']+'/'+this.$route.params.section_id)
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async search() {
        console.log('search');
    },
    async fetchData() {
        console.log('this.page');
    },
    async get_questions(){
      try{
        let response = await tender.questions(this.$route.params.section_id)
        this.questions = response.data['results']
        this.dataCount = response.data['count']
        this.dataPerPage = response.data['count']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.get_questions()
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