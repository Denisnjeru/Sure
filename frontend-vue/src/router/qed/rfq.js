const routes = [
    {
        path: '/qed/rfq/buyers',
        name: 'QedSourcingRfqBuyers',
        component: () => import('../../views/qed/rfq/Buyers.vue')
    },
    {
        path: '/qed/rfqs',
        name: 'QedSourcingRfqs',
        component: () => import('../../views/qed/rfq/List.vue')
    },
    // create RFQ
    {
        path: '/qed/create/rfq',
        name: 'QedSourcingRfqCreate',
        component: () => import('../../views/qed/rfq/Create.vue')
    },
    // RFQ Details
    {
        path: '/qed/rfq/details/:id',
        name: 'QedSourcingRfqDetails',
        component: () => import('../../views/qed/rfq/Details.vue')
    },
    // create RFQ category
    {
        path: '/qed/rfq/create/category/:id',
        name: 'QedSourcingRfqCategoryCreate',
        component: () => import('../../views/qed/rfq/category/Create.vue')
    },
    // RFQ category details
    {
        path: '/qed/rfq/category/details/:rfq_id/:category_id',
        name: 'QedSourcingRfqCategoryDetails',
        component: () => import('../../views/qed/rfq/category/Details.vue')
    },
    // RFQ edit category
    {
        path: '/qed/rfq/edit/category/:rfq_id/:category_id',
        name: 'QedSourcingRfqCategoryEdit',
        component: () => import('../../views/qed/rfq/category/Edit.vue')
    },
    //RFQ Invited suppliers
    {
        path: '/qed/rfq/invited/suppliers/:rfq_id/:category_id',
        name: 'QedSourcingRfqInvitedSupplier',
        component: () => import('../../views/qed/rfq/category/invitees/Invitees.vue')
    },
    //RFQ Invite bidders from prequal
    {
        path: '/qed/rfq/invite/suppliers/:rfq_id/:category_id',
        name: 'QedSourcingRfqInviteSuppliers',
        component: () => import('../../views/qed/rfq/category/invitees/InviteSupplierPrequal.vue')
    },
    //RFQ Job Reports
    {
        path: '/qed/rfq/job/reports/:rfq_id',
        name: 'QedSourcingRfqJobReports',
        component: () => import('../../views/qed/rfq/reports/List.vue')
    },
    {
        path: '/qed/rfq/report/progress/:prequal_id/:task_id',
        name: 'QedSourcingRfqProgress',
        component: () => import('../../views/qed/rfq/reports/Progress.vue')
    },
    {
        path: '/qed/rfq/category/upload/progress/:category_id/:task_id',
        name: 'QedSourcingRfqCategoryUploadProgress',
        component: () => import('../../views/qed/rfq/category/UploadProgress.vue')
    },
    {
        path: '/qed/rfq/category/download/progress/:category_id/:task_id',
        name: 'QedSourcingRfqCategoryDownloadProgress',
        component: () => import('../../views/qed/rfq/category/DownloadProgress.vue')
    },
    {
        path: '/qed/rfq/cat/suppliers/progress/:tender_id/:task_id/',
        name: 'QedSourcingRfqCatSuppliers',
        component: () => import('../../views/qed/rfq/RFQCatSupplierProgress.vue')
    },
]

export default routes;