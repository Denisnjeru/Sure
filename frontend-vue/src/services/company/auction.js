import api from '../../apiV1/api';

const auctions = {
// Buyer Urls
    reverseAuctions(){
        return new Promise((resolve, reject) => {
            api.get(`/auction/?format=datatables&search=${"Reverse Auction"}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });  
    },
    createReverseAuctions(content){
        return new Promise((resolve, reject) =>{
            api.post(`/auction/`, content, (data) =>{
                resolve(data);
            }, (error) =>{
                reject(error);
            });
        });
    },
    fowardAuctions(){
        return new Promise((resolve, reject) => {
            api.get(`/auction/?format=datatables&search=${"Forward Auction"}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });  
    },
    createFowardAuctions(content){
        return new Promise((resolve, reject) =>{
            api.post(`/auction/`, content, (data) =>{
                resolve(data);
            }, (error) =>{
                reject(error);
            });
        });
    },
    getRetrieveAuction(auctionID){
        return new Promise((resolve, reject) =>{
            api.get(`/auction/${auctionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateAuction(auctionID, content) {
        return new Promise((resolve, reject) => {
            api.patch(`/auction/${auctionID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteAuction(auctionID){
        return new Promise((resolve, reject) =>{
            api.delete(`/auction/${auctionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    addAuctionItem(auctionID, content){
        return new Promise((resolve, reject) =>{
            api.post(`/auction/items/${auctionID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    getAuctionItem(auctionID, auctionItemId){
        return new Promise((resolve, reject) =>{
            api.get(`/auction/items/${auctionID}/${auctionItemId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateAuctionItem(auctionID, auctionItemId, content) {
        return new Promise((resolve, reject) =>{
            api.patch(`/auction/items/${auctionID}/${auctionItemId}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteAuctionItem(auctionID, auctionItemId){
        return new Promise((resolve, reject) =>{
            api.delete(`/auction/items/${auctionID}/${auctionItemId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },

    //Supplier Urls

    supplierReverseAuctions(){
        return new Promise((resolve, reject) => {
            api.get(`/auction/supplier/list_retrieve/?search=${"Reverse Auction"}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });  
    },
    supplierFowardAuctions(){
        return new Promise((resolve, reject) => {
            api.get(`/auction/supplier/list_retrieve/?search=${"Foward Auction"}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });  
    },
    getSupplierAuction(auctionID){
        return new Promise((resolve, reject) =>{
            api.get(`/auction/supplier/list_retrieve/${auctionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    closeAuction(auction_id){
        return new Promise((resolve, reject) => {
            api.get(`/auction/close/${auction_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    auctionInviteSuppliers(content,auction_id) {
        return new Promise((resolve, reject) => {
            api.post(`/auction/invite_suppliers/${auction_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    // download/auction_items/template/
    auctionDownloadBidTemplate(auction_id){
        return new Promise((resolve, reject) => {
            api.get(`/auction/download/auction_bids/template/${auction_id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    auctionDownloadItemTemplate(auction_id){
        return new Promise((resolve, reject) => {
            api.get(`/auction/download/auction_items/template/${auction_id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    upload_aution_items(auction_id, form_data) {
        return new Promise((resolve, reject) => {
            api.post(`/auction/upload/auction/items/${auction_id}/`, form_data, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}


export default auctions
