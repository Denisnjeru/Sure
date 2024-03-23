<template>
<div class="dashboard">
    <div class="page__head">
            <span class="page__head--title">
               Job > Category > QualityAssurance > Participant
            </span>

      <div class="page__head--links">
        <!--                    <router-link to="/company/create/prequalification" class="button is-primary">-->
        <!--                        New Prequalification-->
        <!--                    </router-link>-->
      </div>
    </div>
    <div class="page__content columns">
          <div class="column is-12">
            <div class="tabs is-toggle is-fullwidth" >
              <ul>
                <li  :class="active_section.id === section.id ? 'is-active': '' " v-for="section in sections" v-bind:key="section.id" :id="'list_item_'+section.id">
                  <a type="button" @click="get_questions(section)" :id="'button_'+section.id">
                    <span class="icon is-small"><i class="fas fa-image" aria-hidden="true"></i></span>
                    <span>{{ section.name }}</span>
                  </a>
                </li>
              </ul>
            </div>

          </div>
        </div>

    <div class="page__content columns">

      <div class="column is-12 column-page" style="align-items: initial !important; padding: 12px 24px;!important;" id="to_scroll">
        <div class="table-search" style="padding: 0px 0px;!important;">
          <p class="table-search__instruction">
            Conduct Quality Assurance
          </p>
          <hr>
          <div class="table-search__search">
            <!--                        <font-awesome-icon class="table-search__search&#45;&#45;icon" icon="search" />-->
            <!--                        <input @keyup.enter="search()" class="table-search__search&#45;&#45;input" type="text" placeholder="Search here">-->
          </div>
        </div>

        <div class="columns" v-if="section_questions && active_section.name !== 'Financial Ratios' ">
          <div class="column is-12" style="padding: 16px 24px;">
            <div id="accordion_second">

              <article class="message" v-for="question in section_questions" v-bind:key="question.id">
                <a :href="'#collapsible-message-'+question.id">
                <div class="message-header">
                  <p>Question: {{ question.question.description }}</p>
                </div>
                </a>

                <div :id="'collapsible-message-'+question.id" class="message-body is-collapsible" data-parent="accordion_second" data-allow-multiple="true">
                  <div class="message-body-content">
                    <template v-if="question.question_type === 'tcc'">
                      <form >
                      <div class="columns">
                        <div class="column is-12">
                          <p><strong>Instructions: </strong> {{ question.verification_instruction }}</p>
                        </div>
                      </div>
                      <div class="columns">
                        <div class="column is-4">

                          <div class="field">
                            <label>Company Name</label>
                            <div class="control" v-if="question.qa_question_response.tcc">
                              <input type="text" class="input" :id="'company_name_'+question.id"
                                     v-model="question.qa_question_response.tcc.company_name"
                                     @focusout="submit_qa_response(question)">
                            </div>
                            <div class="control" v-else>
                              <input type="text" class="input" :id="'company_name_'+question.id"
                                     @focusout="submit_qa_response(question)">
                            </div>
                          </div>

                          <div class="field">
                            <label>PIN Number:</label>
                            <div class="control">
                              <input type="text" class="input" :id="'document_number_'+question.id" @focusout="submit_qa_response(question)" v-model="question.qa_question_response.number"/>
                              <small style="color: red;">Supplier Response : {{ question.question_type_response }}</small>
                            </div>
                          </div>
                          <div class="field">
                            <label>PIN Number OutCome</label>
                            <div class="control" v-if="question.qa_question_response.tcc">
                              <select class="input" v-model="question.qa_question_response.tcc.pin_number_outcome"
                                      @focusout="submit_qa_response(question)"
                                      :id="'pin_number_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
<!--                                <option value="Subjective">Subjective</option>-->
                              </select>
                            </div>
                            <div class="control" v-else>
                              <select class="input"
                                      @focusout="submit_qa_response(question)"
                                      :id="'pin_number_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
<!--                                <option value="Subjective">Subjective</option>-->
                              </select>
                            </div>
                          </div>

                          <div class="field">
                            <label>Expiry Date</label>
                            <div class="control">
                              <input type="date" class="input" @focusout="submit_qa_response(question)"
                                     :id="'document_date_'+question.id" v-model="question.qa_question_response.date"/>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>
                          <div class="field">
                            <label>Expiry Date OutCome</label>
                            <div class="control" v-if="question.qa_question_response.tcc">
                              <select class="input" v-model="question.qa_question_response.tcc.expiry_date_outcome"
                                      @focusout="submit_qa_response(question)"
                                      :id="'expiry_date_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
<!--                                <option value="Subjective">Subjective</option>-->
                              </select>
                            </div>
                            <div class="control" v-else>
                              <select class="input"
                                      @focusout="submit_qa_response(question)"
                                      :id="'expiry_date_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
<!--                                <option value="Subjective">Subjective</option>-->
                              </select>
                            </div>
                          </div>

                          <div class="field">
                            <label>Comment</label>
                            <div class="control">
                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question)" :id="'document_comment_'+question.id" v-model="question.qa_question_response.comment"></textarea>
                            </div>
                          </div>

                          <div class="field">
                            <label>OutCome</label>
                            <div class="control">
                              <select v-model="question.qa_question_response.outcome" class="input"
                                      @change="hide_show_qa_score_field($event, question)"
                                      :id="'document_outcome_'+question.id"
                                      required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                                <option value="Subjective">Subjective</option>
                              </select>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field" :id="'score_after_qa_field_'+question.id" :style="question.qa_question_response.outcome !== 'Subjective' ? 'display: none' : 'display: block'">
                            <label>Score after QA</label>
                            <input type="number" step="any" class="input" @focusout="submit_qa_response(question)" :id="'document_score_after_qa_'+question.id" v-model="question.qa_question_response.score_after_qa"/>
                          </div>

                          <div class="field">
                            <button type="button" class="button is-primary is-small is-pulled-right" @click="submit_qa_response(question)">Save</button>
                          </div>
                        </div>

                        <div class="column is-8">
                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">
                            <p>Your web browser doesn't have a PDF plugin.
                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>
                          </object>

