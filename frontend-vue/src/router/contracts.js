const routes = [
    {
        path: '/supplier/contracts',
        name: 'SupplierContracts',
        component: () => import('../views/supplier/contracts/Contracts.vue')
    },
    {
      path: '/qed/contracts/buyer',
      name: 'QedContractsBuyers',
      component: () => import('../views/qed/contracts/buyer/Buyers.vue')
    },
    {
      path: '/qed/contracts/buyer/:buyerId/contracts',
      name: 'QedContractsBuyerContracts',
      component: () => import('../views/qed/contracts/buyer/Contracts.vue')
    },
    {
      path: '/qed/contracts/buyer/:buyerId/jobs',
      name: 'QedContractsBuyerJobs',
      component: () => import('../views/qed/contracts/buyer/Jobs.vue')
    },
    {
      path: '/qed/contracts/buyer/contract/:contractId/update',
      name: 'QedContractsBuyerUpdate',
      component: () => import('../views/qed/contracts/buyer/UpdateContract.vue')
    },
    {
      path: '/qed/contracts/buyer/contract/create',
      name: 'QedContractsBuyerCreate',
      component: () => import('../views/qed/contracts/buyer/CreateContract.vue')
    },
    {
      path: '/buyer/contracts/sections',
      name: 'BuyerContractsTemplatesSections',
      component: () => import('../views/company/contracts/sections/Sections.vue')
    },
    {
      path: '/buyer/contracts/sections/:sectionId/view',
      name: 'BuyerContractsTemplatesSection',
      component: () => import('../views/company/contracts/sections/Section.vue')
    },
    {
      path: '/buyer/contracts/sections/create',
      name: 'BuyerContractsTemplatesSectionsCreate',
      component: () => import('../views/company/contracts/sections/CreateSection.vue')
    },
    {
      path: '/buyer/contracts/sections/:sectionId/update',
      name: 'BuyerContractsTemplatesSectionsUpdate',
      component: () => import('../views/company/contracts/sections/UpdateSection.vue')
    },
    {
      path: '/buyer/contracts/templates',
      name: 'BuyerContractsTemplatesTemplates',
      component: () => import('../views/company/contracts/templates/Templates.vue')
    },
    {
      path: '/buyer/contracts/templates/:templateId/view',
      name: 'BuyerContractsTemplatesTemplate',
      component: () => import('../views/company/contracts/templates/Template.vue')
    },
    {
      path: '/buyer/contracts/templates/:templateId/update',
      name: 'BuyerContractsTemplatesTemplatesUpdate',
      component: () => import('../views/company/contracts/templates/UpdateTemplate.vue')
    },
    {
      path: '/buyer/contracts/templates/create',
      name: 'BuyerContractsTemplatesTemplatesCreate',
      component: () => import('../views/company/contracts/templates/CreateTemplate.vue')
    },
    {
      path: '/buyer/contracts/qed',
      name: 'BuyerContractsQed',
      component: () => import('../views/company/contracts/qed/Contracts.vue')
    },
    {
      path: '/buyer/contracts/qed/:contractId/update',
      name: 'BuyerContractsQedUpdate',
      component: () => import('../views/company/contracts/qed/UpdateContract.vue')
    },
    {
      path: '/buyer/contracts/supplier/jobs',
      name: 'BuyerContractsSupplierJobs',
      component: () => import('../views/company/contracts/supplier/Jobs.vue')
    },
    {
      path: '/buyer/contracts/supplier/jobs/:jobId/:sourcing_activity/categories',
      name: 'BuyerContractsSupplierCategories',
      component: () => import('../views/company/contracts/supplier/Categories.vue')
    },
    {
      path: '/buyer/contracts/supplier/categories/:categoryId/contracts',
      name: 'BuyerContractsSupplierCategoryContracts',
      component: () => import('../views/company/contracts/supplier/Contracts.vue')
    },
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
]

export default routes;