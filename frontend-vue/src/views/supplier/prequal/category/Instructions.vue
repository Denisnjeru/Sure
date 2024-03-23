<template>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Pre-qualification Details
            </span>

            <div class="page__head--links">
<!--                    <router-link to="/company/create/prequalification" class="button is-primary">-->
<!--                        New Prequalification-->
<!--                    </router-link>-->
            </div>
        </div>
        <div class="page__content columns top-content">
            <div class="column-details column is-12" style="padding: 20px;">
                <div class="table-search" style="font-size: 12px;">
                    <p class="table-search__instruction">
                      Prequalification Details
                    </p>
<!--                    <div class="table-search__search">-->
<!--                        <font-awesome-icon class="table-search__search--icon" icon="search" />-->
<!--                        <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">-->
<!--                    </div>-->
                </div>

              <div class="columns" style="padding: 6px 24px;">
                <div class="column is-6" style="font-size: 12px">
                  <span class="page__head--title" style="font-size: 12px"><strong>Job Title: </strong>{{ category.prequalification.title }}</span><br/>
<!--                  <hr style="margin: 1rem 0;">-->
                  <span class="page__head--title" style="font-size: 12px"><strong>Opening Date: </strong>{{ category.opening_date }}</span><br/>
<!--                  <hr style="margin: 1rem 0;">-->
                  <span class="page__head--title" style="font-size: 12px"><strong>Download Supporting Documents Below: </strong></span><br/>
                </div>

                <div class="column is-6">
                  <span class="page__head--title" style="font-size: 12px"><strong>Category Name: </strong>{{ category.name }}</span><br/>
<!--                  <hr style="margin: 1rem 0;">-->
                  <span class="page__head--title" style="font-size: 12px"><strong>Closing Date: </strong>{{ category.closing_date }}</span><br/>
<!--                  <hr style="margin: 1rem 0;">-->
                </div>
              </div>

              <div class="columns" style="padding: 0px 20px">
                <div class="column is-12">
                  <span class="page__head--title" style="font-size: 12px"><strong>Participation Status/Progress {{ progress }}%</strong></span>
                  <template>
                    <progress class="progress" :value="progress" :max="total">{{ progress }}%</progress>
<!--                    <span class="page__head&#45;&#45;title"><strong></strong></span>-->
                  </template>
                </div>
              </div>

              <template v-if="category.participated === true">
                <router-link style="font-size: 12px" class="button is-primary is-pulled-right"
                             :to="'/supplier/prequal/category/bid/'+category.id">
                  <span><font-awesome-icon class="view__icon" icon="pencil-alt" /> Update</span>
                </router-link>
              </template>
              <template v-else-if="category.participated === false">
                <router-link style="font-size: 12px" class="button is-primary is-pulled-right"
                             :to="'/supplier/prequal/category/bid/'+category.id">
                  <span>Bid</span>
                </router-link>
              </template>
            </div>
        </div>
</div>
</template>

<script>
import prequal from "@/services/supplier/prequal";
export default {
  name: "Instructions",
  data(){
    return{
      category: "",
      progress: 0,
      total: 0,
    }
  },
  methods:{
    async getPrequal(){
      try{
        let response = await prequal.category_instructions(this.$route.params.category_id)
        this.category = response.data
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async getParticipationProgress(){
      try{
        let response = await prequal.participation_progress(this.$route.params.category_id)
        if (response.status === 200){
          this.progress = response.data['progress']
          this.total = response.data['total']
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Please Try Again'})
        }
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    }
  },
  mounted() {
    this.getPrequal()
    this.getParticipationProgress()
  },
  created() {

  }
}
</script>

<style lang="scss" scoped>
@include page;

.page__content {
    margin: 0 !important;
    @include grid_column;
}
.is-primary{
  background-color: #073A82 !important;
}
.VueTables__table tbody td {
    padding: 5px 24px;
}
</style>