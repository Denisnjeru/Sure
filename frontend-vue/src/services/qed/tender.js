import api from '../../apiV1/api';

const tender = {
    tenders(page, buyerId) {
        buyerId = buyerId || null;

        return new Promise((resolve, reject) => {
            api.get(`/tender/?company_id=${buyerId}&page=${page}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    tender(id, buyerId) {
        buyerId = buyerId || null;
        
        return new Promise((resolve, reject) => {
            api.get(`/tender/${id}/?company_id=${buyerId}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    categories(id, buyerId){
        buyerId = buyerId || null;
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${id}/?company_id=${buyerId}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category(tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${tender_id}/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    sections(tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${tender_id}/sections/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    technical_bidders(tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${tender_id}/technical/bidders/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    minimized_category_details(tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${tender_id}/minimized/details/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    items(tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${tender_id}/items/${category_id}/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    financial_participants(tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${tender_id}/financial/bidders/${category_id}/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    all_participants(tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${tender_id}/all/bidders/${category_id}/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    open_category(content, tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.post(`/tender/categories/${tender_id}/open/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    close_category(tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${tender_id}/close/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    tender_search(query) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/?query=${query}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create(content, buyerId){
        buyerId = buyerId || null;
        
        return new Promise((resolve, reject) => {
            api.post(`/tender/?company_id=${buyerId}`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update(tender_id, content){
        return new Promise((resolve, reject) => {
            api.put(`/tender/${tender_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    defaults() {
        return new Promise((resolve, reject) => {
            api.get(`/tender/defaults/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    section_defaults(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/sections/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    section(category_id, section_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/sections/${category_id}/${section_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_create(content, tender_id){
        return new Promise((resolve, reject) => {
            api.post(`/tender/categories/${tender_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_category(content, tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.put(`/tender/categories/${tender_id}/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_section(category_id, content){
        return new Promise((resolve, reject) => {
            api.post(`/tender/sections/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_section(category_id, section_id, content){
        return new Promise((resolve, reject) => {
            api.put(`/tender/sections/${category_id}/${section_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    questions(section_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/questions/${section_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    question(section_id, question_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/questions/${section_id}/${question_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_question(content, section_id, question_id) {
        return new Promise((resolve, reject) => {
            api.put(`/tender/questions/${section_id}/${question_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_question(content, section_id){
        return new Promise((resolve, reject) => {
            api.post(`/tender/questions/${section_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    initiate_qa(content, category_id){
        return new Promise((resolve, reject) => {
            api.post(`/tender/qa/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    initiate_dd(content, category_id){
        return new Promise((resolve, reject) => {
            api.post(`/tender/dd/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_instructions(content, category_id, question_id){
        return new Promise((resolve, reject) => {
            api.post(`/tender/qa/${category_id}/submit/instructions/${question_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_qa_question_response(content, category_id, qaq_id){
        return new Promise((resolve, reject) => {
            api.post(`/tender/qa/${category_id}/submit/response/${qaq_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    qa_sections(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/qa/${category_id}/sections/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    qa_section_questions(category_id, section_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/qa/${category_id}/section/questions/${section_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },

    qa_section_questions_supplier_response(category_id, section_id, participant_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/qa/${category_id}/section/questions/${section_id}/${participant_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    dd_participants(category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/dd/${category_id}/participants/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    dd_participant(category_id, participant_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/dd/${category_id}/participant/${participant_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    dd_participant_questions(category_id, participant_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/dd/${category_id}/questions/${participant_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    dd_participant_question_response(category_id, participant_id, dd_question_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/dd/${category_id}/question/${participant_id}/${dd_question_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_dd_supplier_question(content, category_id, participant_id){
        return new Promise((resolve, reject) => {
            api.post(`/tender/dd/${category_id}/new/supplier/question/${participant_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_dd_wide_question(content, category_id,){
        return new Promise((resolve, reject) => {
            api.post(`/tender/dd/${category_id}/add/dd/wide/question/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_dd_supplier_question(content, category_id, participant_id, dqr_id){
        return new Promise((resolve, reject) => {
            api.put(`/tender/dd/${category_id}/update/supplier/question/${participant_id}/${dqr_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    qualified_bidders(job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${job_id}/qualified/bidders/${category_id}/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    unqualified_bidders(job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${job_id}/unqualified/bidders/${category_id}/?format=datatables`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_award_letter(content, category_id){
        return new Promise((resolve, reject) => {
            api.post(`/tender/award/letters/${category_id}/create/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_regret_letter(content, category_id){
        return new Promise((resolve, reject) => {
            api.post(`/tender/regret/letters/${category_id}/create/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    report_categories(id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    interim_report(id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/run/interim/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    qa_report(id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/run/qa/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    // sections_questions_instructions(category_id) {
    //     return new Promise((resolve, reject) => {
    //         api.get(`/tender/qa/${category_id}/sections/questions/instructions/`, (data) => {
    //             resolve(data);
    //         }, (error) => {
    //             reject(error);
    //         });
    //     });
    // },
    tender_participation_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/run/participation/status/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    supplier_details_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/run/supplier/details/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    responsive_bidders_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/run/responsive/bidders/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    non_responsive_bidders_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/run/non/responsive/bidders/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    bidder_locations_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/run/bidder/locations/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    criteria_countries() {
         return new Promise((resolve, reject) => {
            api.get(`/tender/criteria/countries/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    criteria_job_template(id) {
         return new Promise((resolve, reject) => {
            api.get(`/tender/download/criteria/template/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    upload_criteria(content, id) {
         return new Promise((resolve, reject) => {
            api.post(`/tender/upload/criteria/template/${id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    upload_current_suppliers(content, id) {
         return new Promise((resolve, reject) => {
            api.post(`/tender/upload/current_suppliers/${id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    send_current_suppliers_letter(content, id) {
         return new Promise((resolve, reject) => {
            api.post(`/tender/send/current_suppliers/letter/${id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    current_suppliers_report(id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/run/current_suppliers/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    publish_job(id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/publish/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_technical_report_pdf(tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${tender_id}/run/report/${category_id}/pdf/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    tender_summary_report(tender_id, category_id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${tender_id}/consolidated/tender/summary/${category_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    invited_suppliers(tender_id, category_id, page) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/categories/${tender_id}/invited/suppliers/${category_id}/?page=${page}`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    email_invite_suppliers(tender_id, category_id, content) {
        return new Promise((resolve, reject) => {
            api.post(`/tender/categories/${tender_id}/invite/from/email/${category_id}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    category_suppliers_report(id){
        return new Promise((resolve, reject) => {
            api.get(`/tender/category/suppliers/report/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_multiple_award_letter(content, job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.post(`/tender/award/letters/${category_id}/create/multiple/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    create_multiple_regret_letter(content, job_id, category_id) {
        return new Promise((resolve, reject) => {
            api.post(`/tender/regret/letters/${category_id}/create/multiple/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    submit_client_document(content) {
        return new Promise((resolve, reject) => {
            api.post(`/tender/client/documents/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    job_client_document(job_id, type){
        return new Promise((resolve, reject) => {
            api.get(`/tender/client/documents/job/${job_id}/${type}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    update_client_document(form_data, job_id, type) {
        return new Promise((resolve, reject) => {
            api.post(`/tender/client/documents/update/${job_id}/${type}/`, form_data, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    tender_letter_details(id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/job/details/letters/${id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    zip_files(question_id) {
        return new Promise((resolve, reject) => {
            api.get(`/tender/archive/zip/files/${question_id}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    participant_documents(categoryId, supplierId){
        return new Promise((resolve, reject) => {
            api.get(`/tender/archive/documents/${categoryId}/supplier/${supplierId}/`, (data) => {
              resolve(data);
          }, (error) => {
              reject(error);
          });
      });
    },
    upload_category_suppliers(id, form_data) {
        return new Promise((resolve, reject) => {
            api.post(`/tender/upload/category/suppliers/${id}/`, form_data, (data) => {
              resolve(data);
          }, (error) => {
              reject(error);
          });
      });
    },
}

export default tender
