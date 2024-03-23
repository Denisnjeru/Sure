<template>
 <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Score Calculation Progress
            </span>

            <div class="page__head--links">
            </div>
        </div>
        <div class="page__content columns">
            <div class="column is-12 column-page" style="padding: 12px 24px; align-items: initial">
              <div class="table-search">
                    <p class="table-search__instruction">
                      Progress
                    </p>
                    <div class="table-search__search">
<!--                        <font-awesome-icon class="table-search__search&#45;&#45;icon" icon="search" />-->
<!--                        <input @keyup.enter="search()" class="table-search__search&#45;&#45;input" type="text" placeholder="Search here">-->
                    </div>
                </div>

<!--              <div class="column-details">-->
                <div class='progress-wrapper'>
                  <div id='progress-bar' class='progress is-primary'
                      style="background-color: #68a9ef; width: 0%;">&nbsp;</div>
                </div>
                <div id="progress-bar-message">Waiting for progress to start...</div>
                <div id="celery-result"></div>
              </div>
<!--            </div>-->
        </div>
  </div>
</template>

<script>
import $ from "jquery";
import CeleryProgressBar from "@/utils/celery_progress";

export default {
  name: "RefreshScoresProgress",
  data() {
    return {
      task_id: null
    }
  },
  methods: {
    get_task_progress(task_id) {
      var progressUrl = process.env.VUE_APP_DOWNLOAD_URL + "celery-progress/" + task_id + "/";
      let self = this
      function customResult(resultElement, result) {
        $(resultElement).append(
            $('<p>').text(result['messages']),
        );
        $(resultElement).append(
            $('<p>').text(result['response_message']),
        );
        if (result['response_message'] === 'Score calculation complete') {
          window.toast.fire({icon: 'success', title: result['response_message']})
          self.$router.push(`/qed/prequalification/category/details/${self.$route.params.prequal_id}/${self.$route.params.category_id}`
          )
        }
      }

      $(function () {
        CeleryProgressBar.initProgressBar(progressUrl, {
          onResult: customResult,
          pollInterval: 2000
        })
      });
    }
  },
  mounted() {
    this.task_id = this.$route.params.task_id
    this.get_task_progress(this.task_id)
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
.dropdown-content{
  position: fixed !important;
}
.page .table-search{
    padding: 6px 0px;
    padding-bottom: 12px;
}
</style>