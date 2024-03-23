<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                <span @click="$router.go(-1)" class="page__head--back"><font-awesome-icon  icon="chevron-left"/> &nbsp;Back</span>
                Update Contract
                <span v-if="contract.live_edit === true"> - Live Editing: 
                    <span class="green" v-if="userData.username === contract.live_editor">Me</span>
                    <span class="green" v-else> {{contract.live_editor}}</span>
                </span>
            </span>
            <div class="page__head--links"> 
                <a class="page__head--link text-link" @click="contractUpdateRequest()" v-if="contract.live_edit === true && userData.username !== contract.live_editor">
                    Request contract update
                </a>               
                <a class="page__head--link button button-link" @click="popupHistory()">
                    History
                </a>
            </div>
        </div>
        
        <form class="form" v-on:submit.prevent="updateContract()" enctype="multipart/form-data" novalidate>
        <div class="page__content columns is-multiline">
            <div class="column is-12 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title hidecontent">
                        <span>Contract Details</span>
                        <span>
                            <font-awesome-icon class="hidecontent__icon" icon="chevron-down" @click="hideColumnContent()"/>
                        </span>
                    </p>
                    <p class="column-details__head--desc">
                        
                    </p>
                </div>
                <div class="column-details__content" v-if="hideContent===false && contract.target">
                    <p class="page__content-detail">
                        <span class="page__content-detail--title">Job: </span>
                        <span class="page__content-detail--content">{{contract.target.title}}</span>
                    </p>
                    <p class="page__content-detail">
                        <span class="page__content-detail--title">Job Code: </span>
                        <span class="page__content-detail--content">{{contract.target.unique_reference}}</span>
                    </p>
                    <p class="page__content-detail">
                        <span class="page__content-detail--title">Job Type: </span>
                        <span class="page__content-detail--content capitalize">{{contract.target.sourcing_activity}}</span>
                    </p>
                    <p class="page__content-detail">
                        <span class="page__content-detail--title">Status: </span>
                        <span class="page__content-detail--content" :class="contract.status">{{contract.status}}</span>
                    </p>
                    <p class="page__content-detail">
                        <span class="page__content-detail--title">Approval Status: </span>
                        <span class="page__content-detail--content" :class="contract.approval_status">{{contract.approval_status}}</span>
                    </p>
                    <br>
                    <div class="field" hidden>
                        <label class="label">Contact Emails <span class="required">*</span></label>
                        <div class="control">
                            <textarea                                 
                                class="textarea"  cols="30" rows="5"
                                placeholder="Enter comma separated emails"
                                v-model="contract.contact_emails"
                            >
                            </textarea>
                        </div>
                    </div> 
                    <div class="field">
                        <label class="label">Contract Start Date <span class="required">*</span></label>
                        <div class="control">
                            <input class="input" type="date" v-model="contract.start_date">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Contract End Date <span class="required">*</span></label>
                        <div class="control">
                            <input class="input" type="date" v-model="contract.end_date">
                        </div>
                    </div>               
                </div>
            </div>
            <div class="column is-12 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Contract</p>
                    <p class="column-details__head--desc"></p>
                </div>
                <div class="column-details__content">
                    <a @click="confirmEditContract" v-if="contract.live_edit === false">
                        <font-awesome-icon icon="pen" />&nbsp;
                        Edit contract
                    </a>
                    <div class="field" v-if="contract.document === null">
                        <label class="label" v-if="contract.live_edit === true">Live Editing: 
                            <span class="green" v-if="userData.username === contract.live_editor">Me</span>
                            <span class="green" v-else> {{contract.live_editor}}</span></label>
                        <div class="control" v-if="contract.live_edit === true && userData.username === contract.live_editor">
                            <editor 
                                api-key='ilebf08k7e8o2y9rvuxb1tngrsz9ag0emag1yeqbb0oit0uu'
                                v-model="contract.content"
                                :init="config"                            
                            />
                        </div>
                        <div class="control" v-else>
                            <div v-html="contract.content"></div>
                        </div>
                    </div> 
                    <div class="field" v-else>
                        <br>
                        <span v-if="contract.live_edit === true && userData.username === contract.live_editor">
                        <button class="button blue-button" @click="confirmEditContract">
                            <font-awesome-icon icon="file-download" />&nbsp;
                            Download contract
                        </button>
                        <br>
                        <br>
                        <label class="label">Upload updated contract document</label>
                        <div class="file has-name">
                            <label class="file-label">
                                <input class="file-input" type="file" name="contractDocument" @change="handleContractDocument">
                                <span class="file-cta">
                                    <span class="file-icon">
                                        <i class="fas fa-upload"></i>
                                    </span>
                                    <span class="file-label">
                                        Choose contract word document...
                                    </span>
                                </span>
                                <span class="file-name" v-if="contractDocument !== null">
                                    {{contractDocument.name}}
                                </span>
                                <span class="file-name" v-else>
                                    No file selected
                                </span>
                            </label>
                        </div>
                        </span>
                    </div>
                    
                </div>
            </div>
        </div>  

        <div class="popup" v-if="popHistory === true">
            <span class="popup__details">
                <div class="page__head">
                    <span class="page__head--title">
                        <font-awesome-icon class="page__head--back" icon="arrow-left" @click="popupHistory()" />
                        Contract Revision History
                    </span>

                    <div class="page__head--links">
                        <div class="field">
                            <div class="select">
                                <select class="revisions-select">
                                    {{contract.revisions}}
                                    <option class="revisions-select__option" @click="selectRevision(revision)" v-for="revision in contract.revisions" :key="revision.id">{{revision.editor}} - {{revision.updated}}</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="page__content columns">
                    <div class="column is-12">
                        <span v-if="selectedRevision !== null">
                            <documentView :documentUrl="'https://2f13-105-162-7-98.eu.ngrok.io' + selectedRevision.changes" />
                        </span>
                        <span v-if="contract.revisions.length === 0">
                            No changes made to the contract
                        </span>
                    </div>                        
                </div>
            </span>
        </div>
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div>
            <div class="column is-3">
                <input v-if="contract.live_edit === true && userData.username === contract.live_editor" type="submit" class="button button-submit" value="Update Contract">
            </div>
        </div>
        </form>     
    </div>
