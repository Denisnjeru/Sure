import api from '../../apiV1/api';

const rfq = {
    rfqs(page, buyerId) {
        buyerId = buyerId || null;

        return new Promise((resolve, reject) => {
            api.get(`/rfq/?company_id=${buyerId}&page=${page}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfq(id, buyerId) {
        buyerId = buyerId || null;

        return new Promise((resolve, reject) => {
            api.get(`/rfq/${id}/?company_id=${buyerId}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    defaults() {
        return new Promise((resolve, reject) => {
            api.get(`/rfq/defaults/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    categories(id){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/categories/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create(content, buyerId){
        buyerId = buyerId || null;

        return new Promise((resolve, reject) => {
            api.post(`/rfq/?company_id=${buyerId}`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqCategoryCreate(content, job_id){
        return new Promise((resolve, reject) => {
            api.post(`/rfq/categories/${job_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqCategoryDetails(rfq_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/categories/${rfq_id}/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqInvitedBidders(rfq_id, category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/rfq/categories/${rfq_id}/invited/suppliers/${category_id}/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqInviteSuppliers(content,rfq_id, category_id) {
        return new Promise((resolve, reject) => {
            api.post(`/rfq/categories/${rfq_id}/invite_suppliers/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    openRFQCategory(content, rfq_id, category_id){
        return new Promise((resolve, reject) => {
            api.post(`/rfq/categories/${rfq_id}/open/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    closeRFQCategory(rfq_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/categories/${rfq_id}/close/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqRelatedPrequals(rfq_id,category_id){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/categories/${rfq_id}/related/prequals/${category_id}/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqSubmitItemResponse(content,item_id,supplier_id){
        return new Promise((resolve, reject) => {
            api.post(`/rfq/items/responses/${item_id}/${supplier_id}/`,content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqRetrieveSupplierItemResponse(item_id,supplier_id){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/items/responses/${item_id}/${supplier_id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqSubmitTotal(content,category_id,supplier_id){
        return new Promise((resolve, reject) => {
            api.post(`/rfq/category/response_totals/${category_id}/${supplier_id}/`,content,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqGetParticipants(rfq_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/categories/${rfq_id}/participants/${category_id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqDownloadSupplierResponse(rfq_id,category_id,supplier_id){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/categories/${rfq_id}/generate/supplier/rfq/report/pdf/${category_id}/${supplier_id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });

    },
    rfqDownloadParticipationSummary(rfq_id,category_id){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/categories/${rfq_id}/generate/category/rfq/report/pdf/${category_id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqDownloadFinancialReport(rfq_id,category_id){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/categories/${rfq_id}/generate/financial/report/${category_id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqDownloadJobSummaryReport(rfq_id){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/generate/job/summary/report/${rfq_id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqDownloadCurrentSupplierTemplate(rfq_id,category_id){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/categories/${rfq_id}/download/current_prices/template/${category_id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    rfqUploadCurrentSupplierTemplate(rfq_id,category_id){
        return new Promise((resolve, reject) => {
            api.post(`/rfq/categories/${rfq_id}/upload/current_prices/template/${category_id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    participant_documents(categoryId, supplierId){
        return new Promise((resolve, reject) => {
            api.get(`/rfq/archive/documents/${categoryId}/supplier/${supplierId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    upload_category_suppliers(id, form_data) {
        return new Promise((resolve, reject) => {
            api.post(`/rfq/upload/category/suppliers/${id}/`, form_data, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default rfq;
