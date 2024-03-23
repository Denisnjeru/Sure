const routes = [
  {
    path: '/company/prequalifications',
    name: 'CompanyPrequalifications',
    component: () => import('../../views/company/prequal/List.vue')
  },
  {
    path: '/company/edit/prequalification/:id',
    name: 'company_edit_prequalification',
    component: () => import('../../views/company/prequal/Edit.vue')
  },
  {
    path: '/company/create/prequalification',
    name: 'company_create_prequalification',
    component: () => import('../../views/company/prequal/Create.vue')
  },
  {
    path: '/company/prequalification/details/:id',
    name: 'CompanyPrequalification_details',
    component: () => import('../../views/company/prequal/Details.vue')
  },
  {
    path: '/company/prequalification/create/category/:id',
    name: 'CompanyPrequalification_category_create',
    component: () => import('../../views/company/prequal/category/Create.vue')
  },
  {
    path: '/company/prequalification/edit/category/:prequal_id/:category_id',
    name: 'CompanyPrequalification_category_edit',
    component: () => import('../../views/company/prequal/category/Edit.vue')
  },
  {
    path: '/company/prequalification/category/details/:prequal_id/:category_id',
    name: 'CompanyPrequal_category_details',
    component: () => import('../../views/company/prequal/category/Details.vue')
  },
  {
    path: '/company/prequal/category/refresh/scores/:prequal_id/:category_id/:task_id',
    name: 'CompanyPrequalCategoryRefreshScores',
    component: () => import('../../views/company/prequal/category/RefreshScoresProgress.vue')
  },
  {
    path: '/company/prequal/create/section/:prequal_id/:category_id',
    name: 'CompanyPrequal_create_section',
    component: () => import('../../views/company/prequal/category/section/Create.vue')
  },
  {
    path: '/company/prequal/edit/section/:prequal_id/:category_id/:section_id',
    name: 'CompanyPrequal_edit_section',
    component: () => import('../../views/company/prequal/category/section/Edit.vue')
  },
  {
    path: '/company/prequal/section/questions/:section_id',
    name: 'CompanyPrequal_section_questions',
    component: () => import('../../views/company/prequal/category/section/Questions.vue')
  },
  {
    path: '/company/prequal/create/question/:section_id',
    name: 'CompanyPrequal_create_question',
    component: () => import('../../views/company/prequal/category/section/CreateQuestion.vue')
  },
  {
    path: '/company/prequal/edit/question/:section_id/:id',
    name: 'CompanyPrequal_edit_question',
    component: () => import('../../views/company/prequal/category/section/EditQuestion.vue')
  },
  {
    path: '/company/prequal/qa/instructions/:category_id',
    name: 'CompanyPrequal_qa_instructions',
    component: () => import('../../views/company/prequal/category/qa/AddInstructions.vue')
  },
  {
    path: '/company/prequal/conduct/qa/:category_id/:participant_id',
    name: 'CompanyPrequal_conduct_qa',
    component: () => import('../../views/company/prequal/category/qa/ConductQa.vue')
  },
  {
    path: '/company/prequal/dd/details/:category_id',
    name: 'CompanyPrequal_dd_details',
    component: () => import('../../views/company/prequal/category/dd/Participants.vue')
  },
  {
    path: '/company/prequal/dd/conduct/:category_id/:participant_id/:question_id',
    name: 'CompanyPrequal_dd_conduct',
    component: () => import('../../views/company/prequal/category/dd/ConductDD.vue')
  },
  {
    path: '/company/prequal/dd/add/questions/:category_id',
    name: 'CompanyPrequal_dd_add_questions',
    component: () => import('../../views/company/prequal/category/dd/AddDDWideQuestions.vue')
  },
  {
    path: '/company/prequal/dd/add/supplier/questions/:category_id/:participant_id',
    name: 'CompanyPrequal_dd_add_supplier_questions',
    component: () => import('../../views/company/prequal/category/dd/AddPerSupplierQuestion.vue')
  },
  {
    path: '/company/prequal/dd/supplier/questions/:category_id/:participant_id',
    name: 'CompanyPrequal_dd_supplier_questions',
    component: () => import('../../views/company/prequal/category/dd/SupplierQuestions.vue')
  },
  {
    path: '/company/prequal/letters/:job_id/:category_id',
    name: 'CompanyPrequal_letters',
    component: () => import('../../views/company/prequal/category/letters/ParticipantList.vue')
  },
  {
    path: '/company/prequal/preview/award/letter/:job_id/:category_id/:supplier_id',
    name: 'CompanyPrequal_preview_award_letter',
    component: () => import('../../views/company/prequal/category/letters/award_letter/PreviewLetter.vue')
  },
  {
    path: '/company/prequal/preview/regret/letter/:job_id/:category_id/:supplier_id',
    name: 'CompanyPrequal_preview_regret_letter',
    component: () => import('../../views/company/prequal/category/letters/regret_letter/PreviewLetter.vue')
  },
  {
    path: '/company/prequal/category/question/upload/progress/:prequal_id/:category_id/:task_id',
    name: 'CompanyPrequal_category_question_upload_progress',
    component: () => import('../../views/company/prequal/category/section/QuestionUploadProgress.vue')
  },
  {
    path: '/company/prequal/reports/:id',
    name: 'CompanyPrequal_reports',
    component: () => import('../../views/company/prequal/reports/Details.vue')
  },
  {
    path: '/company/prequal/report/progress/:prequal_id/:task_id',
    name: 'CompanyPrequal_reports',
    component: () => import('../../views/company/prequal/reports/Progress.vue')
  },
    {
    path: '/company/prequal/invited/suppliers/:prequal_id/:category_id',
    name: 'CompanyPrequal_invited_suppliers',
    component: () => import('../../views/company/prequal/category/InvitedSuppliers.vue')
  },
  {
    path: '/company/prequal/letters/jobs',
    name: 'CompanyPrequalLetterJobs',
    component: () => import('../../views/company/prequal/category/letters/LetterJobs.vue')
  },
  {
    path: '/company/prequal/letters/:job_id',
    name: 'CompanyPrequalLetterCategories',
    component: () => import('../../views/company/prequal/category/letters/LetterCategories.vue')
  },
  {
    path: '/company/prequal/letters/success/create/:job_id',
    name: 'CompanyPrequalLetterSuccessCreate',
    component: () => import('../../views/company/prequal/category/letters/award_letter/CreateAward.vue')
  },
  {
    path: '/company/prequal/letters/success/edit/:job_id',
    name: 'CompanyPrequalLetterSuccessEdit',
    component: () => import('../../views/company/prequal/category/letters/award_letter/EditAwardLetter.vue')
  },
  {
    path: '/company/prequal/letters/custom/create/:job_id',
    name: 'CompanyPrequalLetterCustomCreate',
    component: () => import('../../views/company/prequal/category/letters/custom/CreateCustom.vue')
  },
    {
    path: '/company/prequal/letters/custom/edit/:job_id',
    name: 'CompanyPrequalLetterCustomEdit',
    component: () => import('../../views/company/prequal/category/letters/custom/EditCustomLetter.vue')
  },
  {
    path: '/company/prequal/letters/dd/create/:job_id',
    name: 'CompanyPrequalLetterDDCreate',
    component: () => import('../../views/company/prequal/category/letters/dd_letter/CreateDD.vue')
  },
  {
    path: '/company/prequal/letters/dd/edit/:job_id',
    name: 'CompanyPrequalLetterDDEdit',
    component: () => import('../../views/company/prequal/category/letters/dd_letter/EditDDLetter.vue')
  },
  {
    path: '/company/prequal/letters/regret/create/:job_id',
    name: 'CompanyPrequalLetterRegretCreate',
    component: () => import('../../views/company/prequal/category/letters/regret_letter/CreateRegret.vue')
  },
  {
    path: '/company/prequal/letters/regret/edit/:job_id',
    name: 'CompanyPrequalLetterRegretEdit',
    component: () => import('../../views/company/prequal/category/letters/regret_letter/EditRegretLetter.vue')
  },
  {
    path: '/company/prequal/zip/files/progress/:task_id/:section_id',
    name: 'CompanyPrequalZipFiles',
    component: () => import('../../views/company/prequal/category/ZipFilesProgress.vue')
  },
  {
    path: '/company/prequal/cat/suppliers/progress/:prequal_id/:task_id/',
    name: 'CompanyPrequalCatSuppliers',
    component: () => import('../../views/company/prequal/CatSuppliersProgress.vue')
  },
]

export default routes;