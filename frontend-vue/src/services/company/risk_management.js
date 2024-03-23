import api from '../../apiV1/api';

const risk_management = {
    risks() {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createRisks(content) {
        return new Promise((resolve, reject) => {
            api.post(`/risk_management/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    approveRisk(riskID) {
        return new Promise((resolve, reject) => {
            api.post(`/risk_management/approve/${riskID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    getRisk(riskID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/${riskID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateRisk(riskID) {
        return new Promise((resolve, reject) => {
            api.patch(`/risk_management/${riskID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRisk(riskID) {
        return new Promise((resolve, reject) => {
            api.delete(`/risk_management/${riskID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    riskCategories(riskID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/categories/${riskID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createRiskCategory(content, riskID) {
        return new Promise((resolve, reject) => {
            api.post(`/risk_management/categories/${riskID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    getRiskCategory(riskID,categoryID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/categories/${riskID}/${categoryID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateRiskCategory(riskID,categoryID) {
        return new Promise((resolve, reject) => {
            api.patch(`/risk_management/categories/${riskID}/${categoryID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRiskCategory(riskID,categoryID) {
        return new Promise((resolve, reject) => {
            api.delete(`/risk_management/categories/${riskID}/${categoryID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRiskSupportingDocument(riskID,documentID) {
        return new Promise((resolve, reject) => {
            api.delete(`/risk_management/supportingdocuments/${riskID}/${documentID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createRiskCategorySection(content, categoryID) {
        return new Promise((resolve, reject) => {
            api.post(`/risk_management/sections/${categoryID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    getRiskCategorySection(categoryID,sectionID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/sections/${categoryID}/${sectionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateRiskCategorySection(categoryID,sectionID) {
        return new Promise((resolve, reject) => {
            api.patch(`/risk_management/sections/${categoryID}/${sectionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRiskCategorySection(categoryID,sectionID) {
        return new Promise((resolve, reject) => {
            api.delete(`/risk_management/sections/${categoryID}/${sectionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRiskCategorySupportingDocument(categoryID,documentID) {
        return new Promise((resolve, reject) => {
            api.delete(`/risk_management/categorysupportingdocuments/${categoryID}/${documentID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createRiskQuestion(content, sectionID) {
        return new Promise((resolve, reject) => {
            api.post(`/risk_management/questions/${sectionID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    getRiskQuestion(sectionID, questionID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/questions/${sectionID}/${questionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateRiskQuestion(content, sectionID, questionID) {
        return new Promise((resolve, reject) => {
            api.put(`/risk_management/questions/${sectionID}/${questionID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRiskQuestion(sectionID,questionID) {
        return new Promise((resolve, reject) => {
            api.delete(`/risk_management/questions/${sectionID}/${questionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createRiskAssessment(content, categoryID) {
        return new Promise((resolve, reject) => {
            api.post(`/risk_management/qa/${categoryID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    getRiskAssessment(categoryID, raID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/qa/${categoryID}/${raID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    getRiskAssessments(categoryID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/qa/${categoryID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateRiskAssessment(content, categoryID, raID) {
        return new Promise((resolve, reject) => {
            api.put(`/risk_management/qa/${categoryID}/${raID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRiskAssessment(categoryID, raID) {
        return new Promise((resolve, reject) => {
            api.delete(`/risk_management/qa/${categoryID}/${raID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    getRiskAssessmentRASections(categoryID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/qa/${categoryID}/get_qa_sections/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    severityoptions(raID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/qa/questions/${raID}/severity_options/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    likelihoodoptions(raID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/qa/questions/${raID}/likelihood_options/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createRiskAssessmentQuestion(content, raID) {
        return new Promise((resolve, reject) => {
            api.post(`/risk_management/qa/questions/${raID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createRiskAssessmentQuestions(content, raID) {
        return new Promise((resolve, reject) => {
            api.post(`/risk_management/qa/questions/${raID}/create_qa_questions/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    getRiskAssessmentQuestion(raID, raquestionID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/qa/questions/${raID}/${raquestionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateRiskAssessmentQuestion(content, raID, raquestionID) {
        return new Promise((resolve, reject) => {
            api.put(`/risk_management/qa/questions/${raID}/${raquestionID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRiskAssessmentQuestion(raID, raquestionID) {
        return new Promise((resolve, reject) => {
            api.delete(`/risk_management/qa/questions/${raID}/${raquestionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createRiskAssessmentQuestionResponses(content, raquestionID) {
        return new Promise((resolve, reject) => {
            api.post(`/risk_management/qa/questions/responses/${raquestionID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    getRiskAssessmentQuestionResponses(raquestionID, raquestionresponseID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/qa/questions/responses/${raquestionID}/${raquestionresponseID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateRiskAssessmentQuestionResponses(content, raquestionID, raquestionresponseID) {
        return new Promise((resolve, reject) => {
            api.put(`/risk_management/qa/questions/responses/${raquestionID}/${raquestionresponseID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRiskAssessmentQuestionResponses(raquestionID, raquestionresponseID) {
        return new Promise((resolve, reject) => {
            api.delete(`/risk_management/qa/questions/responses/${raquestionID}/${raquestionresponseID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },

    // Supplier Risk management URL's
    createRiskManagementSupplierResponse(content, questionID, supplierID) {
        return new Promise((resolve, reject) => {
            api.post(`/risk_management/supplier/response/${questionID}/${supplierID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    getRiskManagementSupplierResponse(questionID, supplierID, questionsupplierresponseID) {
        return new Promise((resolve, reject) => {
            api.get(`/risk_management/supplier/response/${questionID}/${supplierID}/${questionsupplierresponseID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateRiskManagementSupplierResponse(content, questionID, supplierID, questionsupplierresponseID) {
        return new Promise((resolve, reject) => {
            api.put(`/risk_management/supplier/response/${questionID}/${supplierID}/${questionsupplierresponseID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteRiskManagementSupplierResponse(questionID, supplierID, questionsupplierresponseID) {
        return new Promise((resolve, reject) => {
            api.delete(`/risk_management/supplier/response/${questionID}/${supplierID}/${questionsupplierresponseID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default risk_management