</template>

<script>
import axios from 'axios'
import contracts from '@/services/company/contracts'
import documentView from '@/components/contracts/DocumentView.vue'
import { mapGetters } from 'vuex'

export default {
    name: 'BuyerContractsQedUpdate',
    data() {
        return {
            contractSource: "write",
            contact_emails: '',
            hideContent: false,
            contract: {},
            last_revision: {},
            popHistory: false,
            contractDocument: null,
            config: {
                height: 400,
                plugins: [
                    'hr pagebreak emoticons advlist autolink lists link image charmap print preview anchor',
                    'searchreplace visualblocks code fullscreen directionality',
                    'insertdatetime media table paste code help wordcount autosave save',
                ],
                toolbar:
                    'restoredraft pagebreak undo redo save | hr | blocks fontfamily fontsize | formatselect | bold italic forecolor backcolor strikethrough | \
                    alignleft aligncenter alignright alignjustify | \
                    bullist numlist outdent indent | removeformat | help | ltr rtl',
                setup: function () {
                    // window.tinymce.activeEditor.mode.set("readonly");
                }
            },
            selectedRevision: null
        }
    },
    mounted() {
        this.getContract()      
    },
    components: {
        // HtmlDiff,
        documentView,
    },
    computed: {
        ...mapGetters('Auth',['authUser', 'authStatus', 'authError']),
        ...mapGetters('User',['userData',]),
    },
    methods: {
        popupHistory: function() {
            if (this.popHistory === false && this.contract.revisions !== undefined) {
                if (this.contract.revisions.length > 0) {
                    this.selectRevision(this.contract.revisions[0])
                }
            } else {
                this.selectedRevision = null
            }
            this.popHistory = !this.popHistory
        },
        hideColumnContent: function() {
            this.hideContent = !this.hideContent
        },
        handleContractDocument(event){
            this.contractDocument = event.target.files[0]
        },
        confirmEditContract: function() {
            this.getContract()
            if (this.contract.live_editor === this.userData.username) {
                if (this.contract.document !== null) {
                    this.downloadContract()
                }
            }
            else if (this.contract.live_edit === true) {
                this.$swal({
                    text: 'This contract is being edited by ' + this.contract.live_editor + '. Send email to request for update.',
                    icon: 'error',
                    showCancelButton: true,
                    confirmButtonText: 'Send email',
                    confirmButtonColor: '#073A82',
                    cancelButtonText: 'No, just download contract',
                    reverseButtons: true
                }).then((result) => {
                    
                    if (result.isConfirmed) {
                        this.contractUpdateRequest()                                        
                    } else {
                        if (this.contract.document !== null) {
                            this.downloadContract()
                        }
                    }
                });
            } else {
                this.$swal({
                    text: 'Mark this contract as being edited by you. No else can edit until you submit the updated contract or a day has already passed without any update.',
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Proceed',
                    confirmButtonColor: '#073A82',
                    cancelButtonText: 'No, just download contract',
                    reverseButtons: true
                }).then((result) => {
                    if (result.isConfirmed) {
                        this.markContractForEdit()
                        if (this.contract.document !== null) {
                            this.downloadContract()  
                        }              
                    }
                });
            }
        },
        downloadContract: function() {
            this.contract.document = this.contract.document + "/"
            axios.get(this.contract.document, { responseType: 'blob' })
            .then(response => {
                const blob = new Blob([response.data], { type: 'application/pdf' })
                const link = document.createElement('a')
                link.href = URL.createObjectURL(blob)
                link.download = this.contract.target.title + '_contract.docx'
                link.click()
                URL.revokeObjectURL(link.href)
            }).catch(console.error)
        },
        selectRevision: function(revision) {
            if (revision.changes === null) {
                this.getRevision(this.contract.id, revision.id)
            } else {
                this.selectedRevision = revision
            }
        },
        async getContract() {
            try {
                const response = await contracts.contract(this.$route.params.contractId)
                this.contract = response.data
                // window.tinymce.activeEditor.mode.set("readonly");
                // if (this.contract.live_edit === true && this.contract.live_editor !== this.userData.username) {
                //     window.tinymce.activeEditor.mode.set("readonly");
                // }
            } catch (err) {
                console.log(err)
            }
        },
        async markContractForEdit() {
            try {
                const response = await contracts.contractEdit(this.$route.params.contractId)
                this.contract = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async contractUpdateRequest() {
            try {
                await contracts.contractUpdateRequest(this.$route.params.contractId)
                window.toast.fire({
                    icon: 'success',
                    title: 'Request sent'
                })
            } catch (err) {
                console.log(err)
            }
        },
        async getRevision(contractId, revisionId) {
            try {
                const response = await contracts.contractRevision(contractId, revisionId)
                this.selectedRevision = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async updateContract() {
            try {
                
                const fd = new FormData()
                fd.append('start_date',this.contract.start_date)
                fd.append('end_date',this.contract.end_date)
                fd.append('contact_emails',this.contact_emails)
                fd.append('content',this.contract.content)

                if (this.contractDocument !== null) {
                    fd.append('document',this.contractDocument)
                }

                await contracts.updateContract(this.contract.id, fd)
                window.toast.fire({
                    icon: 'success',
                    title: 'Contract updated successfully'
                })

                this.$router.push('/buyer/contracts/supplier/categories/' + this.contract.category.id + '/contracts')
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

.revisions-select {
    width: 40%;

    &__option{
        width: 100%;
    }
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

.hidecontent {
    @include grid_row;

    &__icon {
        cursor: pointer;
    }
}

.column-details__content {
    transition: height 2s linear 1s;
}

.green {
    color: $color-green-main;
}
</style>
