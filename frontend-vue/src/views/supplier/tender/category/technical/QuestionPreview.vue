<template>
  <div class="dashboard">
    <div class="page__head">
      <span class="page__head--title">
         Tender > Category > Question Preview
      </span>

      <div class="page__head--links">
        <!--        <router-link :to="'/supplier/prequal/preview/'+$route.params.category_id" class="button is-primary">-->
        <!--          Preview-->
        <!--        </router-link>-->
      </div>
    </div>

    <div class="columns" style="padding: 0px 30px">
      <div class="column is-12">
        <span class="page__head--title"><strong>Participation Status/Progress {{ progress }}%</strong></span>
        <template>
          <progress class="progress" :value="progress" :max="total">{{ progress }}%</progress>
        </template>
      </div>
    </div>


    <div class="page__content columns">

      <div class="column is-12 column-page" id="to_scroll_top"
           style="align-items: initial !important; padding: 12px 24px;!important;">
        <div class="table-search">
          <p class="table-search__instruction">
            Technical Envelope Preview
          </p>
          <div class="table-search__search">
            <!--                  <font-awesome-icon class="table-search__search&#45;&#45;icon" icon="search"/>-->
            <!--                  <input @keyup.enter="search()" class="table-search__search&#45;&#45;input" type="text" placeholder="Search here">-->
          </div>

        </div>
        <br>

        <div v-for="section in sections" v-bind:key="section.id">
          <template v-if="section.name !== 'Financial Ratios'">
            <article class="message">
              <a :href="'#collapsible-message-'+section.id">
                <div class="message-header">
                  <p>{{ section.name }}</p>
                </div>
              </a>

              <div :id="'collapsible-message-'+section.id" class="message-body is-collapsible"
                   data-parent="accordion_second" data-allow-multiple="true">
                <div class="message-body-content">
                  <form>
                    <div class="columns">
                      <div class="column content is-12">
                        <div class="field" v-for="question in section.questions" v-bind:key="question.id">
                          <label><strong>{{ question.description }}</strong></label>
                          <template v-if="question.answer_type === 1">
                            <ul>
                              <li v-if="question.response.options !== null">Response: {{
                                  question.response.options
                                }}
                              </li>
                              <li v-else>Response: No response submitted</li>
                            </ul>
                          </template>

                          <template v-else-if="question.answer_type === 2">
                            <ul>
                              <li v-if="question.response.options !== null">Response: {{
                                  question.response.options
                                }}
                              </li>
                              <li v-else>Response: No response submitted</li>
                            </ul>
                          </template>

                          <template v-else-if="question.answer_type === 3">
                            <ul>
                              <li v-if="question.response.options !== null">Response: {{
                                  question.response.options
                                }}
                              </li>
                              <li v-else>Response: No response submitted</li>
                            </ul>
                          </template>

                          <template v-else-if="question.answer_type === 4">
                            <ul>
                              <li v-if="question.response.options !== null">Response: {{
                                  question.response.options
                                }}
                              </li>
                              <li v-else>Response: No response submitted</li>
                            </ul>
                          </template>

                          <template v-else-if="question.answer_type === 5">
                            <ul>
                              <li v-if="question.response.document_url !== null">Response:
                                {{ question.response.document_url }}
                              </li>
                              <li v-else>Response: No response submitted</li>
                            </ul>
                          </template>

                          <template v-else-if="question.answer_type===6">
                            <ul>
                              <li v-if="question.response.options !== null">Response: {{
                                  question.response.options
                                }}
                              </li>
                              <li v-else>Response: No response submitted</li>
                            </ul>
                          </template>

                          <template v-else-if="question.answer_type===7">
                            <ul>
                              <li v-if="question.response.options !== null">Response: {{
                                  question.response.options
                                }}
                              </li>
                              <li v-else>Response: No response submitted</li>
                            </ul>
                          </template>

                          <template v-else-if="question.answer_type===8">
                            <ul>
                              <li v-if="question.response.options !== null">Response: {{
                                  question.response.options
                                }}
                              </li>
                              <li v-else>Response: No response submitted</li>
                            </ul>
                          </template>

                        </div>

                        <!--                          <div class="field">-->
                        <!--                            <button type="button" class="button is-primary is-small is-pulled-right" >Save</button>-->
                        <!--                          </div>-->
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            </article>
            <br>
          </template>

          <template>
            <template v-if="section.name === 'Financial Ratios'">
              <article class="message">
                <a :href="'#collapsible-message-'+section.id">
                  <div class="message-header">
                    <p>{{ section.name }}</p>
                  </div>
                </a>

                <div :id="'collapsible-message-'+section.id" class="message-body is-collapsible"
                     data-parent="accordion_second" data-allow-multiple="true">
                  <div class="message-body-content">
                    <form>
                      <div class="columns">
                        <div class="column content is-12">
                          <table class="table is-fullwidth">
                            <thead>
                            <tr>
                              <th>Description</th>
                              <th>Value</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr>
                              <th><label class="label">Equity</label></th>
                              <th>
                                <div class="field">
                                  <div class="control">
                                    <input class="input is-small" type="number" step="any" style="text-align: right;"
                                           :value="section.financial_ratios.equity"
                                           disabled readonly>
                                  </div>
                                </div>
                              </th>
                            </tr>
                            <tr>
                              <th><label class="label">Current Liabilities</label></th>
                              <th>
                                <div class="field">
                                  <div class="control">
                                    <input class="input is-small" type="number" step="any" style="text-align: right;"
                                           :value="section.financial_ratios.curr_liabilities" readonly disabled>
                                  </div>
                                </div>
                              </th>
                            </tr>
                            <tr>
                              <th><label class="label">Fixed Assets</label></th>
                              <th>
                                <div class="field">
                                  <div class="control">
                                    <input class="input is-small" type="number" step="any" style="text-align: right;"
                                           :value="section.financial_ratios.fixed_assets" readonly disabled>
                                  </div>
                                </div>
                              </th>
                            </tr>
                            <tr>
                              <th><label class="label">Current Assets</label></th>
                              <th>
                                <div class="field">
                                  <div class="control">
                                    <input class="input is-small" type="number" step="any" style="text-align: right;"
                                           :value="section.financial_ratios.current_assets" readonly disabled>
                                  </div>
                                </div>
                              </th>
                            </tr>
                            <tr>
                              <th><label class="label">Long Term Loans(Debt)</label></th>
                              <th>
                                <div class="field">
                                  <div class="control">
                                    <input class="input is-small" type="number" step="any" style="text-align: right;"
                                           :value="section.financial_ratios.debtors" readonly disabled>
                                  </div>
                                </div>
                              </th>
                            </tr>
                            <tr>
                              <th><label class="label">Cash</label></th>
                              <th>
                                <div class="field">
                                  <div class="control">
                                    <input class="input is-small" type="number" step="any" style="text-align: right;"
                                           :value="section.financial_ratios.cash" readonly disabled>
                                  </div>
                                </div>
                              </th>
                            </tr>
                            <tr>
                              <th><label class="label">Turnover</label></th>
                              <th>
                                <div class="field">
                                  <div class="control">
                                    <input class="input is-small" type="number" step="any" style="text-align: right;"
                                           :value="section.financial_ratios.turnover" readonly disabled>
                                  </div>
                                </div>
                              </th>
                            </tr>
                            <tr>
                              <th><label class="label">Gross Profit</label></th>
                              <th>
                                <div class="field">
                                  <div class="control">
                                    <input class="input is-small" type="number" step="any" style="text-align: right;"
                                           :value="section.financial_ratios.gross_profit" readonly disabled>
                                  </div>
                                </div>
                              </th>
                            </tr>
                            <tr>
                              <th><label class="label">Net Profit</label></th>
                              <th>
                                <div class="field">
                                  <div class="control">
                                    <input class="input is-small" type="number" step="any" style="text-align: right;"
                                           :value="section.financial_ratios.net_profit" readonly disabled>
                                  </div>
                                </div>
                              </th>
                            </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
              </article>
            </template>
          </template>
          <!--              <h4>{{ section.name }}</h4>-->

          <!--              <div v-for="question in section.questions" v-bind:key="question.id">-->
          <!--                <h5>{{ question.description }}</h5>-->
          <!--                <ul>-->
          <!--                  <li>Response: {{ question.response.options }}</li>-->
          <!--                </ul>-->
          <!--              </div>-->
        </div>


      </div>
    </div>
  </div>
</template>

<script>
import supplier_tender from "@/services/supplier/tender";

export default {
  name: "QuestionPreview",
  data() {
    return {
      sections: [],
      progress: 0,
      total: 0,
    }
  },
  methods: {
    async getSections() {
      try {
        let response = await supplier_tender.preview_sections(this.$route.params.category_id)
        if (response.status === 200) {
          this.sections = response.data
        } else {
          window.toast.fire({icon: 'error', title: 'Error, please try again'})
        }
      } catch (e) {
        window.toast.fire({icon: 'error', title: e})
      }
    },
    async getParticipationProgress() {
      try {
        let response = await supplier_tender.participation_progress(this.$route.params.category_id)
        if (response.status === 200) {
          this.progress = response.data['progress']
          this.total = response.data['total']
        } else {
          window.toast.fire({icon: 'error', title: 'Error. Please Try Again'})
        }
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    }
  },
  mounted() {
    this.getSections()
    this.getParticipationProgress()
  }
}
</script>

<style lang="scss" scoped>
@include page;
.page__content {
  margin: 0 !important;
  @include grid_column;
}

.is-primary {
  background-color: #073A82 !important;
}

.message-header {
  background-color: #073A82 !important;
}
</style>