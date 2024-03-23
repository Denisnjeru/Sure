<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Create Contract
            </span>
        </div>
        <form class="form" v-on:submit.prevent="createContract()">
        <div class="page__content columns">
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Supplier Details</p>
                    <p class="column-details__head--desc"></p>
                </div>
                <div class="column-details__content">
                    <div class="field">
                        <label class="label">Category <span class="required">*</span></label>
                        <div class="control">
                            <input readonly class="input readonly" type="text" :value="selectedCategory.name">
                        </div>
                    </div> 
                    <div class="field">
                        <label class="label">Supplier <span class="required">*</span></label>
                        <div class="control">
                            <input readonly class="input readonly" type="text" :value="selectedSupplier.company_name">
                        </div>
                    </div>  
                    <div class="field">
                        <label class="label">Contact Name <span class="required">*</span></label>
                        <div class="control">
                            <input readonly class="input readonly" type="text" :value="selectedSupplier.contact_name">
                        </div>
                    </div> 
                    <div class="field">
                        <label class="label">Contact Phone Number <span class="required">*</span></label>
                        <div class="control">
                            <input readonly class="input readonly" type="text" :value="selectedSupplier.phone_number">
                        </div>
                    </div> 
                    <div class="field">
                        <label class="label">Contact Emails <span class="required">*</span></label>
                        <div class="control">
                            <textarea                                 
                                class="textarea"  cols="30" rows="5"
                                placeholder="Enter comma separated emails"
                                v-model="contact_emails"
                            >
                            </textarea>
                        </div>
                    </div>                
                </div>
            </div>
            <div class="column is-6 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Contract Details</p>
                    <p class="column-details__head--desc"></p>
                </div>
                <div class="column-details__content">
                    <div class="field">
                        <label class="label">Contract Start Date <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="contract.start_date" class="input" type="date">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Contract End Date <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="contract.end_date" class="input" type="date">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Create Contract from <span class="required">*</span></label>
                        <div class="select">
                            <select v-model="contractSource">
                                <option>Select contract source</option>
                                <option value="write">Write New Contract</option>
                                <option value="upload">Upload Contract</option>
                                <option value="sections">Contract Sections</option>
                                <option value="templates">Contract Templates</option>
                            </select>
                        </div>
                    </div>
                    <div class="field" v-if="contractSource === 'upload'">
                        <label class="label">Contract Document</label>
                        <div class="control">
                           <input type="file">
                           <span class="help">Upload word document</span>
                        </div>
                    </div>
                    <div class="field" v-if="contractSource === 'sections'">
                        <label class="label">Contract Sections</label>
                        <div class="control">
                            <span class="page__action--link" @click="popupContractSections()">
                                Select contract sections
                            </span>
                        </div>
                    </div>
                    <div class="field" v-if="contractSource === 'templates'">
                        <label class="label">Contract Template</label>
                        <div class="control">
                            <span class="page__action--link" @click="popupContractTemplates()">
                                Select contract template
                            </span>
                        </div>
                    </div>

                    <p class="selected-sections__section"  v-for="(contractTemplate) in selectedContractTemplate" :key="contractTemplate.id">
                        {{contractTemplate.name}} 
                    </p>

                    <p class="selected-sections__section"  v-for="(contractSection, index) in selectedContractSections" :key="contractSection.id">
                        {{index+1}}. {{contractSection.name}} 
                    </p>
                </div>
            </div>
        </div>  
        <div class="popup" v-if="popContractSections === true">
            <span class="popup__details">
                <div class="page__head">
                    <span class="page__head--title">
                        <font-awesome-icon class="page__head--back" icon="arrow-left" @click="popupContractSections()" />
                        Contract Sections
                    </span>

                    <div class="page__head--links">
                        <span class="page__head--link text-link">
                            Refresh
                        </span>
                        <router-link to="/update-profile">
                            <a class="page__head--link button button-link">
                                Create Contract Section
                            </a>
                        </router-link>
                    </div>
                </div>
                <div class="page__content columns">
                    <div class="column is-9 column-page">
                        <div class="table-search">
                            <p class="table-search__instruction">
                                Select Contract Sections
                            </p>
                            <div class="table-search__search">
                                <font-awesome-icon class="table-search__search--icon" icon="search" />
                                <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                            </div>
                        </div>
                        <v-client-table :columns="sectionColumns" :data="contractSections" :options="options" class="hasNoWrap">
                            <span class="view" slot="section" slot-scope="{row}">
                                <router-link :to="'/buyer/contracts/sections/' + row.id + '/view'">
                                    <font-awesome-icon class="view__icon" icon="eye" />
                                    <span> View Section</span>
                                </router-link>
                            </span>

                            <p slot="created">
                                April 29, 2022
                            </p>

                            <p slot="updated">
                                May 1, 2022
                            </p>
                            <span class="actions" slot="actions" slot-scope="{row}">
                                <span class="actions__select" @click="selectContractSection(row)">
                                    Select
                                </span>
                            </span>
                        </v-client-table>
                    </div>
                    <div class="column is-3 column-page selected-sections">
                        <span class="page__action--link">
                            Selected contract sections
                        </span>
                        <span class="help">Drag to sort</span>
                        <draggable v-model="selectedContractSections" group="sections" @start="drag=true" @end="drag=false">
                            <p class="selected-sections__section"  v-for="(contractSection, index) in selectedContractSections" :key="contractSection.id">
                                {{index+1}}. {{contractSection.name}} 
                                <span class="delete-icon">
                                    <font-awesome-icon class="delete-icon__icon" icon="times" @click="removeSelectedContractSection(contractSection)"/>
                                </span>
                            </p>
                        </draggable>
                    </div>
                </div>
            </span>
        </div>
        <div class="popup" v-if="popContractTemplates === true">
            <span class="popup__details">
                <div class="page__head">
                    <span class="page__head--title">
                        <font-awesome-icon class="page__head--back" icon="arrow-left" @click="popupContractTemplates()" />
                        Contract Templates
                    </span>

                    <div class="page__head--links">
                        <span class="page__head--link text-link">
                            Refresh
                        </span>
                        <router-link to="/update-profile">
                            <a class="page__head--link button button-link">
                                Create Contract Template
                            </a>
                        </router-link>
                    </div>
                </div>
                <div class="page__content columns">
                    <div class="column is-9 column-page">
                        <div class="table-search">
                            <p class="table-search__instruction">
                                Select Contract Templates
                            </p>
                            <div class="table-search__search">
                                <font-awesome-icon class="table-search__search--icon" icon="search" />
                                <input @keyup.enter="search()" class="table-search__search--input" type="text" placeholder="Search here">
                            </div>
                        </div>
                        <v-client-table :columns="templateColumns" :data="contractTemplates" :options="options" class="hasNoWrap">
                            <span class="view" slot="section" slot-scope="{row}">
                                <router-link :to="'/buyer/contracts/templates/' + row.id + '/view'">
                                    <font-awesome-icon class="view__icon" icon="eye" />
                                    <span> View Template</span>
                                </router-link>
                            </span>

                            <p slot="created">
                                April 29, 2022
                            </p>

                            <p slot="updated">
                                May 1, 2022
                            </p>
                            <span class="actions" slot="actions" slot-scope="{row}">
                                <span class="actions__select" @click="selectContractTemplate(row)">
                                    Select
                                </span>
                            </span>
                        </v-client-table>
                    </div>
                    <div class="column is-3 column-page selected-sections">
                        <span class="page__action--link">
                            Selected contract template
                        </span>
                        <p class="selected-sections__section"  v-for="(contractTemplate, index) in selectedContractTemplate" :key="contractTemplate.id">
                            {{index+1}}. {{contractTemplate.name}} 
                            <span class="delete-icon">
                                <font-awesome-icon class="delete-icon__icon" icon="times" @click="removeSelectedContractTemplate(contractTemplate)"/>
                            </span>
                        </p>
                    </div>
                </div>
            </span>
        </div>
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div><div class="column is-3">
                <input type="submit" class="button button-submit" value="Proceed">
            </div>
        </div>
        </form>     
    </div>