<!--                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">-->
<!--                            <p>Your web browser doesn't have a PDF plugin.-->
<!--                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>-->
<!--                          </object>-->
<!--                          <iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url=https://media.readthedocs.org/pdf/django/2.2.x/django.pdf" type="application/pdf"-->
<!--                                  frameBorder="0" scrolling="auto" height="100%" width="100%" ></iframe>-->
                        </div>
                      </div>
                    </form>
                    </template>
                    <template v-else-if="question.question_type === 'bp'">
                      <form >
                      <div class="columns">
                        <div class="column is-12">
                          <p><strong>Instructions: </strong> {{ question.verification_instruction }}</p>
                        </div>
                      </div>
                      <div class="columns">

                        <div class="column is-4">
                          <div class="field">
                            <label>Business Name</label>
                            <div class="control">
                              <input type="text" class="input" :id="'business_name_'+question.id" @focusout="submit_qa_response(question)"
                                     v-model="question.qa_question_response.business_permit.business_name"/>
                              <small style="color: red">Supplier Response: {{ question.question_type_response }}</small>
                            </div>
                          </div>

                          <div class="field">
                            <label>Business Name OutCome</label>
                            <div class="control" v-if="question.qa_question_response.business_permit">
                              <select class="input" v-model="question.qa_question_response.business_permit.business_name_outcome"
                                      @focusout="submit_qa_response(question)"
                                      :id="'business_name_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                            <div class="control" v-else>
                              <select class="input"
                                      @focusout="submit_qa_response(question)"
                                      :id="'business_name_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                          </div>


                          <div class="field">
                            <label>Business Number</label>
                            <div class="control">
                              <input type="text" class="input" :id="'document_number_'+question.id" @focusout="submit_qa_response(question)"
                                     v-model="question.qa_question_response.number"/>
<!--                              <small style="color: red">Supplier Response: {{ question.question_type_response.registration_number }}</small>-->
                            </div>
                          </div>

                          <div class="field">
                            <label>Document Date</label>
                            <div class="control">
                              <input type="date" class="input" @focusout="submit_qa_response(question)" :id="'document_date_'+question.id" v-model="question.qa_question_response.date"/>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field">
                            <label>Comment</label>
                            <div class="control">
                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question)" :id="'document_comment_'+question.id" v-model="question.qa_question_response.comment"></textarea>
                            </div>
                          </div>

                          <div class="field">
                            <label>OutCome</label>
                            <div class="control">
                              <select v-model="question.qa_question_response.outcome" class="input"
                                      @change="hide_show_qa_score_field($event, question)"
                                      :id="'document_outcome_'+question.id"
                                      required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                                <option value="Subjective">Subjective</option>
                              </select>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field" :id="'score_after_qa_field_'+question.id" :style="question.qa_question_response.outcome !== 'Subjective' ? 'display: none' : 'display: block'">
                            <label>Score after QA</label>
                            <input type="number" step="any" class="input" @focusout="submit_qa_response(question)" :id="'document_score_after_qa_'+question.id" v-model="question.qa_question_response.score_after_qa"/>
                          </div>

                          <div class="field">
                            <button type="button" class="button is-primary is-small is-pulled-right" @click="submit_qa_response(question)">Save</button>
                          </div>
                        </div>

                        <div class="column is-8">
                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">
                            <p>Your web browser doesn't have a PDF plugin.
                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>
                          </object>

