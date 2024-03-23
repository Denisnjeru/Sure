<template>
<div class="dashboard">
    <div class="page__head">
      <span class="page__head--title">
         Letters > Prequalification Job > Due Diligence
      </span>

      <div class="page__head--links">

      </div>
    </div>

  <div class="page__content columns bottom_content">
      <div class="column is-12 column-page">
        <div class="table-search">
          <p class="table-search__instruction">
            Update Due Diligence Letter
          </p>
          <div class="table-search__search">
<!--            <font-awesome-icon class="table-search__search&#45;&#45;icon" icon="search"/>-->
<!--            <input @keyup.enter="search()" class="table-search__search&#45;&#45;input" type="text" placeholder="Search here">-->
          </div>
        </div>

        <div class="page__content">
          <div class="columns is-centered">
            <div class="column is-12">
              <form @submit.prevent="submitLetter()">
                <div class="field is-fullwidth">
                  <label>Signed Letter</label>
                  <div class="control">
                    <input type="file" class="input" @change="selectFile($event)" required>
                    <small><strong>Current: </strong><a download="download" target="_blank" :href="letter.file">Download</a></small>
                  </div>
                </div>

                <div class="field is-fullwidth">
                  <label>Subject</label>
                  <div class="control">
                    <input type="text" class="input" v-model="form.subject" required>
                  </div>
                </div>

                <div class="field is-fullwidth">
                  <label>Body</label>
                  <div class="control">
                    <editor v-model="form.body" />
<!--                    <textarea class="textarea" v-model="form.body" required></textarea>-->
                  </div>
                </div>

                <div class="columns">
                  <div class="column">
                    <div class="field is-fullwidth">
                      <label>Letter Header</label>
                      <div class="control">
                        <input type="file" class="input" @change="selectHeader($event)" required>
                        <small><strong>Current: </strong><a download target="_blank" :href="letter.header">Download</a></small>
                      </div>
                    </div>

                    <div class="field is-fullwidth">
                      <label>Letter Signature</label>
                      <div class="control">
                        <input type="file" class="input" @change="selectSignature($event)" required>
                        <small><strong>Current: </strong><a download target="_blank" :href="letter.signature">Download</a></small>
                      </div>
                    </div>

                    <div class="field is-fullwidth">
                      <label>Authorizer Name</label>
                      <div class="control">
                        <input type="text" class="input" v-model="form.authoriser_name" required>
                      </div>
                    </div>

                  </div>

                  <div class="column">
                    <div class="field is-fullwidth">
                      <label>Letter Footer</label>
                      <div class="control">
                        <input type="file" class="input" @change="selectFooter($event)" required>
                        <small><strong>Current: </strong><a download target="_blank" :href="letter.footer">Download</a></small>
                      </div>
                    </div>

                    <div class="field is-fullwidth">
                      <label>Letter Watermark</label>
                      <div class="control">
                        <input type="file" class="input" @change="selectWatermark($event)" required>
                        <small><strong>Current: </strong><a download target="_blank" :href="letter.watermark">Download</a></small>
                      </div>
                    </div>

                    <div class="field is-fullwidth">
                      <label>Authorizer Role</label>
                      <div class="control">
                        <input type="text" class="input" v-model="form.authoriser_role" required>
                      </div>
                    </div>

                  </div>
                </div>

                <div class="field is-fullwidth">
                  <button type="submit" class="button is-primary is-small">Update</button>
                </div>

              </form>
            </div>
          </div>
        </div>
      </div>
  </div>
</div>
</template>

<script>
import prequal from "@/services/qed/prequal";

export default {
  name: "EditAwardLetter",
  data(){
    return{
      form: {
        "header": "",
        "footer": "",
        "file": "",
        "signature": "",
        "watermark": "",
        "body": "",
        "subject": "",
        "authoriser_name": "",
        "authoriser_role": "",
      },
      letter: {}
    }
  },
  methods:{
    selectFile(event){
      this.form.file= event.target.files[0]
    },
    selectHeader(event){
      this.form.header = event.target.files[0]
    },
    selectSignature(event){
      this.form.signature = event.target.files[0]
    },
    selectWatermark(event){
      this.form.watermark = event.target.files[0]
    },
    selectFooter(event){
      this.form.footer = event.target.files[0]
    },
    async getLetter(){
      try{
        let response = await prequal.job_client_document(this.$route.params.job_id, 'custom')
        if (response.status === 200){
          this.letter = response.data
          this.form.authoriser_name = response.data['authoriser_name']
          this.form.authoriser_role = response.data['authoriser_role']
          this.form.body = response.data['body']
          this.form.body = response.data['subject']
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Please Try Again!!'})
        }
      }catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async submitLetter(){
      let form_data = new FormData();
      if (this.form.file) {
        form_data.append("file", this.form.file, this.form.file.name)
      }
      if (this.form.header) {
        form_data.append("header", this.form.header, this.form.header.name)
      }
      if (this.form.signature) {
        form_data.append("signature", this.form.signature, this.form.signature.name)
      }
      if (this.form.watermark) {
        form_data.append("watermark", this.form.watermark, this.form.watermark.name)
      }
      if (this.form.footer) {
        form_data.append("footer", this.form.footer, this.form.footer.name)
      }
      form_data.append("prequalification", this.$route.params.job_id)
      form_data.append("body", this.form.body)
      form_data.append("authoriser_name", this.form.authoriser_name)
      form_data.append("authoriser_role", this.form.authoriser_role)
      form_data.append("document_type", "dd")
      form_data.append("tendersure_module", "letters")

      try{
        let response = await prequal.update_client_document(form_data, this.$route.params.job_id, 'dd')
        if(response.status === 200){
          this.$router.push(`/qed/prequal/letters/${this.$route.params.job_id}`)
        }else{
          window.toast.fire({icon: 'error', title: 'Error. Please Try Again!'})
        }
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    }
  },
  mounted() {
    this.getLetter()
  }
}
</script>

<style lang="scss" scoped>
@include page;

//.page__content {
//  margin: 0 !important;
//  @include grid_column;
//}

.is-primary {
  background-color: #073A82 !important;
}
</style>