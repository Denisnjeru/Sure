<template>
<div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
               Zip Files Progress
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
import $ from 'jquery'
import CeleryProgressBar from "@/utils/celery_progress";
export default {
  name: "ZipFilesProgress",
  data() {
    return {
      task_id: null
    }
  },
  methods: {
    get_task_progress(task_id) {
      var progressUrl = process.env.VUE_APP_DOWNLOAD_URL + "celery-progress/" + task_id + '/';

      function customResult(resultElement, result) {
        // $( resultElement ).append(
        //     elements
        // );
        $(resultElement).append(
            $('<p>').text(result['messages']),
        );
        if (result['response_message'] === 'File generated successfully') {
          window.toast.fire({icon: 'success', title: result['response_message']})
          $(resultElement).append(
              $('<a href="'+process.env.VUE_APP_DOWNLOAD_URL+result['filepath']+'" ' +
                  'class="button is-primary is-pulled-right" style="background-color: #073A82;" download="download">Download Report</a>'
              )
          );
        }
      }

      $(function () {
        CeleryProgressBar.initProgressBar(progressUrl, {
          onResult: customResult,
          pollInterval: 5000
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
.dropdown-content{
  position: fixed !important;
}
.page .table-search{
    padding: 6px 0px;
    padding-bottom: 12px;
}
</style>