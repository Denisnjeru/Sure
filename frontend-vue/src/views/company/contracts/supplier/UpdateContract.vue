<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                <span @click="$router.go(-1)" class="page__head--back"><font-awesome-icon  icon="chevron-left"/> &nbsp;Back</span>
                Update Contract
            </span>
            <div class="page__head--links">                
                <a class="page__head--link button button-link" @click="popupHistory()">
                    History
                </a>
            </div>
        </div>
        <form class="form" v-on:submit.prevent="updateContract()">
        <div class="page__content columns is-multiline">
            <div class="column is-12 column-details" v-if="contract.supplier">
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
                <div class="column-details__content" v-if="hideContent === false">
                    <div class="field">
                        <label class="label">Category <span class="required">*</span></label>
                        <div class="control">
                            <input readonly class="input readonly" type="text" :value="contract.category.name">
                        </div>
                    </div> 
                    <div class="field">
                        <label class="label">Supplier <span class="required">*</span></label>
                        <div class="control">
                            <input readonly class="input readonly" type="text" :value="contract.supplier.company_name">
                        </div>
                    </div>  
                    <div class="field">
                        <label class="label">Contact Name <span class="required">*</span></label>
                        <div class="control">
                            <input readonly class="input readonly" type="text" :value="contract.supplier.contact_name">
                        </div>
                    </div> 
                    <div class="field">
                        <label class="label">Contact Phone Number <span class="required">*</span></label>
                        <div class="control">
                            <input readonly class="input readonly" type="text" :value="contract.supplier.phone_number">
                        </div>
                    </div> 
                    <div class="field">
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
                            <input v-model="contract.start_date" class="input" type="date">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Contract End Date <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="contract.end_date" class="input" type="date">
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
                    <div class="field">
                        <label class="label" v-if="contract.live_edit === true">Live Editing: 
                            <span class="green" v-if="userData.username === contract.live_editor">Me</span>
                            <span class="green" v-else> {{contract.live_editor}}</span></label>
                        <div class="control">
                            <editor 
                                api-key='ilebf08k7e8o2y9rvuxb1tngrsz9ag0emag1yeqbb0oit0uu'
                                v-model="contract.content"
                                :init="config"                            
                            />
                        </div>
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
                        
                    </div>
                </div>
                <div class="page__content columns">
                    <div class="column is-12 column-page">
                        <HtmlDiff :old="contract.content" :current="last_revision.content"/>
                    </div>                        
                </div>
            </span>
        </div>
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div><div class="column is-3">
                <input v-if="contract.live_editor === userData.username" type="submit" class="button button-submit" value="Save">
            </div>
        </div>
        </form>     
    </div>
</template>

<script>
import contracts from '@/services/company/contracts'
import HtmlDiff from '@/components/HtmlDiff'
import { mapGetters } from 'vuex'

export default {
    name: 'Dashboard',
    data() {
        return {
            contractSource: "write",
            contact_emails: '',
            hideContent: true,
            contract: {},
            last_revision: {},
            popHistory: false,
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
            }
        }
    },
    mounted() {
        this.getContract()      
    },
    components: {
        HtmlDiff,
    },
    computed: {
        ...mapGetters('Auth',['authUser', 'authStatus', 'authError']),
        ...mapGetters('User',['userData',]),
    },
    methods: {
        popupHistory: function() {
            if (this.popHistory === false) {
                this.getLastRevision()
            }
            this.popHistory = !this.popHistory
        },
        hideColumnContent: function() {
            this.hideContent = !this.hideContent
        },
        async getContract() {
            try {
                const response = await contracts.supplierContractEdit(this.$route.params.contractId)
                this.contract = response.data
                if (this.contract.live_edit === true && this.contract.live_editor !== this.userData.username) {
                    window.tinymce.activeEditor.mode.set("readonly");
                }
            } catch (err) {
                console.log(err)
            }
        },
        async getLastRevision() {
            try {
                const response = await contracts.supplierContractLastRevision()
                this.last_revision = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async updateContract() {
            try {
                
                let payload = {
                    "type": "save",
                    "content": this.contract.content
                }

                await contracts.supplierContractEditSave(this.contract.id, payload)

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