<!--                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">-->
<!--                            <p>Your web browser doesn't have a PDF plugin.-->
<!--                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>-->
<!--                          </object>-->
<!--                          <iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url=https://media.readthedocs.org/pdf/django/2.2.x/django.pdf" type="application/pdf"-->
<!--                                  frameBorder="0" scrolling="auto" height="100%" width="100%" ></iframe>-->
                        </div>
                      </div>
                    </form>
                    </template>
                    <template v-else-if="question.question_type === 'pin'">
                      <form >
                      <div class="columns">
                        <div class="column is-12">
                          <p><strong>Instructions: </strong> {{ question.verification_instruction }}</p>
                        </div>
                      </div>
                      <div class="columns">

                        <div class="column is-4">

                          <div class="field">
                            <label>Tax PIN Number</label>
                            <div class="control">
                              <input type="text" class="input" :id="'document_number_'+question.id" @focusout="submit_qa_response(question)"
                                     v-model="question.qa_question_response.number"/>
                              <small style="color: red">Supplier Response: {{ question.question_type_response }}</small>
                            </div>
                          </div>

                          <div class="field">
                            <label>Tax PIN OutCome</label>
                            <div class="control" v-if="question.qa_question_response.tax_pin">
                              <select class="input" v-model="question.qa_question_response.tax_pin.tax_pin_outcome"
                                      @focusout="submit_qa_response(question)"
                                      :id="'tax_pin_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                            <div class="control" v-else>
                              <select class="input"
                                      @focusout="submit_qa_response(question)"
                                      :id="'tax_pin_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                          </div>

                          <div class="field">
                            <label>Document Date</label>
                            <div class="control">
                              <input type="date" class="input" @focusout="submit_qa_response(question)" :id="'document_date_'+question.id" v-model="question.qa_question_response.date"/>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field">
                            <label>Comment</label>
                            <div class="control">
                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question)" :id="'document_comment_'+question.id" v-model="question.qa_question_response.comment"></textarea>
                            </div>
                          </div>

                          <div class="field">
                            <label>OutCome</label>
                            <div class="control">
                              <select v-model="question.qa_question_response.outcome" class="input"
                                      @change="hide_show_qa_score_field($event, question)"
                                      :id="'document_outcome_'+question.id"
                                      required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                                <option value="Subjective">Subjective</option>
                              </select>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field" :id="'score_after_qa_field_'+question.id" :style="question.qa_question_response.outcome !== 'Subjective' ? 'display: none' : 'display: block'">
                            <label>Score after QA</label>
                            <input type="number" step="any" class="input" @focusout="submit_qa_response(question)" :id="'document_score_after_qa_'+question.id" v-model="question.qa_question_response.score_after_qa"/>
                          </div>

                          <div class="field">
                            <button type="button" class="button is-primary is-small is-pulled-right" @click="submit_qa_response(question)">Save</button>
                          </div>
                        </div>

                        <div class="column is-8">
                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">
                            <p>Your web browser doesn't have a PDF plugin.
                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>
                          </object>

<!--                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">-->
<!--                            <p>Your web browser doesn't have a PDF plugin.-->
<!--                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>-->
<!--                          </object>-->
<!--                          <iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url=https://media.readthedocs.org/pdf/django/2.2.x/django.pdf" type="application/pdf"-->
<!--                                  frameBorder="0" scrolling="auto" height="100%" width="100%" ></iframe>-->
                        </div>
                      </div>
                    </form>
                    </template>
                    <template v-else-if="question.question_type === 'nca_c'">
                      <form >
                      <div class="columns">
                        <div class="column is-12">
                          <p><strong>Instructions: </strong> {{ question.verification_instruction }}</p>
                        </div>
                      </div>
                      <div class="columns">

                        <div class="column is-4">

                          <div class="field">
                            <label>Serial Number</label>
                            <div class="control">
                              <input type="text" class="input" :id="'document_number_'+question.id" @focusout="submit_qa_response(question)"
                                     v-model="question.qa_question_response.number"/>
<!--                              <small style="color: red">Supplier Response: {{ question.question_type_response }}</small>-->
                            </div>
                          </div>

                          <div class="field">
                            <label>Expiry Date</label>
                            <div class="control">
                              <input type="date" class="input" @focusout="submit_qa_response(question)" :id="'document_date_'+question.id"
                                     v-model="question.qa_question_response.date"/>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>
                          <div class="field">
                            <label>Expiry Date OutCome</label>
                            <div class="control" v-if="question.qa_question_response.nca">
                              <select class="input" v-model="question.qa_question_response.nca.expiry_date_outcome"
                                      @focusout="submit_qa_response(question)"
                                      :id="'nca_expiry_date_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                            <div class="control" v-else>
                              <select class="input"
                                      @focusout="submit_qa_response(question)"
                                      :id="'nca_expiry_date_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                          </div>

                          <div class="field">
                            <label>Comment</label>
                            <div class="control">
                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question)" :id="'document_comment_'+question.id" v-model="question.qa_question_response.comment"></textarea>
                            </div>
                          </div>

                          <div class="field">
                            <label>OutCome</label>
                            <div class="control">
                              <select v-model="question.qa_question_response.outcome" class="input"
                                      @change="hide_show_qa_score_field($event, question)"
                                      :id="'document_outcome_'+question.id"
                                      required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                                <option value="Subjective">Subjective</option>
                              </select>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field" :id="'score_after_qa_field_'+question.id" :style="question.qa_question_response.outcome !== 'Subjective' ? 'display: none' : 'display: block'">
                            <label>Score after QA</label>
                            <input type="number" step="any" class="input" @focusout="submit_qa_response(question)" :id="'document_score_after_qa_'+question.id" v-model="question.qa_question_response.score_after_qa"/>
                          </div>

                          <div class="field">
                            <button type="button" class="button is-primary is-small is-pulled-right" @click="submit_qa_response(question)">Save</button>
                          </div>
                        </div>

                        <div class="column is-8">
                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">
                            <p>Your web browser doesn't have a PDF plugin.
                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>
                          </object>

