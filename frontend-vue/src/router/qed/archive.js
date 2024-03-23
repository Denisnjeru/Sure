const routes = [
    {
        path: '/qed/archive/buyers',
        name: 'BWQedArchiveBuyers',
        component: () => import('../../views/qed/archive/Companies.vue')
    },
    {
        path: '/qed/archive/buyers/:buyerId/jobs',
        name: 'BWQedArchiveJobs',
        component: () => import('../../views/qed/archive/Jobs.vue')
    },
    {
        path: '/qed/archive/jobs/:jobId/:sourcing_activity/categories',
        name: 'BWQedArchiveJobsCategories',
        component: () => import('../../views/qed/archive/Categories.vue')
    },
    {
        path: '/qed/archive/jobs/:jobId/:sourcing_activity/categories/:categoryId/suppliers',
        name: 'BWQedArchiveJobsCategorySuppliers',
        component: () => import('../../views/qed/archive/Suppliers.vue')
    },
    {
        path: '/qed/archive/:sourcing_activity/categories/:categoryId/suppliers/:supplierId',
        name: 'BWQedArchiveSupplierDocuments',
        component: () => import('../../views/qed/archive/SupplierDocuments.vue')
    },
]

export default routes;