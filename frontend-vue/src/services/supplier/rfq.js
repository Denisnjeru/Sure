import api from '../../apiV1/api';

const supplierRfq = {
    //Supplier RFQ list
    rfqs(page) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/rfqs/?page=${page}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqDetails(category_id){
        return new Promise((resolve, reject) => {
            api.get(`/supplier/rfqs/apply/rfq/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    supplierRfqParticipation(category_id, supplier_id, page){
        return new Promise((resolve, reject) => {
            api.get(`/supplier/rfqs/supplier/rfq/participation_status/${category_id}/${supplier_id}/?page=${page}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    gen_items_template(id) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/rfqs/get/items/template/${id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}
export default supplierRfq;