<!--                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">-->
<!--                            <p>Your web browser doesn't have a PDF plugin.-->
<!--                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>-->
<!--                          </object>-->
<!--                          <iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url=https://media.readthedocs.org/pdf/django/2.2.x/django.pdf" type="application/pdf"-->
<!--                                  frameBorder="0" scrolling="auto" height="100%" width="100%" ></iframe>-->
                        </div>
                      </div>
                    </form>
                    </template>
                    <template v-else-if="question.question_type === 'ppb'">
                      <form >
                      <div class="columns">
                        <div class="column is-12">
                          <p><strong>Instructions: </strong> {{ question.verification_instruction }}</p>
                        </div>
                      </div>
                      <div class="columns">

                        <div class="column is-4">
                          <div class="field">
                            <label>Company Name</label>
                            <div class="control">
                              <input type="text" class="input" :id="'ppb_company_name_'+question.id"
                                     @focusout="submit_qa_response(question)"
                                     v-if="question.qa_question_response.poisons_board"
                                     v-model="question.qa_question_response.poisons_board.company_name"/>
                              <input v-else type="text" class="input" :id="'ppb_company_name_'+question.id"
                                     @focusout="submit_qa_response(question)"/>
                              <small style="color: red">Supplier Response: {{ question.question_type_response }}</small>
                            </div>
                          </div>

                          <div class="field">
                            <label>Company Name OutCome</label>
                            <div class="control" v-if="question.qa_question_response.poisons_board">
                              <select class="input" v-model="question.qa_question_response.poisons_board.company_name_outcome"
                                      @focusout="submit_qa_response(question)"
                                      :id="'ppb_company_name_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                            <div class="control" v-else>
                              <select class="input"
                                      @focusout="submit_qa_response(question)"
                                      :id="'ppb_company_name_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                          </div>

                          <div class="field">
                            <label>Expiry Date</label>
                            <div class="control">
                              <input type="date" class="input" @focusout="submit_qa_response(question)" :id="'document_date_'+question.id" v-model="question.qa_question_response.date"/>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>
                          <div class="field">
                            <label>Expiry Date OutCome</label>
                            <div class="control" v-if="question.qa_question_response.poisons_board">
                              <select class="input" v-model="question.qa_question_response.poisons_board.expiry_date_outcome"
                                      @focusout="submit_qa_response(question)"
                                      :id="'ppb_expiry_date_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                            <div class="control" v-else>
                              <select class="input"
                                      @focusout="submit_qa_response(question)"
                                      :id="'ppb_expiry_date_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                          </div>

                          <div class="field" hidden>
                            <label>Document Number</label>
                            <div class="control">
                              <input type="text" class="input" :id="'document_number_'+question.id"/>
<!--                              <small style="color: red">Supplier Response: {{ question.question_type_response }}</small>-->
                            </div>
                          </div>

                          <div class="field">
                            <label>Comment</label>
                            <div class="control">
                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question)" :id="'document_comment_'+question.id" v-model="question.qa_question_response.comment"></textarea>
                            </div>
                          </div>

                          <div class="field">
                            <label>OutCome</label>
                            <div class="control">
                              <select v-model="question.qa_question_response.outcome" class="input"
                                      @change="hide_show_qa_score_field($event, question)"
                                      :id="'document_outcome_'+question.id"
                                      required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                                <option value="Subjective">Subjective</option>
                              </select>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field" :id="'score_after_qa_field_'+question.id" :style="question.qa_question_response.outcome !== 'Subjective' ? 'display: none' : 'display: block'">
                            <label>Score after QA</label>
                            <input type="number" step="any" class="input" @focusout="submit_qa_response(question)" :id="'document_score_after_qa_'+question.id" v-model="question.qa_question_response.score_after_qa"/>
                          </div>

                          <div class="field">
                            <button type="button" class="button is-primary is-small is-pulled-right" @click="submit_qa_response(question)">Save</button>
                          </div>
                        </div>

                        <div class="column is-8">
                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">
                            <p>Your web browser doesn't have a PDF plugin.
                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>
                          </object>

<!--                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">-->
<!--                            <p>Your web browser doesn't have a PDF plugin.-->
<!--                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>-->
<!--                          </object>-->
<!--                          <iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url=https://media.readthedocs.org/pdf/django/2.2.x/django.pdf" type="application/pdf"-->
<!--                                  frameBorder="0" scrolling="auto" height="100%" width="100%" ></iframe>-->
                        </div>
                      </div>
                    </form>
                    </template>
                    <template v-else-if="question.question_type === 'coi'">
                      <form >
                      <div class="columns">
                        <div class="column is-12">
                          <p><strong>Instructions: </strong> {{ question.verification_instruction }}</p>
                        </div>
                      </div>
                      <div class="columns">

                        <div class="column is-4">
                          <div class="field">
                            <label>Company Name</label>
                            <div class="control">
                              <input type="text" class="input" :id="'coi_company_name_'+question.id"
                                     @focusout="submit_qa_response(question)"
                                     v-if="question.qa_question_response.incorporation"
                                     v-model="question.qa_question_response.incorporation.company_name"/>
                              <input type="text" class="input" :id="'coi_company_name_'+question.id"
                                     @focusout="submit_qa_response(question)" v-else/>
                              <small style="color: red">Supplier Response: {{ question.question_type_response.company_name }}</small>
                            </div>
                          </div>

                          <div class="field">
                            <label>Company Name OutCome</label>
                            <div class="control" v-if="question.qa_question_response.incorporation">
                              <select class="input" v-model="question.qa_question_response.incorporation.company_name_outcome"
                                      @focusout="submit_qa_response(question)"
                                      :id="'coi_company_name_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                            <div class="control" v-else>
                              <select class="input"
                                      @focusout="submit_qa_response(question)"
                                      :id="'coi_company_name_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                          </div>

