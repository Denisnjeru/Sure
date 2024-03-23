<template>
    <div class="dashboard">
        <div class="page__head">
            <span class="page__head--title">
                Update Contract Section
            </span>
        </div>
        <form class="form" v-on:submit.prevent="updateSection()">
        <div class="page__content columns">
            <div class="column is-12 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Contract Section Details</p>
                    <p class="column-details__head--desc"></p>
                </div>
                <div class="column-details__content">
                    <div class="field" v-if="contractSection.name">
                        <label class="label">Section Name <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="contractSection.name" class="input" type="text">
                        </div>
                    </div> 
                    <div class="field" v-if="contractSection.content">
                        <label class="label">Section Content <span class="required">*</span></label>
                        <div class="control">
                            <editor 
                                v-model="contractSection.content"
                                :init="{
                                    height: 400,
                                    plugins: [
                                        'advlist autolink lists link image charmap print preview anchor',
                                        'searchreplace visualblocks code fullscreen',
                                        'insertdatetime media table paste code help wordcount'
                                    ],
                                }" 
                            />
                            
                        </div>
                    </div>   
                </div>
            </div>
        </div>  
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div>
            <div class="column is-3">
                <input type="submit" class="button button-submit" value="Update section">
            </div>
        </div>
        </form>     
    </div>
</template>

<script>
import contracts from '@/services/company/contracts'

export default {
    name: 'BuyerContractsTemplatesSectionsUpdate',
    data() {
        return {
            contractSection: {}
        }
    },
    mounted() {
        this.getContractSection()
    },
    methods: {
        async search() {
            console.log('search');
        },
        async getContractSection() {
            try {
                const response = await contracts.contractSection(this.$route.params.sectionId)
                this.contractSection = response.data
            } catch (err) {
                console.log(err)
            }
        },
        async updateSection(){
            try {
                const response = await contracts.updateContractSection(this.$route.params.sectionId, this.contractSection)
                window.toast.fire({
                    icon: 'success',
                    title: response.data.name + ' updated successfully'
                })
                this.$router.push('/buyer/contracts/sections')
            } catch (err) {
                console.log(err.response)      
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
