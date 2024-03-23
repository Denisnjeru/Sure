const routes = [
  {
    path: '/qed/tender/buyers',
    name: 'QedSourcingTenderBuyers',
    component: () => import('../../views/qed/tender/Buyers.vue')
  },
  {
    path: '/qed/tenders',
    name: 'QedSourcingTenders',
    component: () => import('../../views/qed/tender/List.vue')
  },
  {
    path: '/qed/edit/tender/:id',
    name: 'QedSourcingTender_edit',
    component: () => import('../../views/qed/tender/Edit.vue')
  },
  {
    path: '/qed/create/tender',
    name: 'QedSourcingTender_create',
    component: () => import('../../views/qed/tender/Create.vue')
  },
  {
    path: '/qed/tender/details/:id',
    name: 'QedSourcingTender_details',
    component: () => import('../../views/qed/tender/Details.vue')
  },
  {
    path: '/qed/tender/create/category/:id',
    name: 'QedSourcingTender_category_create',
    component: () => import('../../views/qed/tender/category/Create.vue')
  },
  {
    path: '/qed/tender/edit/category/:tender_id/:category_id',
    name: 'QedSourcingTender_category_edit',
    component: () => import('../../views/qed/tender/category/Edit.vue')
  },
  {
    path: '/qed/tender/category/details/:tender_id/:category_id',
    name: 'QedSourcingTender_category_details',
    component: () => import('../../views/qed/tender/category/Details.vue')
  },
  {
    path: '/qed/tender/category/refresh/scores/:tender_id/:category_id/:task_id',
    name: 'QedSourcingTenderCategoryRefreshScores',
    component: () => import('../../views/qed/tender/category/RefreshScoresProgress.vue')
  },
  {
    path: '/qed/tender/financial/details/:tender_id/:category_id',
    name: 'QedSourcingTender_financial_details',
    component: () => import('../../views/qed/tender/category/financial/Details.vue')
  },
  {
    path: '/qed/tender/create/section/:tender_id/:category_id',
    name: 'QedSourcingTender_create_section',
    component: () => import('../../views/qed/tender/category/section/Create.vue')
  },
  {
    path: '/qed/tender/edit/section/:tender_id/:category_id/:section_id',
    name: 'QedSourcingTender_edit_section',
    component: () => import('../../views/qed/tender/category/section/Edit.vue')
  },
  {
    path: '/qed/tender/section/questions/:section_id',
    name: 'QedSourcingTender_section_questions',
    component: () => import('../../views/qed/tender/category/section/Questions.vue')
  },
  {
    path: '/qed/tender/create/question/:section_id',
    name: 'QedSourcingTender_create_question',
    component: () => import('../../views/qed/tender/category/section/CreateQuestion.vue')
  },
  {
    path: '/qed/tender/edit/question/:section_id/:id',
    name: 'QedSourcingTender_edit_question',
    component: () => import('../../views/qed/tender/category/section/EditQuestion.vue')
  },
  {
    path: '/qed/tender/qa/instructions/:category_id',
    name: 'QedSourcingTender_qa_instructions',
    component: () => import('../../views/qed/tender/category/qa/AddInstructions.vue')
  },
  {
    path: '/qed/tender/conduct/qa/:category_id/:participant_id',
    name: 'QedSourcingTender_conduct_qa',
    component: () => import('../../views/qed/tender/category/qa/ConductQa.vue')
  },
  {
    path: '/qed/tender/dd/details/:category_id',
    name: 'QedSourcingTender_dd_details',
    component: () => import('../../views/qed/tender/category/dd/Participants.vue')
  },
  {
    path: '/qed/tender/dd/conduct/:category_id/:participant_id/:question_id',
    name: 'QedSourcingTender_dd_conduct',
    component: () => import('../../views/qed/tender/category/dd/ConductDD.vue')
  },
  {
    path: '/qed/tender/dd/add/questions/:category_id',
    name: 'QedSourcingTender_dd_add_questions',
    component: () => import('../../views/qed/tender/category/dd/AddDDWideQuestions.vue')
  },
  {
    path: '/qed/tender/dd/add/supplier/questions/:category_id/:participant_id',
    name: 'QedSourcingTender_dd_add_supplier_questions',
    component: () => import('../../views/qed/tender/category/dd/AddPerSupplierQuestion.vue')
  },
  {
    path: '/qed/tender/dd/supplier/questions/:category_id/:participant_id',
    name: 'QedSourcingTender_dd_supplier_questions',
    component: () => import('../../views/qed/tender/category/dd/SupplierQuestions.vue')
  },
  {
    path: '/qed/tender/letters/:job_id/:category_id',
    name: 'QedSourcingTender_letters',
    component: () => import('../../views/qed/tender/category/letters/ParticipantList.vue')
  },
  {
    path: '/qed/tender/preview/award/letter/:job_id/:category_id/:supplier_id',
    name: 'QedSourcingTender_preview_award_letter',
    component: () => import('../../views/qed/tender/category/letters/award_letter/PreviewLetter.vue')
  },
  {
    path: '/qed/tender/preview/regret/letter/:job_id/:category_id/:supplier_id',
    name: 'QedSourcingTender_preview_regret_letter',
    component: () => import('../../views/qed/tender/category/letters/regret_letter/PreviewLetter.vue')
  },
  {
    path: '/qed/tender/reports/:id',
    name: 'QedSourcingTender_reports_details',
    component: () => import('../../views/qed/tender/reports/Details.vue')
  },
  {
    path: '/qed/tender/report/progress/:tender_id/:task_id',
    name: 'QedSourcingTender_reports_progress',
    component: () => import('../../views/qed/tender/reports/Progress.vue')
  },
  {
    path: '/qed/tender/invited/suppliers/:tender_id/:category_id',
    name: 'QedSourcingTender_invited_suppliers',
    component: () => import('../../views/qed/tender/category/InvitedSuppliers.vue')
  },
    {
    path: '/qed/tender/letters/jobs',
    name: 'QedSourcingTenderLetterJobs',
    component: () => import('../../views/qed/tender/category/letters/LetterJobs.vue')
  },
  {
    path: '/qed/tender/letters/:job_id',
    name: 'QedSourcingTenderLetterCategories',
    component: () => import('../../views/qed/tender/category/letters/LetterCategories.vue')
  },
  {
    path: '/qed/tender/letters/success/create/:job_id',
    name: 'QedSourcingTenderLetterSuccessCreate',
    component: () => import('../../views/qed/tender/category/letters/award_letter/CreateAward.vue')
  },
  {
    path: '/qed/tender/letters/success/edit/:job_id',
    name: 'QedSourcingTenderLetterSuccessEdit',
    component: () => import('../../views/qed/tender/category/letters/award_letter/EditAwardLetter.vue')
  },
  {
    path: '/qed/tender/letters/custom/create/:job_id',
    name: 'QedSourcingTenderLetterCustomCreate',
    component: () => import('../../views/qed/tender/category/letters/custom/CreateCustom.vue')
  },
    {
    path: '/qed/tender/letters/custom/edit/:job_id',
    name: 'QedSourcingTenderLetterCustomEdit',
    component: () => import('../../views/qed/tender/category/letters/custom/EditCustomLetter.vue')
  },
  {
    path: '/qed/tender/letters/dd/create/:job_id',
    name: 'QedSourcingTenderLetterDDCreate',
    component: () => import('../../views/qed/tender/category/letters/dd_letter/CreateDD.vue')
  },
  {
    path: '/qed/tender/letters/dd/edit/:job_id',
    name: 'QedSourcingTenderLetterDDEdit',
    component: () => import('../../views/qed/tender/category/letters/dd_letter/EditDDLetter.vue')
  },
  {
    path: '/qed/tender/letters/regret/create/:job_id',
    name: 'QedSourcingTenderLetterRegretCreate',
    component: () => import('../../views/qed/tender/category/letters/regret_letter/CreateRegret.vue')
  },
  {
    path: '/qed/tender/letters/regret/edit/:job_id',
    name: 'QedSourcingTenderLetterRegretEdit',
    component: () => import('../../views/qed/tender/category/letters/regret_letter/EditRegretLetter.vue')
  },
    {
    path: '/qed/tender/zip/files/progress/:task_id/:section_id',
    name: 'QedSourcingTenderZipFiles',
    component: () => import('../../views/qed/tender/category/ZipFilesProgress.vue')
  },
    {
    path: '/qed/tender/cat/suppliers/progress/:tender_id/:task_id/',
    name: 'QedSourcingTenderCatSuppliers',
    component: () => import('../../views/qed/tender/CatSuppliersProgress.vue')
  },
]

export default routes;