<!--                          <div class="field">-->
<!--                            <label>Company Number</label>-->
<!--                            <div class="control">-->
<!--                              <input type="text" class="input" :id="'document_number_'+question.id" @focusout="submit_qa_response(question)"-->
<!--                                     v-model="question.qa_question_response.number"/>-->
<!--                              <small style="color: red">Supplier Response: {{ question.question_type_response.data.registration_number }}</small>-->
<!--                            </div>-->
<!--                          </div>-->

                          <div class="field">
                            <label>Company Number OutCome</label>
                            <div class="control" v-if="question.qa_question_response.incorporation">
                              <select class="input" v-model="question.qa_question_response.incorporation.company_number_outcome"
                                      @focusout="submit_qa_response(question)"
                                      :id="'coi_company_number_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                            <div class="control" v-else>
                              <select class="input"
                                      @focusout="submit_qa_response(question)"
                                      :id="'coi_company_number_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                          </div>

                          <div class="field">
                            <label>Expiry Date</label>
                            <div class="control">
                              <input type="date" class="input" @focusout="submit_qa_response(question)" :id="'document_date_'+question.id" v-model="question.qa_question_response.date"/>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>
                          <div class="field">
                            <label>Expiry Date OutCome</label>
                            <div class="control" v-if="question.qa_question_response.poisons_board">
                              <select class="input" v-model="question.qa_question_response.poisons_board.expiry_date_outcome"
                                      @focusout="submit_qa_response(question)"
                                      :id="'ppb_expiry_date_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                            <div class="control" v-else>
                              <select class="input"
                                      @focusout="submit_qa_response(question)"
                                      :id="'ppb_expiry_date_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                          </div>

                          <div class="field" hidden>
                            <label>Document Number</label>
                            <div class="control">
                              <input type="text" class="input" :id="'document_number_'+question.id"/>
<!--                              <small style="color: red">Supplier Response: {{ question.question_type_response }}</small>-->
                            </div>
                          </div>

                          <div class="field">
                            <label>Comment</label>
                            <div class="control">
                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question)" :id="'document_comment_'+question.id" v-model="question.qa_question_response.comment"></textarea>
                            </div>
                          </div>

                          <div class="field">
                            <label>OutCome</label>
                            <div class="control">
                              <select v-model="question.qa_question_response.outcome" class="input"
                                      @change="hide_show_qa_score_field($event, question)"
                                      :id="'document_outcome_'+question.id"
                                      required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                                <option value="Subjective">Subjective</option>
                              </select>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field" :id="'score_after_qa_field_'+question.id" :style="question.qa_question_response.outcome !== 'Subjective' ? 'display: none' : 'display: block'">
                            <label>Score after QA</label>
                            <input type="number" step="any" class="input" @focusout="submit_qa_response(question)" :id="'document_score_after_qa_'+question.id" v-model="question.qa_question_response.score_after_qa"/>
                          </div>

                          <div class="field">
                            <button type="button" class="button is-primary is-small is-pulled-right" @click="submit_qa_response(question)">Save</button>
                          </div>
                        </div>

                        <div class="column is-8">
                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">
                            <p>Your web browser doesn't have a PDF plugin.
                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>
                          </object>

<!--                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">-->
<!--                            <p>Your web browser doesn't have a PDF plugin.-->
<!--                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>-->
<!--                          </object>-->
<!--                          <iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url=https://media.readthedocs.org/pdf/django/2.2.x/django.pdf" type="application/pdf"-->
<!--                                  frameBorder="0" scrolling="auto" height="100%" width="100%" ></iframe>-->
                        </div>
                      </div>
                    </form>
                    </template>
                    <template v-else>
                      <form >
                      <div class="columns">
                        <div class="column is-12">
                          <p><strong>Instructions: </strong> {{ question.verification_instruction }}</p>
                        </div>
                      </div>
                      <div class="columns">

                        <div class="column is-4">
                          <template>
                            <div class="field" v-if="question.question_type === 'cr12'">
                              <label>Supplier Company Directors</label>
                              <div class="control" v-if="question.question_type_response['directors'].length">
                                <label v-for="director in question.question_type_response['directors']"
                                  v-bind:key="director">
                                  {{ director }}
                                </label>
                              </div>
                              <div class="control">
                                <small style="color: red">No Response Submitted</small>
                              </div>
                            </div>

                            <div class="field" v-if="question.question_type === 'cr12'">
                            <label>Supplier Company Directors OutCome</label>
                            <div class="control" v-if="question.qa_question_response.cr12">
                              <select class="input" v-model="question.qa_question_response.cr12.directors_outcome"
                                      @focusout="submit_qa_response(question)"
                                      :id="'cr12_directors_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                            <div class="control" v-else>
                              <select class="input"
                                      @focusout="submit_qa_response(question)"
                                      :id="'cr12_directors_outcome_'+question.id" required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                              </select>
                            </div>
                          </div>


                            <div class="field" v-if="question.question_type === 'cr12'">
                              <label>Company Number</label>
                              <div class="control">
                                <input type="text" class="input" :id="'document_number_'+question.id" @focusout="submit_qa_response(question)" v-model="question.qa_question_response.number"/>
                                <small style="color: red">Supplier Response: {{ question.question_type_response.registration_number }}</small>
                              </div>
                            </div>

                            <div class="field" v-if="question.question_type === 'cr12'">
                              <label>Company Number OutCome</label>
                              <div class="control">
                                <template v-if="question.qa_question_response.cr12">
                                  <select class="input" v-model="question.qa_question_response.cr12.company_number_outcome"
                                        @focusout="submit_qa_response(question)"
                                        :id="'cr12_company_number_outcome_'+question.id" required>
                                  <option selected disabled>Select Outcome</option>
                                  <option value="Pass">Pass</option>
                                  <option value="Fail">Fail</option>
                                </select>
                                </template>

                                <template v-else>
                                  <select class="input"
                                        @focusout="submit_qa_response(question)"
                                        :id="'cr12_company_number_outcome_'+question.id" required>
                                  <option selected disabled value="">Select Outcome</option>
                                  <option value="Pass">Pass</option>
                                  <option value="Fail">Fail</option>
                                </select>
                                </template>
                              </div>
                            </div>

                            <div class="field" v-else>
                              <label>Document Number</label>
                              <div class="control">
                                <input type="text" class="input" :id="'document_number_'+question.id" @focusout="submit_qa_response(question)" v-model="question.qa_question_response.number"/>
                              </div>
                            </div>
                          </template>



                          <div class="field">
                            <label>Document Date</label>
                            <div class="control">
                              <input type="date" class="input" @focusout="submit_qa_response(question)" :id="'document_date_'+question.id" v-model="question.qa_question_response.date"/>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field">
                            <label>Comment</label>
                            <div class="control">
                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question)" :id="'document_comment_'+question.id" v-model="question.qa_question_response.comment"></textarea>
                            </div>
                          </div>

                          <div class="field">
                            <label>OutCome</label>
                            <div class="control">
                              <select v-model="question.qa_question_response.outcome" class="input"
                                      @change="hide_show_qa_score_field($event, question)"
                                      :id="'document_outcome_'+question.id"
                                      required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                                <option value="Subjective">Subjective</option>
                              </select>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field" :id="'score_after_qa_field_'+question.id" :style="question.qa_question_response.outcome !== 'Subjective' ? 'display: none' : 'display: block'">
                            <label>Score after QA</label>
                            <input type="number" step="any" class="input" @focusout="submit_qa_response(question)" :id="'document_score_after_qa_'+question.id" v-model="question.qa_question_response.score_after_qa"/>
                          </div>

                          <div class="field">
                            <button type="button" class="button is-primary is-small is-pulled-right" @click="submit_qa_response(question)">Save</button>
                          </div>
                        </div>

                        <div class="column is-8">
                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">
                            <p>Your web browser doesn't have a PDF plugin.
                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>
                          </object>

