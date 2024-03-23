// import Vue from 'vue'
// import VueRouter from 'vue-router'

// Vue.use(VueRouter)

// const routes = [
//     {
//         path: '/qed/list/foward/auction',
//         name: 'QedListFowardAuction',
//         component: () => import('../views/company/auction/foward_auctions/List.vue')
//     },
//     {
//         path: '/qed/list/reverse/auction',
//         name: 'QedListReverseAuction',
//         component: () => import('../views/company/auction/reverse_auctions/List.vue')
//     },
//     {
//         path: '/qed/add/foward/auction',
//         name: 'QedAddFowardAuction',
//         component: () => import('../views/company/auction/foward_auctions/AddAuction.vue')
//     },
//     {
//         path: '/qed/add/reverse/auction',
//         name: 'QedAddReverseAuction',
//         component: () => import('../views/company/auction/reverse_auctions/AddAuction.vue')
//     },
//     {
//         path: '/qed/:auctionId/foward/auction',
//         name: 'QedDetailsFowardAuction',
//         component: () => import('../views/company/auction/foward_auctions/DetailsAuction.vue')
//     },
//     {
//         path: '/qed/:auctionId/reverse/auction',
//         name: 'QedDetailsReverseAuction',
//         component: () => import('../views/company/auction/reverse_auctions/DetailsAuction.vue')
//     },
//     {
//         path: '/qed/reverse/:auctionId/auction/add/item',
//         name: 'QedReverseAuctionAddItem',
//         component: () => import('../views/company/auction/reverse_auctions/item/AddItem.vue')
//     },
//     {
//         path: '/qed/foward/:auctionId/auction/add/item',
//         name: 'QedFowardAuctionAddItem',
//         component: () => import('../views/company/auction/foward_auctions/item/AddItem.vue')
//     },
//     {
//         path: '/qed/item/:auctionId/:itemId/foward/auction',
//         name: 'QedItemDetailsFowardAuction',
//         component: () => import('../views/company/auction/foward_auctions/item/DetailsItem.vue')
//     },
//     {
//         path: '/qed/item/:auctionId/:itemId/reverse/auction',
//         name: 'QedItemDetailsReverseAuction',
//         component: () => import('../views/company/auction/reverse_auctions/item/DetailsItem.vue')
//     },
// ]

// export default routes