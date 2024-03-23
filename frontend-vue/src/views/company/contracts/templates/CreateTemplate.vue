<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Create Contract Template
            </span>
            <div class="page__head--links">
                <a class="page__head--link button button-link" @click="popupContractSections()">
                    Select Contract Sections
                </a>
            </div>
        </div>
        <form class="form" v-on:submit.prevent="createTemplate()">
        <div class="page__content columns">
            <div class="column is-12 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Contract Template Details</p>
                    <p class="column-details__head--desc"></p>
                </div>
                <div class="column-details__content">                    
                    <div class="field">
                        <label class="label">Template Name <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="contractTemplate.name" class="input" type="text">
                        </div>
                    </div> 
                    <div class="field">
                        <label class="label">Template Content <span class="required">*</span></label>
                        <div class="control">
                            <!-- <TinyMce /> -->
                            <editor 
                                api-key='ilebf08k7e8o2y9rvuxb1tngrsz9ag0emag1yeqbb0oit0uu'
                                :init="config"
                                v-model="contractTemplate.content"
                            />
                            <div>
                                <button v-on:click='saveAsDocx' >Save</button>
                            </div>
                        </div>
                    </div>   
                    <!-- <HtmlDiff />  -->
                </div>
            </div>
        </div>  
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div>
            <div class="column is-3">
                <input type="submit" class="button button-submit" value="Create template">
            </div>
        </div>
        </form>  
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
                        <router-link to="/buyer/contracts/sections">
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
                        <v-client-table :columns="sectionColumns" :data="contractSections" :options="options" class="hasRowNo hasNoWrap">
                            <p class="row-no" v-if="contractSections.length !== 0" slot="#" slot-scope="props">
                                {{props.index}}
                            </p>
                            <span class="view" slot="section" slot-scope="{row}">
                                <router-link :to="'/buyer/contracts/sections/' + row.id + '/view'" target="_blank">
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
                        <div class="columns additions">
                            <div class="column is-12">
                                <span @click="getContent()" class="button button-submit">Submit</span>
                            </div>
                        </div>
                    </div>
                </div>
            </span>
        </div>   
    </div>
</template>

<script>
import contracts from '@/services/company/contracts'
// import TinyMce from '@/components/TinyMce'
// import HtmlDiff from '@/components/HtmlDiff'
import { customHr } from '@/plugins/myHr/plugin'


export default {
    name: 'contractTemplatesCreate',
    data() {
        return {
            contractTemplate: {},
            popContractSections: false,
            sectionColumns: ['name', 'section', 'created_by', 'actions', 'created', 'updated'],
            options: {
                sortable: ['name', 'created_by'],
                perPageValues: [20], 
                filterable: false
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
            contractSections: [],
            selectedContractSections: [],
            config: {
                height: 400,
                plugins: [
                    'hrcustom hr pagebreak emoticons advlist autolink lists link image charmap print preview anchor',
                    'searchreplace visualblocks code fullscreen directionality',
                    'insertdatetime media table paste code help wordcount autosave save',
                ],
                toolbar:
                    'restoredraft pagebreak undo redo save | hrcustom hr | blocks fontfamily fontsize | formatselect | bold italic forecolor backcolor strikethrough | \
                    alignleft aligncenter alignright alignjustify | \
                    bullist numlist outdent indent | removeformat | help | ltr rtl',
                setup: function () {
                    window.tinymce.PluginManager.add('hrcustom', customHr)
                }
            }
        }
    },
    mounted() {
        this.getContractSections()
    },
    components: {
        // TinyMce,
        // HtmlDiff
    },
    methods: {
        popupContractSections() {
            this.popContractSections = !this.popContractSections
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
        async search() {
            console.log('search');
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
        async getContent(){
            try {
                let payload = {
                    "source_list": this.selectedContractSections.map(item => item['id'])
                }

                console.log(payload)
                const response = await contracts.combineContractSections(payload)
                this.contractTemplate.content = response.data.content
                this.popupContractSections()
            } catch (err) {
                console.log(err.response)      
            } 
        },
        async createTemplate(){
            try {
                const response = await contracts.createContractTemplate(this.contractTemplate)
                window.toast.fire({
                    icon: 'success',
                    title: response.data.name + ' created successfully'
                })
                this.$router.push('/buyer/contracts/templates')
            } catch (err) {
                console.log(err)      
            } 
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
}
</style>