<!--                          <object :data="question.question.supplier_response.document_url" type="application/pdf" height="100%" width="100%">-->
<!--                            <p>Your web browser doesn't have a PDF plugin.-->
<!--                             <a :href="question.question.supplier_response.document_url">click here to download the PDF file.</a></p>-->
<!--                          </object>-->
<!--                          <iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url=https://media.readthedocs.org/pdf/django/2.2.x/django.pdf" type="application/pdf"-->
<!--                                  frameBorder="0" scrolling="auto" height="100%" width="100%" ></iframe>-->
                        </div>
                      </div>
                    </form>
                    </template>
                  </div>
                </div>
              </article>

              <template v-if="next_section !== ''">
                <button type="button" @click="go_to_next_section()" class="button is-primary is-small is-pulled-right">Next</button>
              </template>
              <template v-else>
                <div class="field">
                  <router-link :to="'/company/prequalification/category/details/'+sections[0].prequal_id+'/'+$route.params.category_id" type="button" class="button is-primary is-small is-pulled-right">Finish</router-link>
                </div>
              </template>
            </div>
          </div>
        </div>

        <div class="columns" v-else-if="active_section.name === 'Financial Ratios'">
          <div class="column is-12" style="padding: 16px 24px;">
            <div class="accordion_third">
              <table class="table is-fullwidth">
            <thead>
              <tr>
                <th>Description</th>
                <th>Bidder Response</th>
                <th>QA Response</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th><label class="label">Equity *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right" disabled readonly
                      :value="ratio_instance.equity"
                      >
                    </div>
                  </div>
                </th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="ratios_form.equity_after_qa" required>
                    </div>
                  </div>
                </th>
              </tr>

              <tr>
                <th><label class="label">Current Liabilities *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right" disabled readonly
                      :value="ratio_instance.curr_liabilities">
                    </div>
                  </div>
                </th>
                <th>
                  <div class="field">
                      <div class="control">
                        <input class="input is-small" type="number" style="text-align: right"
                               step="any" v-model="ratios_form.curr_liabilities_after_qa" required>
                      </div>
                    </div>
                </th>
              </tr>
              <tr>
                <th><label class="label">Fixed Assets *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right" disabled readonly
                      :value="ratio_instance.fixed_assets">
                    </div>
                  </div>
                </th>
                <th>
                  <div class="field">
                      <div class="control">
                        <input class="input is-small" type="number" style="text-align: right"
                               step="any" v-model="ratios_form.fixed_assets_after_qa" required>
                      </div>
                    </div>
                </th>
              </tr>

              <tr>
                <th><label class="label">Current Assets *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right" disabled readonly
                      :value="ratio_instance.current_assets">
                    </div>
                  </div>
                </th>
                <th>
                  <div class="field">
                      <div class="control">
                        <input class="input is-small" type="number" style="text-align: right"
                               step="any" v-model="ratios_form.current_assets_after_qa" required>
                      </div>
                    </div>
                </th>
              </tr>

              <tr>
                <th><label class="label">Long Term Loans(Debt) *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right" disabled readonly
                      :value="ratio_instance.debtors">
                    </div>
                  </div>
                </th>
                <th>
                  <div class="field">
                      <div class="control">
                        <input class="input is-small" type="number" style="text-align: right"
                               v-model="ratios_form.debtors_after_qa" step="any" required>
                      </div>
                    </div>
                </th>
              </tr>

              <tr>
                <th><label class="label">Cash *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right" disabled readonly
                      :value="ratio_instance.cash">
                    </div>
                  </div>
                </th>
                <th>
                  <div class="field">
                      <div class="control">
                        <input class="input is-small" type="number" style="text-align: right"
                               step="any" v-model="ratios_form.cash_after_qa" required>
                      </div>
                    </div>
                </th>
              </tr>

              <tr>
                <th><label class="label">Turnover *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right" disabled readonly
                      :value="ratio_instance.turnover">
                    </div>
                  </div>
                </th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="ratios_form.turnover_after_qa" required>
                    </div>
                  </div>
                </th>
                </tr>
              <tr>
                <th><label class="label">Gross Profit *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right" disabled readonly
                      :value="ratio_instance.gross_profit">
                    </div>
                  </div>
                </th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="ratios_form.gross_profit_after_qa" required>
                    </div>
                  </div>
                </th>
                </tr>
              <tr>
                <th><label class="label">Net Profit *</label></th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right" disabled readonly
                      :value="ratio_instance.net_profit">
                    </div>
                  </div>
                </th>
                <th>
                  <div class="field">
                    <div class="control">
                      <input class="input is-small" type="number" style="text-align: right"
                             step="any" v-model="ratios_form.net_profit_after_qa" required>
                    </div>
                  </div>
                </th>
                </tr>
                <tr>
                  <th></th>
                  <th></th>
                  <th>
                    <button class="button is-primary is-small is-pulled-right" @click="submit_ratios_qa()">Submit Values</button>
                  </th>
                </tr>
            </tbody>
          </table>

              <article class="message" v-for="question in section_questions" v-bind:key="question.id">
                <a :href="'#collapsible-message-'+question.id">
                <div class="message-header">
                  <p>Question: {{ question.question.description }}</p>
                </div>
                </a>

                <div :id="'collapsible-message-'+question.id" class="message-body is-collapsible" data-parent="accordion_second" data-allow-multiple="true">
                  <div class="message-body-content">
                    <form >
                      <div class="columns">
                        <div class="column is-12">
                          <p><strong>Instructions: </strong> {{ question.verification_instruction }}</p>
                        </div>
                      </div>
                      <div class="columns">

                        <div class="column is-4">

                            <div class="field" hidden>
                              <label>Document Number</label>
                              <div class="control">
                                <input type="text" class="input" :id="'document_number_'+question.id" @focusout="submit_qa_response(question)" v-model="question.qa_question_response.number"/>
                              </div>
                            </div>

                          <div class="field" hidden>
                            <label>Document Date</label>
                            <div class="control">
                              <input type="date" class="input" @focusout="submit_qa_response(question)" :id="'document_date_'+question.id" v-model="question.qa_question_response.date"/> -->
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field">
                            <label>Ratio Before QA</label>
                            <div class="control">
                              <input type="number" step="any" class="input" :value="question.question.supplier_response.options"
                               readonly />
                            </div>
                          </div>

                          <div class="field">
                            <label>Ratio After QA</label>
                            <div class="control">
                              <input type="number" step="any" class="input" :value="question.qa_question_response.number" readonly>
                            </div>
                          </div>

                          <div class="field">
                            <label>Comment</label>
                            <div class="control">
                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question)" :id="'document_comment_'+question.id" v-model="question.qa_question_response.comment"></textarea>
                            </div>
                          </div>

                          <div class="field">
                            <label>OutCome</label>
                            <div class="control">
                              <select v-model="question.qa_question_response.outcome" class="input"
                                      @change="hide_show_qa_score_field($event, question)"
                                      :id="'document_outcome_'+question.id"
                                      required>
                                <option selected disabled>Select Outcome</option>
                                <option value="Pass">Pass</option>
                                <option value="Fail">Fail</option>
                                <option value="Subjective">Subjective</option>
                              </select>
