<template>
    <div class="dashboard">
        <div class="page__head is-vcentered">
            <span @click="$router.go(-1)" class="page__head--back"><font-awesome-icon  icon="chevron-left"/> &nbsp;Back</span>            
            <span class="page__head--title">
                New Buyer
            </span>
            <div class="page__head--links">
            </div>
        </div>
        <form class="form" v-on:submit.prevent="createBuyer()">
        <div class="page__content columns is-centered is-multiline">
            <div class="column is-8 column-details">
                <div class="column-details__head">
                    <p class="column-details__head--title">Add New Buyer</p>
                    <p class="column-details__head--desc">Fill in the required details.</p>
                </div>
                <div class="column-details__content">                    
                    <div class="field">
                        <label class="label">Company Name <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="company.company_name" class="input" type="text">
                        </div>
                    </div>  
                    <div class="field">
                        <label class="label">Initials <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="company.buyer_initials" class="input" type="text">
                        </div>
                    </div> 
                    <div class="field">
                        <label class="label">Upload Logo <span class="required">*</span></label>
                        <div class="control">
                           <label class="file-label">
                                <input class="file-input" type="file" name="companLogo" @change="handleCompanyLogo">
                                <span class="file-cta">
                                    <span class="file-icon">
                                        <i class="fas fa-upload"></i>
                                    </span>
                                    <span class="file-label">
                                        Choose company logo...
                                    </span>
                                </span>
                                <span class="file-name" v-if="companyLogo !== null">
                                    {{companyLogo.name}}
                                </span>
                                <span class="file-name" v-else>
                                    No file selected
                                </span>
                            </label>
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Country <span class="required">*</span></label>
                        <div class="select">
                            <country-select v-model="company.country" :country="company.country" :countryName="true" topCountry="KE" />
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">KRA PIN/Tax Registration <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="company.kra_pin_number" class="input" type="text">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Contact name <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="company.contact_name" class="input" type="text">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Phone number <span class="required">*</span></label>
                        <div class="control">
                            <input v-model="company.phone_number" class="input" type="text">
                        </div>
                    </div>
                </div>
                <div class="column-details__content is-centered additions form-submit">     
                    <input type="submit" class="button button-submit" value="Create buyer">
                </div>
            </div>
        </div>  
        <div class="columns additions">
            <div class="column is-9">
                <p class="note"></p>
            </div>
            <div class="column is-3">
               <!-- <input type="submit" class="button button-submit" value="Create role"> -->
            </div>
        </div>
        </form>     
    </div>
</template>

<script>
import buyer from '@/services/qed/buyer'

export default {
    name: 'QedBuyerCreate',
    data() {
        return {
            company: {
                "country": 'Kenya'
            },
            companyLogo: null
        }
    },
    methods: {
        async search() {
            console.log('search');
        },
        handleCompanyLogo(event){
            this.companyLogo = event.target.files[0]
        },
        async createBuyer(){
            try {
                const fd = new FormData();
                fd.append('company_name', this.company.company_name)
                fd.append('phone_number',this.company.phone_number)
                fd.append('contact_name', this.company.contact_name)
                fd.append('country',this.company.country)
                fd.append('buyer_initials',this.company.buyer_initials)
                fd.append('kra_pin_number',this.company.kra_pin_number)
                fd.append('company_logo_url', this.companyLogo)

                const response = await buyer.createBuyer(fd)
                window.toast.fire({
                    icon: 'success',
                    title: response.data.company_name + ' created successfully'
                })
                this.$router.push('/qed/buyers')
            } catch (err) {
                window.toast.fire({
                    icon: 'error',
                    title: err.response.data
                })   
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
    margin-top: $line-height;

}

.dashboard {
    position: relative;
}

.readonly {
    background-color: $color-gray-light;
}


// .form-submit {
//     @include grid_row;
//     justify-content: center;

//     .button-submit {
//         width: 60% !important;
//     }
// }

</style>
