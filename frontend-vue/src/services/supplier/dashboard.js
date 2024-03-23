import api from '../../apiV1/api';

const dashboardStats = {
    stats() {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/dashboard/stats/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    companiesWithOpenJobs() {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/dashboard/companies_open_jobs/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    openPrequals(companyID) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/prequal/open/categories/${companyID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    openTenders(companyID) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/tender/open/categories/${companyID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    addCategoryToCart(content) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/category_order/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    removeCategoryFromCart(content) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/category_order/remove/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    cartCategories() {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/category_order/categories/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    ongoingBids(page, dataPerPage, searchQuery) {
        return new Promise((resolve, reject) => {
            let url = `/supplier/category_order/ongoing_bids/?page=${page}&page_size=${dataPerPage}`

            searchQuery = searchQuery || null;
            if( searchQuery !== null) {
                url = `/supplier/category_order/ongoing_bids/?page=${page}&page_size=${dataPerPage}&search=${searchQuery}`
            }

            api.get(url, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    closedBids(page, dataPerPage, searchQuery) {
        return new Promise((resolve, reject) => {
            let url = `/supplier/category_order/closed_bids/?page=${page}&page_size=${dataPerPage}`

            searchQuery = searchQuery || null;
            if( searchQuery !== null) {
                url = `/supplier/category_order/closed_bids/?page=${page}&page_size=${dataPerPage}&search=${searchQuery}`
            }

            api.get(url, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    letters(page, dataPerPage, searchQuery) {
        return new Promise((resolve, reject) => {
            let url = `/supplier/dashboard/stats/letters/?page=${page}&page_size=${dataPerPage}`

            searchQuery = searchQuery || null;
            if( searchQuery !== null) {
                url = `/supplier/dashboard/stats/letters/?page=${page}&page_size=${dataPerPage}&search=${searchQuery}`
            }

            api.get(url, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    stkMpesaPrompt(content) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/category_order/payment/mpesa/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    makeZeroCharge(content) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/category_order/payment/zero_charge/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    cellulantPayment(content) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/category_order/payment/cellulant/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    dpoPayment(content) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/category_order/payment/dpo/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}
export default dashboardStats;