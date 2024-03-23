<template>
<div>

</div>
</template>

<script>
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
      var progressUrl = process.env.VUE_APP_DOWNLOAD_URL + "celery-progress/" + task_id;

      function customResult(resultElement, result) {
        // $( resultElement ).append(
        //     elements
        // );
        $(resultElement).append(
            $('<p>').text(result['messages']),
        );
        if (result['response_message'] === 'Report generated successfully') {
          $(resultElement).append(
              $('<a href="' + process.env.VUE_APP_DOWNLOAD_URL + result['filepath'] + '" class="btn btn-success">Download Report</a>')
          );
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

<style scoped>

</style>