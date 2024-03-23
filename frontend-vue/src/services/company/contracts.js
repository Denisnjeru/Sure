import api from '../../apiV1/api';

const contracts = {
    jobs(companyID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/jobs/${companyID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    suppliers(categoryID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/category/${categoryID}/suppliers/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    buyers() {
        return new Promise((resolve, reject) => {
            api.get(`/buyer/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    contract(contractID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/contracts/${contractID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createContract(content) {
        return new Promise((resolve, reject) => {
            api.post(`/contract/contracts/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateContract(contractID, content) {
        return new Promise((resolve, reject) => {
            api.put(`/contract/contracts/${contractID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    contractEdit(contractID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/contracts/${contractID}/live_edit/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    contractUpdateRequest(contractID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/contracts/${contractID}/request_update/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    contractRevision(contractID, revisionID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/contracts/${contractID}/revision/${revisionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    qedContracts(companyID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/contracts/company/${companyID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    supplierContracts(categoryID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/supplier_contracts/category/${categoryID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    supplierContract(contractID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/supplier_contracts/${contractID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    supplierContractEdit(contractID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/supplier_contracts/${contractID}/live_edit/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    supplierContractEditSave(contractID, content) {
        return new Promise((resolve, reject) => {
            api.post(`/contract/supplier_contracts/${contractID}/live_edit_save/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    supplierContractLastRevision() {
        return new Promise((resolve, reject) => {
            api.get(`/contract/revisions/last_revision/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createSupplierContract(content) {
        return new Promise((resolve, reject) => {
            api.post(`/contract/supplier_contracts/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    contractSections() {
        return new Promise((resolve, reject) => {
            api.get(`/contract/sections/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    contractSection(sectionID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/sections/${sectionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createContractSections(content) {
        return new Promise((resolve, reject) => {
            api.post(`/contract/sections/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateContractSection(sectionID, content) {
        return new Promise((resolve, reject) => {
            api.put(`/contract/sections/${sectionID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteContractSection(sectionID) {
        return new Promise((resolve, reject) => {
            api.delete(`/contract/sections/${sectionID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    combineContractSections(content) {
        return new Promise((resolve, reject) => {
            api.post(`/contract/sections/combine_sections/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    contractTemplates() {
        return new Promise((resolve, reject) => {
            api.get(`/contract/templates/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    contractTemplate(templateID) {
        return new Promise((resolve, reject) => {
            api.get(`/contract/templates/${templateID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    createContractTemplate(content) {
        return new Promise((resolve, reject) => {
            api.post(`/contract/templates/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    updateContractTemplate(templateID, content) {
        return new Promise((resolve, reject) => {
            api.put(`/contract/templates/${templateID}/`, content, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
    deleteContractTemplate(templateID) {
        return new Promise((resolve, reject) => {
            api.delete(`/contract/templates/${templateID}/`, (data) => {
                resolve(data);
            }, (error) => {
                reject(error);
            });
        });
    },
}

export default contracts