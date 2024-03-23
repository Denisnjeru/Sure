import api from '../../apiV1/api';

const auctions = {
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
    auctionResponses(auctionID){
        return new Promise((resolve, reject) =>{
            api.get(`/supplier/auction/participating/responses/${auctionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    bid(item_id, content){
        return new Promise((resolve, reject) => {
            api.post(`/supplier/auction/participating/bid/${item_id}/`,content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default auctions;