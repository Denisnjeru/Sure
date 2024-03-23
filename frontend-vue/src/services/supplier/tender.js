import api from '../../apiV1/api';

const supplier_tender = {
    ordered_categories(page, dataPerPage) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/tender/ordered/categories/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_instructions(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/tender/ordered/categories/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    bid_sections(category_id){
        return new Promise((resolve, reject) => {
            api.get(`/supplier/tender/ordered/categories/sections/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    bid_questions(section_id){
        return new Promise((resolve, reject) => {
            api.get(`/supplier/tender/ordered/categories/questions/${section_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    bid(question_id, content){
        return new Promise((resolve, reject) => {
            api.post(`/supplier/tender/ordered/categories/bid/${question_id}/`,content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    items(category_id){
        return new Promise((resolve, reject) => {
            api.get(`/supplier/tender/ordered/categories/items/${category_id}/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_item_response(category_id, content){
        return new Promise((resolve, reject) => {
            api.post(
                `/supplier/tender/ordered/categories/submit/item/response/${category_id}/`,
                content,
                (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    finish_technical_bid(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/tender/ordered/categories/finish/technical/bid/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    participation_progress(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/tender/ordered/categories/t/participation/progress/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_ratios(id, form) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/tender/ordered/categories/submit/ratios/${id}/`, form, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    preview_sections(category_id) {
         return new Promise((resolve, reject) => {
            api.get(`/supplier/tender/ordered/categories/preview/sections/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    delete_response(question_id) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/tender/ordered/categories/delete/response/${question_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_profile_response(data, id) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/tender/ordered/categories/profile/selection/bid/${id}/`,data, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    gen_items_template(id) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/tender/ordered/categories/get/items/template/${id}/`,(data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_advanced_financial_bid(data, id){
        return new Promise((resolve, reject) => {
            api.post(`/supplier/tender/ordered/categories/submit/advanced/bid/${id}/`,data, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    }
}

export default supplier_tender;