<!--                              <textarea class="textarea" rows="4" @focusout="submit_qa_response(question.id)" :id="'instructions_'+question.id" v-model="question.verification_instruction"></textarea>-->
                            </div>
                          </div>

                          <div class="field" :id="'score_after_qa_field_'+question.id" :style="question.qa_question_response.outcome !== 'Subjective' ? 'display: none' : 'display: block'">
                            <label>Score after QA</label>
                            <input type="number" step="any" class="input" @focusout="submit_qa_response(question)" :id="'document_score_after_qa_'+question.id" v-model="question.qa_question_response.score_after_qa"/>
                          </div>

                          <div class="field">
                            <button type="button" class="button is-primary is-small is-pulled-right" @click="submit_qa_response(question)">Save</button>
                          </div>
                        </div>

                        <div class="column is-8">
                          <object :data="question.question_type_response" type="application/pdf" height="100%" width="100%">
                            <p>Your web browser doesn't have a PDF plugin.
                             <a :href="question.question_type_response">click here to download the PDF file.</a></p>
                          </object>

                        </div>
                      </div>
                    </form>
                  </div>
                </div>
              </article>

              <template v-if="next_section !== ''">
                <button type="button" @click="go_to_next_section()" class="button is-primary is-small is-pulled-right">Next</button>
              </template>
              <template v-else>
                <div class="field">
                  <router-link :to="'/company/prequalification/category/details/'+sections[0].prequal_id+'/'+$route.params.category_id" type="button" class="button is-primary is-small is-pulled-right">Finish</router-link>
                </div>
              </template>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import prequal from "@/services/company/prequal";

