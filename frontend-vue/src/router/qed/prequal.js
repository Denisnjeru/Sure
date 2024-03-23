import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/qed/prequalification/buyers',
    name: 'QedSourcingPrequalificationsBuyers',
    component: () => import('../../views/qed/prequal/Buyers.vue')
  },
  {
    path: '/qed/prequalifications',
    name: 'QedSourcingPrequalifications',
    component: () => import('../../views/qed/prequal/List.vue')
  },
  {
    path: '/qed/edit/prequalification/:id',
    name: 'QedSourcingPrequalification_edit_prequalification',
    component: () => import('../../views/qed/prequal/Edit.vue')
  },
  {
    path: '/qed/create/prequalification',
    name: 'QedSourcingPrequalification_create_prequalification',
    component: () => import('../../views/qed/prequal/Create.vue')
  },
  {
    path: '/qed/prequalification/details/:id',
    name: 'QedSourcingPrequalification_details',
    component: () => import('../../views/qed/prequal/Details.vue')
  },
  {
    path: '/qed/prequalification/create/category/:id',
    name: 'QedSourcingPrequalification_category_create',
    component: () => import('../../views/qed/prequal/category/Create.vue')
  },
  {
    path: '/qed/prequalification/edit/category/:prequal_id/:category_id',
    name: 'QedSourcingPrequalification_category_edit',
    component: () => import('../../views/qed/prequal/category/Edit.vue')
  },
  {
    path: '/qed/prequalification/category/details/:prequal_id/:category_id',
    name: 'QedSourcingPrequal_category_details',
    component: () => import('../../views/qed/prequal/category/Details.vue')
  },
  {
    path: '/qed/prequal/category/refresh/scores/:prequal_id/:category_id/:task_id',
    name: 'QedSourcingPrequalCategoryRefreshScores',
    component: () => import('../../views/qed/prequal/category/RefreshScoresProgress.vue')
  },
  {
    path: '/qed/prequal/create/section/:prequal_id/:category_id',
    name: 'QedSourcingPrequal_create_section',
    component: () => import('../../views/qed/prequal/category/section/Create.vue')
  },
  {
    path: '/qed/prequal/edit/section/:prequal_id/:category_id/:section_id',
    name: 'QedSourcingPrequal_edit_section',
    component: () => import('../../views/qed/prequal/category/section/Edit.vue')
  },
  {
    path: '/qed/prequal/section/questions/:section_id',
    name: 'QedSourcingPrequal_section_questions',
    component: () => import('../../views/qed/prequal/category/section/Questions.vue')
  },
  {
    path: '/qed/prequal/create/question/:section_id',
    name: 'QedSourcingPrequal_create_question',
    component: () => import('../../views/qed/prequal/category/section/CreateQuestion.vue')
  },
  {
    path: '/qed/prequal/edit/question/:section_id/:id',
    name: 'QedSourcingPrequal_edit_question',
    component: () => import('../../views/qed/prequal/category/section/EditQuestion.vue')
  },
  {
    path: '/qed/prequal/qa/instructions/:category_id',
    name: 'QedSourcingPrequal_qa_instructions',
    component: () => import('../../views/qed/prequal/category/qa/AddInstructions.vue')
  },
  {
    path: '/qed/prequal/conduct/qa/:category_id/:participant_id',
    name: 'QedSourcingPrequal_conduct_qa',
    component: () => import('../../views/qed/prequal/category/qa/ConductQa.vue')
  },
  {
    path: '/qed/prequal/dd/details/:category_id',
    name: 'QedSourcingPrequal_dd_details',
    component: () => import('../../views/qed/prequal/category/dd/Participants.vue')
  },
  {
    path: '/qed/prequal/dd/conduct/:category_id/:participant_id/:question_id',
    name: 'QedSourcingPrequal_dd_conduct',
    component: () => import('../../views/qed/prequal/category/dd/ConductDD.vue')
  },
  {
    path: '/qed/prequal/dd/add/questions/:category_id',
    name: 'QedSourcingPrequal_dd_add_questions',
    component: () => import('../../views/qed/prequal/category/dd/AddDDWideQuestions.vue')
  },
  {
    path: '/qed/prequal/dd/add/supplier/questions/:category_id/:participant_id',
    name: 'QedSourcingPrequal_dd_add_supplier_questions',
    component: () => import('../../views/qed/prequal/category/dd/AddPerSupplierQuestion.vue')
  },
  {
    path: '/qed/prequal/dd/supplier/questions/:category_id/:participant_id',
    name: 'QedSourcingPrequal_dd_supplier_questions',
    component: () => import('../../views/qed/prequal/category/dd/SupplierQuestions.vue')
  },
  {
    path: '/qed/prequal/letters/:job_id/:category_id',
    name: 'QedSourcingPrequal_letters',
    component: () => import('../../views/qed/prequal/category/letters/ParticipantList.vue')
  },
  {
    path: '/qed/prequal/preview/award/letter/:job_id/:category_id/:supplier_id',
    name: 'QedSourcingPrequal_preview_award_letter',
    component: () => import('../../views/qed/prequal/category/letters/award_letter/PreviewLetter.vue')
  },
  {
    path: '/qed/prequal/preview/regret/letter/:job_id/:category_id/:supplier_id',
    name: 'QedSourcingPrequal_preview_regret_letter',
    component: () => import('../../views/qed/prequal/category/letters/regret_letter/PreviewLetter.vue')
  },
  {
    path: '/qed/prequal/category/question/upload/progress/:prequal_id/:category_id/:task_id',
    name: 'QedSourcingPrequal_category_question_upload_progress',
    component: () => import('../../views/qed/prequal/category/section/QuestionUploadProgress.vue')
  },
  {
    path: '/qed/prequal/reports/:id',
    name: 'QedSourcingPrequal_reports_details',
    component: () => import('../../views/qed/prequal/reports/Details.vue')
  },
  {
    path: '/qed/prequal/report/progress/:prequal_id/:task_id',
    name: 'QedSourcingPrequal_reports_progress',
    component: () => import('../../views/qed/prequal/reports/Progress.vue')
  },
    {
    path: '/qed/prequal/invited/suppliers/:prequal_id/:category_id',
    name: 'QedSourcingPrequal_invited_suppliers',
    component: () => import('../../views/qed/prequal/category/InvitedSuppliers.vue')
  },
  {
    path: '/qed/prequal/letters/jobs',
    name: 'QedSourcingPrequalLetterJobs',
    component: () => import('../../views/qed/prequal/category/letters/LetterJobs.vue')
  },
  {
    path: '/qed/prequal/letters/:job_id',
    name: 'QedSourcingPrequalLetterCategories',
    component: () => import('../../views/qed/prequal/category/letters/LetterCategories.vue')
  },
  {
    path: '/qed/prequal/letters/success/create/:job_id',
    name: 'QedSourcingPrequalLetterSuccessCreate',
    component: () => import('../../views/qed/prequal/category/letters/award_letter/CreateAward.vue')
  },
  {
    path: '/qed/prequal/letters/success/edit/:job_id',
    name: 'QedSourcingPrequalLetterSuccessEdit',
    component: () => import('../../views/qed/prequal/category/letters/award_letter/EditAwardLetter.vue')
  },
  {
    path: '/qed/prequal/letters/custom/create/:job_id',
    name: 'QedSourcingPrequalLetterCustomCreate',
    component: () => import('../../views/qed/prequal/category/letters/custom/CreateCustom.vue')
  },
    {
    path: '/qed/prequal/letters/custom/edit/:job_id',
    name: 'QedSourcingPrequalLetterCustomEdit',
    component: () => import('../../views/qed/prequal/category/letters/custom/EditCustomLetter.vue')
  },
  {
    path: '/qed/prequal/letters/dd/create/:job_id',
    name: 'QedSourcingPrequalLetterDDCreate',
    component: () => import('../../views/qed/prequal/category/letters/dd_letter/CreateDD.vue')
  },
  {
    path: '/qed/prequal/letters/dd/edit/:job_id',
    name: 'QedSourcingPrequalLetterDDEdit',
    component: () => import('../../views/qed/prequal/category/letters/dd_letter/EditDDLetter.vue')
  },
  {
    path: '/qed/prequal/letters/regret/create/:job_id',
    name: 'QedSourcingPrequalLetterRegretCreate',
    component: () => import('../../views/qed/prequal/category/letters/regret_letter/CreateRegret.vue')
  },
  {
    path: '/qed/prequal/letters/regret/edit/:job_id',
    name: 'QedSourcingPrequalLetterRegretEdit',
    component: () => import('../../views/qed/prequal/category/letters/regret_letter/EditRegretLetter.vue')
  },
  {
    path: '/qed/prequal/zip/files/progress/:task_id/:section_id',
    name: 'QedSourcingPrequalZipFiles',
    component: () => import('../../views/qed/prequal/category/ZipFilesProgress.vue')
  },
  {
    path: '/qed/prequal/cat/suppliers/progress/:prequal_id/:task_id/',
    name: 'QedSourcingPrequalCatSuppliers',
    component: () => import('../../views/qed/prequal/CatSuppliersProgress.vue')
  },
]

export default routes;