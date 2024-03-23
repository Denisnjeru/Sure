import api from '../../apiV1/api';

const supplier_prequal = {
    ordered_categories(page, dataPerPage) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/prequal/ordered/categories/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_instructions(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/prequal/ordered/categories/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    bid_sections(category_id){
        return new Promise((resolve, reject) => {
            api.get(`/supplier/prequal/ordered/categories/sections/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    bid_questions(section_id){
        return new Promise((resolve, reject) => {
            api.get(`/supplier/prequal/ordered/categories/questions/${section_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    bid(question_id, content){
        return new Promise((resolve, reject) => {
            api.post(`/supplier/prequal/ordered/categories/bid/${question_id}/`,content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    finish_bid(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/prequal/ordered/categories/finish/bid/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    participation_progress(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/prequal/ordered/categories/participation/progress/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_ratios(id, form) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/prequal/ordered/categories/submit/ratios/${id}/`, form, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    preview_sections(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/prequal/ordered/categories/preview/sections/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    delete_response(question_id) {
        return new Promise((resolve, reject) => {
            api.get(`/supplier/prequal/ordered/categories/delete/response/${question_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_profile_response(data, id) {
        return new Promise((resolve, reject) => {
            api.post(`/supplier/prequal/ordered/categories/profile/selection/bid/${id}/`,data, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    }
}

export default supplier_prequal;