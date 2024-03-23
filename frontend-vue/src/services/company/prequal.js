import api from '../../apiV1/api';

const prequal = {
    prequals(page) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/?page=${page}&page_size=10`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    prequal(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    job_search(page, key) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/search/${key}/?page=${page}&page_size=10`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    prequal_letter_details(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/job/details/letters/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    categories(id, page, dataPerPage){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${id}/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_search(id, key, page, dataPerPage){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${id}/search/${key}/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_participants(id, job_id, page){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${job_id}/participants/${id}/?page=${page}&page_size=10`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    search_category_participants(id, job_id, page, key){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${job_id}/participants/search/${id}/?query=${key}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    participant_documents(categoryId, supplierId){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/archive/documents/${categoryId}/supplier/${supplierId}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category(prequal_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${prequal_id}/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    open_category(content, prequal_id, category_id){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/categories/${prequal_id}/open/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    close_category(prequal_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${prequal_id}/close/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    prequal_search(query) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/?query=${query}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create(content){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update(prequal_id, content){
        return new Promise((resolve, reject) => {
            api.put(`/prequal/${prequal_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    defaults() {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/defaults/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    section_defaults(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/sections/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    sections(category_id, page, section_data_per_page) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/sections/${category_id}/?page=${page}&page_size=${section_data_per_page}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    section_search(category_id, query, section_data_per_page) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/sections/${category_id}/search/?page_size=${section_data_per_page}&query=${query}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    section(category_id, section_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/sections/${category_id}/${section_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_create(content, prequal_id){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/categories/${prequal_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_category(content, prequal_id, category_id){
        return new Promise((resolve, reject) => {
            api.put(`/prequal/categories/${prequal_id}/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_section(category_id, content){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/sections/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_section(category_id, section_id, content){
        return new Promise((resolve, reject) => {
            api.put(`/prequal/sections/${category_id}/${section_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    questions(section_id, page, dataPerPage) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/questions/${section_id}/?page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    search_questions(section_id, key, page, dataPerPage) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/questions/${section_id}/search/?query=${key}&page=${page}&page_size=${dataPerPage}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    // questions_filter(section_id, page) {
    //     return new Promise((resolve, reject) => {
    //         api.get(`/prequal/questions/${section_id}/?page=${page}`, (data) => {
    //             resolve(data);
    //         }, (error) => {
    //             reject(error);
    //         });
    //     });
    // },
    question(section_id, question_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/questions/${section_id}/${question_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_question(content, section_id, question_id) {
        return new Promise((resolve, reject) => {
            api.put(`/prequal/questions/${section_id}/${question_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_question(content, section_id){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/questions/${section_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    initiate_qa(content, category_id){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/qa/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    initiate_dd(content, category_id){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/dd/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_instructions(content, category_id, question_id){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/qa/${category_id}/submit/instructions/${question_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_qa_question_response(content, category_id, qaq_id){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/qa/${category_id}/submit/response/${qaq_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    qa_sections(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/qa/${category_id}/sections/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    qa_section_questions(category_id, section_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/qa/${category_id}/section/questions/${section_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },

    qa_section_questions_supplier_response(category_id, section_id, participant_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/qa/${category_id}/section/questions/${section_id}/${participant_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    dd_participants(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/dd/${category_id}/participants/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    dd_participant(category_id, participant_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/dd/${category_id}/participant/${participant_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    dd_participant_questions(category_id, participant_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/dd/${category_id}/questions/${participant_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    dd_participant_question_response(category_id, participant_id, dd_question_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/dd/${category_id}/question/${participant_id}/${dd_question_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_dd_supplier_question(content, category_id, participant_id){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/dd/${category_id}/new/supplier/question/${participant_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_dd_wide_question(content, category_id,){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/dd/${category_id}/add/dd/wide/question/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_dd_supplier_question(content, category_id, participant_id, dqr_id){
        return new Promise((resolve, reject) => {
            api.put(`/prequal/dd/${category_id}/update/supplier/question/${participant_id}/${dqr_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    qualified_bidders(job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${job_id}/qualified/bidders/${category_id}/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    unqualified_bidders(job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${job_id}/unqualified/bidders/${category_id}/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_award_letter(content, category_id){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/award/letters/${category_id}/create/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_regret_letter(content, category_id){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/regret/letters/${category_id}/create/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },

    report_categories(id){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    interim_report(id){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/run/interim/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    qa_report(id){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/run/qa/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    // sections_questions_instructions(category_id) {
    //     return new Promise((resolve, reject) => {
    //         api.get(`/prequal/qa/${category_id}/sections/questions/instructions/`, (data) => {
    //             resolve(data);
    //         }, (error) => {
    //             reject(error);
    //         });
    //     });
    // },
    participation_status_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/run/participation/status/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    directors_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/run/directors/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    non_responsive_bidders_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/run/non-responsive/bidders/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    responsive_bidders_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/run/responsive/bidders/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    job_bidder_payments_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/run/bidder/payments/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    prequalified_suppliers_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/run/prequalified/suppliers/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    current_suppliers_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/run/current_suppliers/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    bidder_locations_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/run/bidder/locations/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    dd_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/run/dd/ranking/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_suppliers_report(id){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/category/suppliers/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    ratios_report(category_id){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/category/reports/${category_id}/financial/ratios/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_email_notifications(content, job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.post(`/prequal/categories/${job_id}/send/email/notifications/${category_id}/`,
                content,
                (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_sms_notifications(content, job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.post(`/prequal/categories/${job_id}/send/sms/notifications/${category_id}/`,
                content,
                (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    criteria_countries() {
         return new Promise((resolve, reject) => {
            api.get(`/prequal/criteria/countries/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    criteria_job_template(id) {
         return new Promise((resolve, reject) => {
            api.get(`/prequal/download/criteria/template/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    upload_criteria(content, id) {
         return new Promise((resolve, reject) => {
            api.post(`/prequal/upload/criteria/template/${id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    upload_current_suppliers(content, id) {
         return new Promise((resolve, reject) => {
            api.post(`/prequal/upload/current_suppliers/${id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    send_current_suppliers_letter(content, id) {
         return new Promise((resolve, reject) => {
            api.post(`/prequal/send/current_suppliers/letter/${id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    publish_job(id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/publish/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_technical_report_pdf(prequal_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${prequal_id}/run/report/${category_id}/pdf/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    invited_suppliers(prequal_id, category_id, page) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${prequal_id}/invited/suppliers/${category_id}/?page=${page}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    email_invite_suppliers(prequal_id, category_id, content) {
        return new Promise((resolve, reject) => {
            api.post(`/prequal/categories/${prequal_id}/invite/from/email/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    refresh_scores(prequal_id, category_id) {
         return new Promise((resolve, reject) => {
            api.get(`/prequal/categories/${prequal_id}/refresh/scores/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_multiple_award_letter(content, job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.post(`/prequal/award/letters/${category_id}/create/multiple/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_multiple_regret_letter(content, job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.post(`/prequal/regret/letters/${category_id}/create/multiple/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_client_document(content) {
        return new Promise((resolve, reject) => {
            api.post(`/prequal/client/documents/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    job_client_document(job_id, type){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/client/documents/job/${job_id}/${type}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_client_document(form_data, job_id, type) {
        return new Promise((resolve, reject) => {
            api.post(`/prequal/client/documents/update/${job_id}/${type}/`, form_data, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    zip_files(question_id) {
        return new Promise((resolve, reject) => {
            api.get(`/prequal/archive/zip/files/${question_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_multiple_custom_letter(content, job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.post(`/prequal/custom/letters/${category_id}/create/multiple/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_multiple_dd_letter(content, job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.post(`/prequal/dd/letters/${category_id}/create/multiple/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    upload_category_suppliers(id, form_data) {
        return new Promise((resolve, reject) => {
            api.post(`/prequal/upload/category/suppliers/${id}/`, form_data, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    ratios_qa(category_id, participant_id, form_data){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/qa/${category_id}/ratios/qa/${participant_id}/`, form_data, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    send_broadcast_notification(prequal_id, content){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/notifications/${prequal_id}/broadcast/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    send_job_email_notification(prequal_id, content){
        return new Promise((resolve, reject) => {
            api.post(`/prequal/notifications/${prequal_id}/email/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    send_invite_email(prequal_id){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/notifications/${prequal_id}/email/invite/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    send_invite_sms(prequal_id){
        return new Promise((resolve, reject) => {
            api.get(`/prequal/notifications/${prequal_id}/sms/invite/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    }
}

export default prequal;