export default {
  name: "ConductQa",
  data() {
    return {
      sections: [],
      active_section: '',
      ratio_instance: '',
      next_section: '',
      section_questions: '',
      ratios_form: {}
    }
  },
  methods: {
    hide_show_qa_score_field(event, question){
      let element = event.target
      let value = element.value
      if (value === 'Subjective'){
        document.getElementById('score_after_qa_field_'+question.id).style.display = 'block'
      }else{
        document.getElementById('score_after_qa_field_'+question.id).style.display = 'none'
      }
    },
    async get_sections() {
      try {
        let response = await prequal.qa_sections(this.$route.params.category_id)
        this.sections = response.data
        this.active_section = response.data[0]
        this.get_questions(response.data[0])
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },

    async get_questions(section) {
      this.section_questions = []
      this.active_section = section
      let active_section_index =  this.sections.indexOf(section)
      let next_section_index = active_section_index + 1
      if (this.sections.length > next_section_index ){
        this.next_section = this.sections[next_section_index]
      }else{
        this.next_section = ''
      }
      try {
        let response = await prequal.qa_section_questions_supplier_response(
            this.$route.params.category_id, section.id, this.$route.params.participant_id
        )
        this.section_questions = response.data['qa_questions']
        this.ratio_instance = response.data['ratios_instance']
        if(this.ratio_instance !== null){
          this.ratios_form = {
          "equity_after_qa": this.ratio_instance.equity_after_qa,
          "curr_liabilities_after_qa": this.ratio_instance.curr_liabilities_after_qa,
          "fixed_assets_after_qa": this.ratio_instance.fixed_assets_after_qa,
          "current_assets_after_qa": this.ratio_instance.current_assets_after_qa,
          "debtors_after_qa": this.ratio_instance.debtors_after_qa,
          "turnover_after_qa": this.ratio_instance.turnover_after_qa,
          "gross_profit_after_qa": this.ratio_instance.gross_profit_after_qa,
          "net_profit_after_qa": this.ratio_instance.net_profit_after_qa,
          "cash_after_qa": this.ratio_instance.cash_after_qa,
        }
        }
        let scroll = document.getElementById('to_scroll');
        scroll.scrollTop = 0;
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },

    go_to_next_section(){
      let n = document.getElementById('button_'+this.next_section.id)
      n.click()
    },
    async submit_qa_response(question){
      let date = document.getElementById('document_date_'+question.id).value

      let content = {
          'number': document.getElementById('document_number_' + question.id).value,
          'outcome': document.getElementById('document_outcome_' + question.id).value,
          'date': date ? date : null,
          'score_after_qa': document.getElementById('document_score_after_qa_' + question.id).value,
          'supplier': this.$route.params.participant_id,
          'quality_assurance_question': question.id,
          'comment': document.getElementById('document_comment_' + question.id).value,
        }

      if (question.question_type === 'tcc'){
        content = {
          ...content,
          'pin_number_outcome': document.getElementById('pin_number_outcome_' + question.id).value,
          'expiry_date_outcome': document.getElementById('expiry_date_outcome_' + question.id).value,
          'company_name': document.getElementById('company_name_'+question.id).value,
        }
      }else if (question.question_type === 'cr12'){
        content = {
          ...content,
          'company_number_outcome': document.getElementById('cr12_company_number_outcome_'+question.id).value,
          'directors_outcome': document.getElementById('cr12_directors_outcome_'+question.id).value,
        }
      }else if(question.question_type === 'bp'){
        content = {
          ...content,
          'business_name': document.getElementById('business_name_'+question.id).value,
          'business_name_outcome': document.getElementById('business_name_outcome_'+question.id).value,
        }
      }else if(question.question_type === 'pin'){
        content = {
          ...content,
          'tax_pin_outcome': document.getElementById('tax_pin_outcome_'+question.id).value,
        }
      }else if(question.question_type === 'nca_c'){
        content = {
          ...content,
          'expiry_date_outcome': document.getElementById('nca_expiry_date_outcome_'+question.id).value
        }
      }else if(question.question_type === 'ppb'){
        content = {
          ...content,
          'company_name': document.getElementById('ppb_company_name_'+question.id).value,
          'company_name_outcome': document.getElementById('ppb_company_name_outcome_'+question.id).value,
          'expiry_date_outcome': document.getElementById('ppb_expiry_date_outcome_'+question.id).value
        }
      }else if(question.question_type === 'coi'){
        content = {
          ...content,
          'company_name': document.getElementById('coi_company_name_'+question.id).value,
          'company_name_outcome': document.getElementById('coi_company_name_outcome_'+question.id).value,
          'company_number_outcome': document.getElementById('coi_company_number_outcome_'+question.id).value,
        }
      }
      console.log(content)
      try {
        await prequal.submit_qa_question_response(content, this.$route.params.category_id, question.id)
        window.toast.fire({icon: 'success', title: 'Response submitted'})
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async submit_ratios_qa(){
      let category_id = this.$route.params.category_id
      let supplier_id = this.$route.params.participant_id

      try{
        let response = await prequal.ratios_qa(category_id, supplier_id, this.ratios_form)
        if(response.status === 200){
          window.toast.fire({icon: 'success', title: 'Values submitted successfully'})
          this.get_questions(this.active_section)
        }
      }catch(err){
        window.toast.fire({icon: 'error', title: err})
      }
    }
  },
  mounted() {
    this.get_sections()
    // this.active_section = this.sections[0]
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

.is-primary {
  background-color: #073A82 !important;
}

li.is-active a{
  background-color: #073A82 !important;
  border-color: #073A82 !important;
  color: #fff;
  z-index: 1;
}
.message-header {
    background-color: #073A82 !important;
}

</style>