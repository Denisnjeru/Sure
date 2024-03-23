const routes = [
    {
    path: '/company/tenders',
    name: 'CompanyTenders',
    component: () => import('../../views/company/tender/List.vue')
  },
  {
    path: '/company/edit/tender/:id',
    name: 'CompanyTender_edit',
    component: () => import('../../views/company/tender/Edit.vue')
  },
  {
    path: '/company/create/tender',
    name: 'CompanyTender_create',
    component: () => import('../../views/company/tender/Create.vue')
  },
  {
    path: '/company/tender/details/:id',
    name: 'CompanyTender_details',
    component: () => import('../../views/company/tender/Details.vue')
  },
  {
    path: '/company/tender/create/category/:id',
    name: 'CompanyTender_category_create',
    component: () => import('../../views/company/tender/category/Create.vue')
  },
  {
    path: '/company/tender/edit/category/:tender_id/:category_id',
    name: 'CompanyTender_category_edit',
    component: () => import('../../views/company/tender/category/Edit.vue')
  },
  {
    path: '/company/tender/category/details/:tender_id/:category_id',
    name: 'CompanyTender_category_details',
    component: () => import('../../views/company/tender/category/Details.vue')
  },
  {
    path: '/company/tender/category/refresh/scores/:tender_id/:category_id/:task_id',
    name: 'CompanyTenderCategoryRefreshScores',
    component: () => import('../../views/company/tender/category/RefreshScoresProgress.vue')
  },
  {
    path: '/company/tender/financial/details/:tender_id/:category_id',
    name: 'CompanyTender_financial_details',
    component: () => import('../../views/company/tender/category/financial/Details.vue')
  },
  {
    path: '/company/tender/create/section/:tender_id/:category_id',
    name: 'CompanyTender_create_section',
    component: () => import('../../views/company/tender/category/section/Create.vue')
  },
  {
    path: '/company/tender/edit/section/:tender_id/:category_id/:section_id',
    name: 'CompanyTender_edit_section',
    component: () => import('../../views/company/tender/category/section/Edit.vue')
  },
  {
    path: '/company/tender/section/questions/:section_id',
    name: 'CompanyTender_section_questions',
    component: () => import('../../views/company/tender/category/section/Questions.vue')
  },
  {
    path: '/company/tender/create/question/:section_id',
    name: 'CompanyTender_create_question',
    component: () => import('../../views/company/tender/category/section/CreateQuestion.vue')
  },
  {
    path: '/company/tender/edit/question/:section_id/:id',
    name: 'CompanyTender_edit_question',
    component: () => import('../../views/company/tender/category/section/EditQuestion.vue')
  },
  {
    path: '/company/tender/qa/instructions/:category_id',
    name: 'CompanyTender_qa_instructions',
    component: () => import('../../views/company/tender/category/qa/AddInstructions.vue')
  },
  {
    path: '/company/tender/conduct/qa/:category_id/:participant_id',
    name: 'CompanyTender_conduct_qa',
    component: () => import('../../views/company/tender/category/qa/ConductQa.vue')
  },
  {
    path: '/company/tender/dd/details/:category_id',
    name: 'CompanyTender_dd_details',
    component: () => import('../../views/company/tender/category/dd/Participants.vue')
  },
  {
    path: '/company/tender/dd/conduct/:category_id/:participant_id/:question_id',
    name: 'CompanyTender_dd_conduct',
    component: () => import('../../views/company/tender/category/dd/ConductDD.vue')
  },
  {
    path: '/company/tender/dd/add/questions/:category_id',
    name: 'CompanyTender_dd_add_questions',
    component: () => import('../../views/company/tender/category/dd/AddDDWideQuestions.vue')
  },
  {
    path: '/company/tender/dd/add/supplier/questions/:category_id/:participant_id',
    name: 'CompanyTender_dd_add_supplier_questions',
    component: () => import('../../views/company/tender/category/dd/AddPerSupplierQuestion.vue')
  },
  {
    path: '/company/tender/dd/supplier/questions/:category_id/:participant_id',
    name: 'CompanyTender_dd_supplier_questions',
    component: () => import('../../views/company/tender/category/dd/SupplierQuestions.vue')
  },
  {
    path: '/company/tender/letters/:job_id/:category_id',
    name: 'CompanyTender_letters',
    component: () => import('../../views/company/tender/category/letters/ParticipantList.vue')
  },
  {
    path: '/company/tender/preview/award/letter/:job_id/:category_id/:supplier_id',
    name: 'CompanyTender_preview_award_letter',
    component: () => import('../../views/company/tender/category/letters/award_letter/PreviewLetter.vue')
  },
  {
    path: '/company/tender/preview/regret/letter/:job_id/:category_id/:supplier_id',
    name: 'CompanyTender_preview_regret_letter',
    component: () => import('../../views/company/tender/category/letters/regret_letter/PreviewLetter.vue')
  },
  {
    path: '/company/tender/reports/:id',
    name: 'CompanyTender_reports',
    component: () => import('../../views/company/tender/reports/Details.vue')
  },
  {
    path: '/company/tender/report/progress/:tender_id/:task_id',
    name: 'CompanyTender_reports',
    component: () => import('../../views/company/tender/reports/Progress.vue')
  },
  {
    path: '/company/tender/invited/suppliers/:tender_id/:category_id',
    name: 'CompanyTender_invited_suppliers',
    component: () => import('../../views/company/tender/category/InvitedSuppliers.vue')
  },
    {
    path: '/company/tender/letters/jobs',
    name: 'CompanyTenderLetterJobs',
    component: () => import('../../views/company/tender/category/letters/LetterJobs.vue')
  },
  {
    path: '/company/tender/letters/:job_id',
    name: 'CompanyTenderLetterCategories',
    component: () => import('../../views/company/tender/category/letters/LetterCategories.vue')
  },
  {
    path: '/company/tender/letters/success/create/:job_id',
    name: 'CompanyTenderLetterSuccessCreate',
    component: () => import('../../views/company/tender/category/letters/award_letter/CreateAward.vue')
  },
  {
    path: '/company/tender/letters/success/edit/:job_id',
    name: 'CompanyTenderLetterSuccessEdit',
    component: () => import('../../views/company/tender/category/letters/award_letter/EditAwardLetter.vue')
  },
  {
    path: '/company/tender/letters/custom/create/:job_id',
    name: 'CompanyTenderLetterCustomCreate',
    component: () => import('../../views/company/tender/category/letters/custom/CreateCustom.vue')
  },
    {
    path: '/company/tender/letters/custom/edit/:job_id',
    name: 'CompanyTenderLetterCustomEdit',
    component: () => import('../../views/company/tender/category/letters/custom/EditCustomLetter.vue')
  },
  {
    path: '/company/tender/letters/dd/create/:job_id',
    name: 'CompanyTenderLetterDDCreate',
    component: () => import('../../views/company/tender/category/letters/dd_letter/CreateDD.vue')
  },
  {
    path: '/company/tender/letters/dd/edit/:job_id',
    name: 'CompanyTenderLetterDDEdit',
    component: () => import('../../views/company/tender/category/letters/dd_letter/EditDDLetter.vue')
  },
  {
    path: '/company/tender/letters/regret/create/:job_id',
    name: 'CompanyTenderLetterRegretCreate',
    component: () => import('../../views/company/tender/category/letters/regret_letter/CreateRegret.vue')
  },
  {
    path: '/company/tender/letters/regret/edit/:job_id',
    name: 'CompanyTenderLetterRegretEdit',
    component: () => import('../../views/company/tender/category/letters/regret_letter/EditRegretLetter.vue')
  },
    {
    path: '/company/tender/zip/files/progress/:task_id/:section_id',
    name: 'CompanyPrequalZipFiles',
    component: () => import('../../views/company/tender/category/ZipFilesProgress.vue')
  },
    {
    path: '/company/tender/cat/suppliers/progress/:tender_id/:task_id/',
    name: 'CompanyTenderCatSuppliers',
    component: () => import('../../views/company/tender/CatSuppliersProgress.vue')
  },
]

export default routes;