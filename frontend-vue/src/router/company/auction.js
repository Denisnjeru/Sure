import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    // List Auction
    {
        path: '/buyer/list/foward/auction',
        name: 'BuyerListFowardAuction',
        component: () => import('../../views/company/auction/foward_auctions/List.vue')
    },
    {
        path: '/buyer/list/reverse/auction',
        name: 'BuyerListReverseAuction',
        component: () => import('../../views/company/auction/reverse_auctions/List.vue')
    },

    // Add Auction
    {
        path: '/buyer/add/foward/auction',
        name: 'BuyerAddFowardAuction',
        component: () => import('../../views/company/auction/foward_auctions/AddAuction.vue')
    },
    {
        path: '/buyer/add/reverse/auction',
        name: 'BuyerAddReverseAuction',
        component: () => import('../../views/company/auction/reverse_auctions/AddAuction.vue')
    },

    // Edit Auction
    {
        path: '/buyer/edit/:auctionId/reverse/auction',
        name: 'BuyerEditReverseAuction',
        component: () => import('../../views/company/auction/reverse_auctions/EditAuction.vue')
    },
    {
        path: '/buyer/edit/:auctionId/foward/auction',
        name: 'BuyerEditFowardAuction',
        component: () => import('../../views/company/auction/foward_auctions/EditAuction.vue')
    },

    // Details Auction
    {
        path: '/buyer/:auctionId/foward/auction',
        name: 'BuyerDetailsFowardAuction',
        component: () => import('../../views/company/auction/foward_auctions/DetailsAuction.vue')
    },
    {
        path: '/buyer/:auctionId/reverse/auction',
        name: 'BuyerDetailsReverseAuction',
        component: () => import('../../views/company/auction/reverse_auctions/DetailsAuction.vue')
    },

    // Invited Participants 
    {
        path: '/buyer/inivited/suppliers/:auctionId/reverse/auction',
        name: 'BuyerInvitedParticipantsReverseAuction',
        component: () => import('../../views/company/auction/reverse_auctions/invitees/Invitees.vue')
    },
    {
        path: '/buyer/inivited/suppliers/:auctionId/foward/auction',
        name: 'BuyerInvitedParticipantsFowardAuction',
        component: () => import('../../views/company/auction/foward_auctions/invitees/Invitees.vue')
    },

    // Add Item
    {
        path: '/buyer/reverse/:auctionId/auction/add/item',
        name: 'BuyerReverseAuctionAddItem',
        component: () => import('../../views/company/auction/reverse_auctions/item/AddItem.vue')
    },
    {
        path: '/buyer/foward/:auctionId/auction/add/item',
        name: 'BuyerFowardAuctionAddItem',
        component: () => import('../../views/company/auction/foward_auctions/item/AddItem.vue')
    },

    // Edit Item
    {
        path: '/buyer/reverse/:auctionId/:itemId/auction/edit/item',
        name: 'BuyerReverseAuctionAddItem',
        component: () => import('../../views/company/auction/reverse_auctions/item/EditItem.vue')
    },
    {
        path: '/buyer/foward/:auctionId/:itemId/auction/edit/item',
        name: 'BuyerFowardAuctionAddItem',
        component: () => import('../../views/company/auction/foward_auctions/item/EditItem.vue')
    },

    // Details Item
    {
        path: '/buyer/item/:auctionId/:itemId/foward/auction',
        name: 'BuyerItemDetailsFowardAuction',
        component: () => import('../../views/company/auction/foward_auctions/item/DetailsItem.vue')
    },
    {
        path: '/buyer/item/:auctionId/:itemId/reverse/auction',
        name: 'BuyerItemDetailsReverseAuction',
        component: () => import('../../views/company/auction/reverse_auctions/item/DetailsItem.vue')
    },
    
    // Download Progress Auction Page
    {
        path: '/company/auction/download/progress/:task_id',
        name: 'companyAuctionDownloadProgress',
        component: () => import('../../views/company/auction/DownloadProgress.vue')
    },

    // Uplaod Multiple Images
    {
        path: '/uploadmultiple',
        name: 'uploadmultiple',
        component: () => import('../../views/company/auction/uploadmultiple')
    },
]

export default routes