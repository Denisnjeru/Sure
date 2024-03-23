import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '../views/Home.vue'
// import auction_routes from '../views/company/auction/router.js'
import store from '../store/index'
import company_prequal from "@/router/company/prequal";
import company_tender from "@/router/company/tender";
import company_auction from "@/router/company/auction";
import qed_project_management from "@/router/qed/project_management";
import company_project_management from "@/router/company/project_management";
import qed_user_management from "@/router/qed/user_management";
import qed_archive from "@/router/qed/archive";
import qed_prequal from "@/router/qed/prequal";
import qed_tender from "@/router/qed/tender";
import qed_rfq from "@/router/qed/rfq";


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    beforeEnter: (to, from, next) => {
      if(store.state.User.userData.user_type === 'supplier') {
        next({ name: 'SupplierDashboard' })
      } else if(store.state.User.userData.user_type === 'buyer') {
        next({ name: 'BuyerDashboard' })
      } else {
        next({ name: 'QedDashboard' })
      }
    }
  },
  {
    path: '/qed/dashboard',
    name: 'QedDashboard',
    component: () => import('../views/qed/dashboard/Dashboard.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "page-login" */ '../views/authentication/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import(/* webpackChunkName: "page-register" */ '../views/authentication/Register.vue')
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: () => import('../views/authentication/ResetPassword.vue')
  },
  {
    path: '/activate-account',
    name: 'ActivateAccount',
    component: () => import('../views/authentication/ActivateAccount.vue')
  },
  {
    path: '/set-password/:uidb64/:token',
    name: 'SetPassword',
    component: () => import('../views/authentication/SetPassword.vue')
  },
    // Notifications urls
  {
    path: '/notifications',
    name: 'Notifications',
    component: () => import('../views/notifications/Notifications.vue')
  },
  {
    path: '/company/rfqs',
    name: 'company_rfqs',
    component: () => import('../views/company/rfq/List.vue')
  },
  {
    path: '/company/users',
    name: 'company_users',
    component: () => import('../views/company/user_management/UserList.vue')
  },
  {
    path: '/company/roles',
    name: 'company_roles',
    component: () => import('../views/company/user_management/RoleList.vue')
  },
  {
    path: '/company/create/role',
    name: 'company_create_role',
    component: () => import('../views/company/user_management/CreateRole.vue')
  },
  {
    path: '/company/create/user',
    name: 'company_create_user',
    component: () => import('../views/company/user_management/CreateUser.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/authentication/Profile.vue')
  },
  {
    path: '/update-profile',
    name: 'UpdateProfile',
    component: () => import('../views/authentication/UpdateProfile.vue')
  },
  {
    path: '/change-password',
    name: 'ChangePassword',
    component: () => import('../views/authentication/ChangePassword.vue')
  },
  // Supplier urls
  {
    path: '/supplier/dashboard',
    name: 'SupplierDashboard',
    component: () => import('../views/supplier/dashboard/Dashboard.vue')
  },
  {
    path: '/supplier/dashboard/company/:id/jobs',
    name: 'SupplierCompanyJobs',
    component: () => import('../views/supplier/dashboard/CompanyJobs.vue')
  },
  {
    path: '/supplier/dashboard/cart',
    name: 'SupplierCompanyCart',
    component: () => import('../views/supplier/dashboard/Cart.vue')
  },
  {
    path: '/supplier/payment/mpesa',
    name: 'SupplierPaymentMpesa',
    component: () => import('../views/supplier/dashboard/Mpesa.vue')
  },
  {
    path: '/supplier/payment/cards/c',
    name: 'SupplierPaymentCellulant',
    component: () => import('../views/supplier/dashboard/Cellulant.vue')
  },
  {
    path: '/supplier/payment/cards/d',
    name: 'SupplierPaymentDPO',
    component: () => import('../views/supplier/dashboard/DPO.vue')
  },
  {
    path: '/supplier/ongoingbids',
    name: 'SupplierDashboardOngoingBids',
    component: () => import('../views/supplier/dashboard/OngoingBids.vue')
  },
  {
    path: '/supplier/closedbids',
    name: 'SupplierDashboardClosedBids',
    component: () => import('../views/supplier/dashboard/ClosedBids.vue')
  },
  {
    path: '/supplier/dashbard/letters',
    name: 'SupplierDashboardLetters',
    component: () => import('../views/supplier/dashboard/Letters.vue')
  },
  {
    path: '/supplier/prequal/ordered/categories',
    name: 'SupplierPrequalOrderedCategories',
    component: () => import('../views/supplier/prequal/category/OrderedCategories.vue')
  },
  {
    path: '/supplier/prequal/category/instructions/:category_id',
    name: 'SupplierPrequalCategoryInstructions',
    component: () => import('../views/supplier/prequal/category/Instructions.vue')
  },
  {
    path: '/supplier/prequal/preview/:category_id',
    name: 'SupplierPrequalPreview',
    component: () => import('../views/supplier/prequal/category/QuestionPreview.vue')
  },
  {
    path: '/supplier/prequal/category/bid/:category_id',
    name: 'SupplierPrequalCategoryBid',
    component: () => import('../views/supplier/prequal/category/Bid.vue')
  },
    {
    path: '/supplier/tender/ordered/categories',
    name: 'SupplierTenderOrderedCategories',
    component: () => import('../views/supplier/tender/category/technical/OrderedCategories.vue')
  },
  {
    path: '/supplier/tender/category/instructions/:category_id',
    name: 'SupplierTenderCategoryInstructions',
    component: () => import('../views/supplier/tender/category/technical/Instructions.vue')
  },
  {
    path: '/supplier/tender/category/bid/:category_id',
    name: 'SupplierTenderCategoryBid',
    component: () => import('../views/supplier/tender/category/technical/Bid.vue')
  },
  {
    path: '/supplier/tender/category/financial/bid/:category_id',
    name: 'SupplierTenderCategoryFinancialBid',
    component: () => import('../views/supplier/tender/category/financial/Bid.vue')
  },
  {
    path: '/supplier/tender/category/advanced/financial/bid/:category_id',
    name: 'SupplierTenderCategoryAdvancedFinancialBid',
    component: () => import('../views/supplier/tender/category/financial/AdvancedBid.vue')
  },
  {
    path: '/supplier/tender/category/item/template/generation/progress/:category_id/:task_id',
    name: 'SupplierTenderCategoryItemGenerationProgress',
    component: () => import('../views/supplier/tender/category/financial/TemplateGenProgress.vue')
  },
    {
    path: '/supplier/tender/preview/:category_id',
    name: 'SupplierTenderPreview',
    component: () => import('../views/supplier/tender/category/technical/QuestionPreview.vue')
  },
   // Supplier System Management urls
   {
    path: '/supplier/user/users',
    name: 'SupplierUserManagementUsers',
    component: () => import('../views/supplier/system_management/users/Users.vue')
  },
  {
    path: '/supplier/user/users/create',
    name: 'SupplierUserManagementUsersCreate',
    component: () => import('../views/supplier/system_management/users/CreateUser.vue')
  },
  {
    path: '/supplier/user/users/:id/update',
    name: 'SupplierUserManagementUsersUpdate',
    component: () => import('../views/supplier/system_management/users/UpdateUser.vue')
  },
  {
    path: '/supplier/user/roles',
    name: 'SupplierUserManagementRoles',
    component: () => import('../views/supplier/system_management/roles/Roles.vue')
  },
  {
    path: '/supplier/user/roles/create',
    name: 'SupplierUserManagementRolesCreate',
    component: () => import('../views/supplier/system_management/roles/CreateRole.vue')
  },
  {
    path: '/supplier/user/roles/:id/update',
    name: 'SupplierUserManagementRolesUpdate',
    component: () => import('../views/supplier/system_management/roles/UpdateRole.vue')
  },
  {
    path: '/supplier/user/roles/:id/privileges',
    name: 'SupplierUserManagementRolesPrivileges',
    component: () => import('../views/supplier/system_management/roles/Privileges.vue')
  },
  {
    path: '/supplier/user/logs',
    name: 'SupplierUserManagementLogs',
    component: () => import('../views/supplier/system_management/logs/Logs.vue')
  },
  // QED urls
  {
    path: '/qed/livejobs/',
    name: 'QedLiveJobs',
    component: () => import('../views/qed/dashboard/live/Jobs.vue')
  },
  {
    path: '/qed/livejobs/:jobId/:sourcing_activity/categories',
    name: 'QedLiveJobCategories',
    component: () => import('../views/qed/dashboard/live/Categories.vue')
  },
  {
    path: '/qed/livejobs/categories/:categoryId/participants',
    name: 'QedLiveJobParticipants',
    component: () => import('../views/qed/dashboard/live/Participants.vue')
  },
  {
    path: '/qed/jobs/buyers/',
    name: 'QedDashboardJobsBuyers',
    component: () => import('../views/qed/dashboard/jobs/Buyers.vue')
  },
  {
    path: '/qed/buyers/:buyerId/jobs/',
    name: 'QedDashboardJobsBuyersJobs',
    component: () => import('../views/qed/dashboard/jobs/Jobs.vue')
  },
  {
    path: '/qed/buyers/',
    name: 'QedBuyers',
    component: () => import('../views/qed/dashboard/buyers/Buyers.vue')
  },
  {
    path: '/qed/buyers/create',
    name: 'QedBuyersCreate',
    component: () => import('../views/qed/dashboard/buyers/CreateBuyer.vue')
  },
  {
    path: '/qed/buyers/:buyerId/update',
    name: 'QedBuyersUpdate',
    component: () => import('../views/qed/dashboard/buyers/UpdateBuyer.vue')
  },
  {
    path: '/qed/buyers/:buyerId/buyer',
    name: 'QedBuyersBuyer',
    component: () => import('../views/qed/dashboard/buyers/Buyer.vue')
  },
  {
    path: '/qed/buyers/:buyerId/users/create',
    name: 'QedBuyersBuyerUser',
    component: () => import('../views/qed/dashboard/buyers/CreateBuyerUser.vue')
  },
  {
    path: '/qed/savings/',
    name: 'QedSavings',
    component: () => import('../views/qed/dashboard/savings/Savings.vue')
  },
  {
    path: '/qed/savings/:id/buyer',
    name: 'QedBuyerSavings',
    component: () => import('../views/qed/dashboard/savings/BuyerSavings.vue')
  },
  {
    path: '/qed/category/types',
    name: 'QedCategoryTypes',
    component: () => import('../views/qed/system_management/category_types/List.vue')
  },
  {
    path: '/qed/category/type/:id',
    name: 'QedCategoryType',
    component: () => import('../views/qed/system_management/category_types/Details.vue')
  },
  {
    path: '/qed/category/types/create',
    name: 'QedCategoryTypeCreate',
    component: () => import('../views/qed/system_management/category_types/CreateCategoryType.vue')
  },
  {
    path: '/qed/category/types/edit/:category_type_id',
    name: 'QedCategoryTypeEdit',
    component: () => import('../views/qed/system_management/category_types/EditCategoryType.vue')
  },
  {
    path: '/qed/category/criteria/create/:category_type_id/:location_id',
    name: 'QedCategoryCriteriaCreate',
    component: () => import('../views/qed/system_management/category_types/CreateCategoryCriteria.vue')
  },
  {
    path: '/qed/category/criteria/edit/:category_type_id/:criteria_id',
    name: 'QedCategoryCriteriaEdit',
    component: () => import('../views/qed/system_management/category_types/EditCategoryCriteria.vue')
  },
  // Buyer urls
  {
    path: '/buyer/dashboard',
    name: 'BuyerDashboard',
    component: () => import('../views/company/dashboard/Dashboard.vue')
  },
  {
    path: '/buyer/livejobs/',
    name: 'BuyerLiveJobs',
    component: () => import('../views/company/dashboard/live/Jobs.vue')
  },
  {
    path: '/buyer/livejobs/:jobId/:sourcing_activity/categories',
    name: 'BuyerLiveJobCategories',
    component: () => import('../views/company/dashboard/live/Categories.vue')
  },
  {
    path: '/buyer/livejobs/categories/:categoryId/participants',
    name: 'BuyerLiveJobParticipants',
    component: () => import('../views/company/dashboard/live/Participants.vue')
  },
  {
    path: '/buyer/ourjobs/',
    name: 'BuyerOurJobs',
    component: () => import('../views/company/dashboard/OurJobs.vue')
  },
  {
    path: '/buyer/savings/',
    name: 'BuyerSavings',
    component: () => import('../views/company/dashboard/Savings.vue')
  },
  // Risk Management urls

  {
    path: '/buyer/list/risk-management',
    name: 'BuyerListRiskManagement',
    component: () => import('../views/company/risk_management/List.vue')
  },
  {
    path: '/supplier/list/risk-management',
    name: 'SupplierListRiskManagement',
    component: () => import('../views/supplier/risk_management/List.vue')
  },
  {
    path: '/qed/list/risk-management',
    name: 'QedListRiskManagement',
    component: () => import('../views/qed/risk_management/List.vue')
  },
  {
    path: '/buyer/add/job/risk-management',
    name: 'BuyerAddRiskManagement',
    component: () => import('../views/company/risk_management/Job/AddJob.vue')
  },
  {
    path: '/buyer/add/category/job/:riskId/risk-management',
    name: 'BuyerAddCategoryRiskManagement',
    component: () => import('../views/company/risk_management/Job/Category/AddCategory.vue')
  },
  {
    path: '/buyer/details/job/:riskId/risk-management/',
    name: 'BuyerDetailsRiskManagement',
    component: () => import('../views/company/risk_management/Job/DetailsJob.vue')
  },
  {
    path: '/buyer/reports/job/:riskId/risk-management/',
    name: 'BuyerReportsRiskManagement',
    component: () => import('../views/company/risk_management/ReportsJob.vue')
  },
  {
    path: '/buyer/category/:riskId/:categoryId/risk-management/',
    name: 'BuyerCategoryDetailsRiskManagement',
    component: () => import('../views/company/risk_management/Job/Category/DetailsCategory.vue')
  },
  {
    path: '/buyer/section/:categoryId/:sectionId/risk-management/',
    name: 'BuyerSectionDetailsRiskManagement',
    component: () => import('../views/company/risk_management/Job/Category/Section/DetailsSection.vue')
  },
  {
    path: '/buyer/add/section/:categoryId/risk-management/',
    name: 'BuyerAddSectionRiskManagement',
    component: () => import('../views/company/risk_management/Job/Category/Section/AddSection.vue')
  },
  {
    path: '/buyer/add/question/:sectionId/risk-management/',
    name: 'BuyerAddQuestionRiskManagement',
    component: () => import('../views/company/risk_management/Job/Category/Section/Question/AddQuestion.vue')
  },
  {
    path: '/buyer/edit/question/:sectionId/:questionId/risk-management/',
    name: 'BuyerQuestionEditRiskManagement',
    component: () => import('../views/company/risk_management/Job/Category/Section/Question/EditQuestion.vue')
  },
  {
    path: '/buyer/edit/section/:categoryId/:sectionId/risk-management/',
    name: 'BuyerSectionEditRiskManagement',
    component: () => import('../views/company/risk_management/Job/Category/Section/EditSection.vue')
  },
  {
    path: '/buyer/add/ra/:categoryId/risk-management/',
    name: 'BuyerAddRiskAssessmentRiskManagement',
    component: () => import('../views/company/risk_management/Job/Category/QualityAssurance/Initiate_ra.vue')
  },
  {
    path: '/buyer/add/ra/instructions/:categoryId/:raId/risk-management/',
    name: 'BuyerAddInstructionsRiskAssessmentRiskManagement',
    component: () => import('../views/company/risk_management/Job/Category/QualityAssurance/Provide_ra_instructions.vue')
  },
  {
    path: '/buyer/list/ra/:categoryId/risk-management/',
    name: 'BuyerListRiskAssessmentsRiskManagement',
    component: () => import('../views/company/risk_management/Job/Category/QualityAssurance/List.vue')
  },
  {
    path: '/buyer/ra/:categoryId/:raId/risk-management/',
    name: 'BuyerDetailsRiskAssessmentRiskManagement',
    component: () => import('../views/company/risk_management/Job/Category/QualityAssurance/Conduct_ra.vue')
  },

  //Suppliers Auction
  {
    path: '/supplier/list/reverse/auction',
    name: 'SupplierDetailsReverseAuction',
    component: () => import('../views/supplier/auction/reverse_auctions/List.vue')
  },
  {
    path: '/supplier/list/foward/auction',
    name: 'SupplierDetailsFowardAuction',
    component: () => import('../views/supplier/auction/foward_auctions/List.vue')
  },
  {
    path: '/supplier/:auctionId/foward/auction',
    name: 'SupplierParticipateFowardAuction',
    component: () => import('../views/supplier/auction/foward_auctions/Participate.vue')
  },
  {
    path: '/supplier/:auctionId/reverse/auction',
    name: 'SupplierParticipateReverseAuction',
    component: () => import('../views/supplier/auction/reverse_auctions/Participate.vue')
  },
  {
    path: '/supplier/bid/:auctionId/foward/auction',
    name: 'SupplierBidFowardAuction',
    component: () => import('../views/supplier/auction/foward_auctions/Bid.vue')
  },
  // Test New Day
  {
    path: '/supplier/bid/:auctionId/test/auction',
    name: 'SupplierBidTestAuction',
    component: () => import('../views/supplier/auction/reverse_auctions/Bid_Auction.vue')
  },
  {
    path: '/supplier/bid/:auctionId/reverse/auction',
    name: 'SupplierBidReverseAuction',
    component: () => import('../views/supplier/auction/reverse_auctions/Bid.vue')
  },
  // Contracts
  {
    path: '/buyer/contracts/supplier/categories/:categoryId/suppliers',
    name: 'BuyerContractsSupplierCategorySuppliers',
    component: () => import('../views/company/contracts/supplier/Suppliers.vue')
  },
  {
    path: '/buyer/contracts/supplier/contract/create',
    name: 'BuyerContractsSupplierCreate',
    component: () => import('../views/company/contracts/supplier/CreateContract.vue')
  },
  {
    path: '/buyer/contracts/supplier/contract/:contractId/update',
    name: 'BuyerContractsSupplierUpdate',
    component: () => import('../views/company/contracts/supplier/UpdateContract.vue')
  },
  // System Management urls
  {
    path: '/buyer/user/users',
    name: 'BuyerUserManagementUsers',
    component: () => import('../views/company/system_management/users/Users.vue')
  },
  {
    path: '/buyer/user/users/create',
    name: 'BuyerUserManagementUsersCreate',
    component: () => import('../views/company/system_management/users/CreateUser.vue')
  },
  {
    path: '/buyer/user/users/:id/update',
    name: 'BuyerUserManagementUsersUpdate',
    component: () => import('../views/company/system_management/users/UpdateUser.vue')
  },
  {
    path: '/buyer/user/roles',
    name: 'BuyerUserManagementRoles',
    component: () => import('../views/company/system_management/roles/Roles.vue')
  },
  {
    path: '/buyer/user/roles/create',
    name: 'BuyerUserManagementRolesCreate',
    component: () => import('../views/company/system_management/roles/CreateRole.vue')
  },
  {
    path: '/buyer/user/roles/:id/update',
    name: 'BuyerUserManagementRolesUpdate',
    component: () => import('../views/company/system_management/roles/UpdateRole.vue')
  },
  {
    path: '/buyer/user/roles/:id/privileges',
    name: 'BuyerUserManagementRolesPrivileges',
    component: () => import('../views/company/system_management/roles/Privileges.vue')
  },
  {
    path: '/buyer/user/logs',
    name: 'BuyerUserManagementLogs',
    component: () => import('../views/company/system_management/logs/Logs.vue')
  },
  //RFQ Urls

  // create RFQ
  {
    path: '/company/create/rfq',
    name: 'CompanyRfqCreate',
    component: () => import('../views/company/rfq/Create.vue')
  },
  // RFQ Details
  {
    path: '/company/rfq/details/:id',
    name: 'CompanyRfqDetails',
    component: () => import('../views/company/rfq/Details.vue')
  },
  // create RFQ category
  {
    path: '/company/rfq/create/category/:id',
    name: 'CompanyRfqCategoryCreate',
    component: () => import('../views/company/rfq/category/Create.vue')
  },
  // RFQ category details
  {
    path: '/company/rfq/category/details/:rfq_id/:category_id',
    name: 'CompanyRfqCategoryDetails',
    component: () => import('../views/company/rfq/category/Details.vue')
  },
  // RFQ edit category
  {
    path: '/company/rfq/edit/category/:rfq_id/:category_id',
    name: 'CompanyRfqCategoryEdit',
    component: () => import('../views/company/rfq/category/Edit.vue')
  },
  //RFQ Invited suppliers
  {
    path: '/company/rfq/invited/suppliers/:rfq_id/:category_id',
    name: 'CompanyRfqInvitedSupplier',
    component: () => import('../views/company/rfq/category/invitees/Invitees.vue')
  },
  //RFQ Invite bidders from prequal
  {
    path: '/company/rfq/invite/suppliers/:rfq_id/:category_id',
    name: 'CompanyRfqInviteSuppliers',
    component: () => import('../views/company/rfq/category/invitees/InviteSupplierPrequal.vue')
  },
  //RFQ Supplier List
  {
    path: '/supplier/list/rfqs',
    name: 'SupplierRFQList',
    component: () => import('../views/supplier/rfq/List.vue')
  },
  {
    path: '/supplier/apply/rfq/:category_id',
    name: 'SupplierRfqApply',
    component: () => import('../views/supplier/rfq/Apply.vue')
  },
  {
    path: '/supplier/apply/rfq/advanced/:category_id',
    name: 'supplierApplyAdvancedRFQ',
    component: () => import('../views/supplier/rfq/advanced_rfq/Apply.vue')
  },
  {
    path: '/supplier/rfq/category/item/template/generation/progress/:category_id/:task_id',
    name: 'SupplierRFQCategoryItemGenerationProgress',
    component: () => import('../views/supplier/rfq/advanced_rfq/TemplateGenProgress.vue')
  },
  //RFQ Job Reports
  {
    path: '/company/rfq/job/reports/:rfq_id',
    name: 'CompanyRfqJobReports',
    component: () => import('../views/company/rfq/reports/List.vue')
  },
  {
    path: '/company/rfq/report/progress/:prequal_id/:task_id',
    name: 'companyRFQProgress',
    component: () => import('../views/company/rfq/reports/Progress.vue')
  },
  {
    path: '/company/rfq/category/upload/progress/:category_id/:task_id',
    name: 'companyRFQCategoryUploadProgress',
    component: () => import('../views/company/rfq/category/UploadProgress.vue')
  },
  {
    path: '/company/rfq/category/download/progress/:category_id/:task_id',
    name: 'companyRFQCategoryDownloadProgress',
    component: () => import('../views/company/rfq/category/DownloadProgress.vue')
  },
  {
    path: '/company/rfq/cat/suppliers/progress/:tender_id/:task_id/',
    name: 'CompanyRFQCatSuppliers',
    component: () => import('../views/company/rfq/RFQCatSupplierProgress.vue')
  },
  // Archive
  // Buyer
  {
    path: '/company/archive/jobs',
    name: 'SWCompanyArchiveJobs',
    component: () => import('../views/company/archive/Jobs.vue')
  },
  {
    path: '/company/archive/jobs/:jobId/:sourcing_activity/categories',
    name: 'SWCompanyArchiveJobsCategories',
    component: () => import('../views/company/archive/Categories.vue')
  },
  {
    path: '/company/archive/jobs/:jobId/:sourcing_activity/categories/:categoryId/suppliers',
    name: 'SWCompanyArchiveJobsCategorySuppliers',
    component: () => import('../views/company/archive/Suppliers.vue')
  },
  {
    path: '/company/archive/:sourcing_activity/categories/:categoryId/suppliers/:supplierId',
    name: 'SWCompanyArchiveSupplierDocuments',
    component: () => import('../views/company/archive/SupplierDocuments.vue')
  },
  // Supplier
  {
    path: '/supplier/archive/companies',
    name: 'SWCompanyArchiveCompanies',
    component: () => import('../views/supplier/archive/Companies.vue')
  },
  {
    path: '/supplier/archive/companies/:companyId/categories',
    name: 'SWCompanyArchiveCompanyCategories',
    component: () => import('../views/supplier/archive/Categories.vue')
  },
  {
    path: '/supplier/archive/:jobType/categories/:categoryId/documents',
    name: 'SWCompanyArchiveCompanyCategoriesDocuments',
    component: () => import('../views/supplier/archive/SupplierDocuments.vue')
  },
    // company prequal urls
    ...company_prequal,
    // end of company prequal urls

     // company tender urls
    ...company_tender,
    // end of company tender urls

    // qed project management urls
    ...qed_project_management,
    // end of qed project management urls

    // company project management urls
    ...company_project_management,
    // end of company project management urls

    // qed user management urls
    ...qed_user_management,
    // end of qed user management urls

    // qed archive urls
    ...qed_archive,
    // end of qed archive urls

    // // qed auction urls
    // ...qed_auction,
    // // end of qed auction urls

    // company auction urls
    ...company_auction,
    // end of company auction urls
    // qed prequal urls
    ...qed_prequal,
    // end of qed prequal urls

    // qed tender urls
    ...qed_tender,
    // end of qed tender urls

    // qed rfq urls
    ...qed_rfq,
    // end of qed rfq urls
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  scrollBehavior () {
    return { x: 0, y: 0 }
  }
})

router.beforeEach((to, from, next) => {
  const authExceptions = ['Login', 'Register', 'ResetPassword', 'SetPassword', 'ActivateAccount']
  if (authExceptions.includes(to.name) === false && store.state.Auth.authUser === null) next({ name: 'Login' })
  else next()
});

export default router