</template>

<script>
import contracts from '@/services/company/contracts'
import { mapGetters } from 'vuex'

export default {
    name: 'Dashboard',
    data() {
        return {
            contractSource: "write",
            contact_emails: '',
            popContractSections: false,
            popContractTemplates: false,
            columns: ['#', 'name', 'section', 'created_by', 'created', 'updated', 'actions'],
            sectionColumns: ['name', 'section', 'created_by', 'actions', 'created', 'updated'],
            templateColumns: ['name', 'template', 'created_by', 'actions', 'created', 'updated'],
            options: {
                sortable: ['company', 'job_title'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            contractSections: [],
            selectedContractSections: [],
            contractTemplates: [],
            selectedContractTemplate: [],
            contract: {}
        }
    },
    computed: {
        ...mapGetters('Contracts',['selectedCategory', 'selectedSupplier']),
    },
    mounted() {
        this.contact_emails = this.selectedSupplier.email + ','
        this.getContractSections()
        this.getContractTemplates()
    },
    methods: {
        popupContractSections() {
            this.popContractSections = !this.popContractSections
            this.selectedContractTemplate = []
        },
        popupContractTemplates() {
            this.popContractTemplates = !this.popContractTemplates
            this.selectedContractSections = []
        },
        selectContractSection: function(section) {
            const isSection = this.selectedContractSections.find( ({ id }) => id === section.id )

            if (isSection === undefined) {
                this.selectedContractSections.push(section)
            } else {
                window.toast.fire({
                    icon: 'error',
                    title: 'Section already selected'
                })
            }        
        },
        removeSelectedContractSection: function(section) {
            this.selectedContractSections = this.selectedContractSections.filter(item => item.id !== section.id);
        },
        selectContractTemplate: function(template) {
            const isTemplate = this.selectedContractTemplate.find( ({ id }) => id === template.id )

            if (isTemplate === undefined) {
                this.selectedContractTemplate = []
                this.selectedContractTemplate.push(template)
            } else {
                window.toast.fire({
                    icon: 'error',
                    title: 'Template already selected'
                })
            }        
        },
        removeSelectedContractTemplate: function(template) {
            this.selectedContractTemplate = this.selectedContractTemplate.filter(item => item.id !== template.id);
        },
        async getContractSections() {
            try {
                const response = await contracts.contractSections()
                this.dataCount = response.data.count
                this.contractSections = response.data.results
            } catch (err) {
                console.log(err)
            }
        },
        async getContractTemplates() {
            try {
                const response = await contracts.contractTemplates()
                this.dataCount = response.data.count
                this.contractTemplates = response.data.results
            } catch (err) {
                console.log(err)
            }
        },
        async createContract() {
            try {
                this.contract.supplier = this.selectedSupplier.id
                this.contract.category = this.selectedCategory.id
                this.contract.source = this.contractSource
                this.contract.contact_emails = this.contact_emails

                if (this.contractSource === 'sections') {
                    this.contract.source_list = this.selectedContractSections.map(item => item['id']);
                } else if (this.contractSource === 'templates') {
                    this.contract.source_list = this.selectedContractTemplate.map(item => item['id']);
                } else {
                    this.contract.source_list = []
                }

                const response = await contracts.createSupplierContract(this.contract)
                window.toast.fire({
                    icon: 'success',
                    title: 'Contract created successfully'
                })

                this.$router.push('/buyer/contracts/supplier/contract/' + response.data.id + '/update')
            } catch (err) {
                console.log(err)
            }
        },
        async search() {
            console.log('search');
        },

    }
}
</script>

<style lang="scss" scoped>
@include page;
@include form;

.page__content {
    padding: $line-height $line-height;
}

.dashboard {
    position: relative;
}

.readonly {
    background-color: $color-gray-light;
}

.popup {
    position: absolute; 
    top: 0vh;
    width: 100%;
    height: 100%; 
    z-index: 90;
    background-color: rgba(0, 0, 0, 0.2); 
    @include grid_row;
    align-items: flex-start;
    transition: opacity .3s;
    
    &__details {
        // position: sticky;
        // top: 20vh;
        min-height: 70vh;
        background-color: $color-white-main;
        $width: 97%;
        width: $width;
        margin: 5vh calc((100% - #{$width})/2);
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: $line-height/2;
        padding: $line-height $line-height/3;

        .page__content {
            padding-top: $line-height*2;
        }

        .column-page {
            box-shadow: none;
            padding: 0 $line-height;
            border-radius: 0;
            
            &:first-child {
                border-right: 1px solid $color-gray-medium;
            }
        }
    }
}

.selected-sections {
    text-align: left;
    align-items: flex-start !important;
    justify-content: flex-start !important;

    &__section {
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: $line-height/4;
        padding: $line-height/3;
        margin: $line-height/3 0;
        width: 100%;
    }

    .delete-icon {
        color: $color-red-main;
        padding: 0 $line-height;

        &__icon {
            color: $color-red-main;
            cursor: pointer;
        }
    }
}
</style>
