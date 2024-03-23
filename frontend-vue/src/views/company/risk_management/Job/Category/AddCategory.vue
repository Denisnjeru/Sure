<template>
    <div class="risk_category_add">
        <div class="page__head">
            <span class="page__head--title">
                <span class="left nav-links__link">
                    <router-link
                        to="{this.router.go(-1)}"
                    >
                        <font-awesome-icon icon="chevron-left" /><span class="text">Back</span>
                    </router-link>
                </span>
            </span>
        </div>
        <div class="page__content">
            <div class="columns is-centered">
                <div class="column-details column is-6">
                    <form v-on:submit.prevent="create_risk_category()">
                        <div class="column-details__head">
                            <p class="column-details__head--title">Add a category</p>
                            <p class="column-details__head--desc">Entered on registration</p>
                        </div>
                        <!-- Form Details -->
                        <div class="column-details__content">
                            <div class="field">
                                <label class="label">Category Name <span class="required">*</span></label>
                                <div class="control">
                                    <input class="input" type="text" placeholder="Enter category name" v-model="category.name">
                                </div>
                            </div>
                            <div class="field">
                                <label class="label">Category Code <span class="required">*</span></label>
                                <div class="control">
                                    <input class="input" type="text" placeholder="Enter category code" v-model="category.unique_reference">
                                </div>
                            </div>
                            <div class="field">
                                <label class="label">Bid Charge <span class="required">*</span></label>
                                <div class="control">
                                    <input class="input" type="number" placeholder="Enter bid charge" v-model="category.bid_charge">
                                </div>
                            </div>
                            <div class="document">
                                <p class="document__title">
                                    <span class="document__title--name">Supporting Documents</span>
                                    <span class="document__title--icon">
                                        <font-awesome-icon class="icon" icon="folder-plus" />
                                    </span>
                                </p>
                                <div class="file has-name">
                                    <label class="file-label">
                                        <input class="file-input" type="file" multiple name="resume"
                                        @change="filesChange($event.target.name, $event.target.files); fileCount = $event.target.files.length">
                                        <span class="file-cta">
                                            <span class="file-icon">
                                                <font-awesome-icon class="nav-links__link--icon" icon="file-upload" />
                                            </span>
                                            <span v-if="isInitial" class="file-label">
                                                Choose a file(s)…
                                            </span>
                                            <span v-else class="file-label">
                                                Uploading {{ fileCount }} files…
                                            </span>
                                        </span>
                                    </label>
                                </div>
                                <span v-for="file in fileNames" :key="file.id" class="document__name" >
                                    <span class="document__name--text">
                                        <img src="@/assets/support_doc.png" class="icon">
                                        <span class="name">{{ file }}</span>
                                    </span>
                                </span>
                            </div>
                            <div class="field expiry">
                                <label class="label">Opening Date <span class="required">*</span></label>
                                <div class="control">
                                    <input class="input" type="datetime-local" placeholder="Enter Opening Date" v-model="category.opening_date">
                                </div>
                            </div>
                            <div class="field expiry">
                                <label class="label">Closing Date <span class="required">*</span></label>
                                <div class="control">
                                    <input class="input" type="datetime-local" placeholder="Enter Closing Date" v-model="category.closing_date">
                                </div>
                            </div>
                            <div class="field">
                                <label class="label">Category Type<span class="required">*</span></label>
                                <div class="select">
                                    <select>
                                        <option>Select Category Type</option>
                                        <option>Supply of pharmaceutical drugs</option>
                                        <option>Provision of security guarding services</option>
                                    </select>
                                </div>                                    
                            </div>

                            <div class="field">
                                <div class="control">
                                    <div class="show_bids">
                                        <input type="checkbox" v-model="category.send_participant_list_to_supplier">
                                        <span class="text"> Send Participant List to Suppliers </span>
                                    </div>
                                </div>
                            </div>
                            <div class="field">
                                <div class="control">
                                    <div class="show_bids">
                                        <input type="checkbox" v-model="category.invite_only">
                                        <span class="text"> Invite Only </span>
                                    </div>
                                </div>
                            </div>
                            <div class="risk_submit">
                                <input type="submit"  class="button button-submit" value="Create">
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import risk_management from '@/services/company/risk_management'
const STATUS_INITIAL = 0, STATUS_SELECTED = 1;

    export default {
        name:'add-risk-management-category-buyer',
        data(){
            return{
                category: {
                    "name": '',
                    "unique_reference": '',
                    "opening_date": '',
                    "closing_date": '',
                    "bid_charge": 0.0,
                    "category_type": '',
                    "send_participant_list_to_supplier":false,
                    "invite_only":false,
                    formData : new FormData(),
                },
                uploadedFiles: [],
                currentStatus: 0,
                error_text: '',
                fileNames: []
            }
        },
        components:{
        },
        mounted:{
        },
        created:{
        },
        computed:{
            isInitial() {
                return this.currentStatus === STATUS_INITIAL;
            },
            isSelected() {
                return this.currentStatus === STATUS_SELECTED;
            }
        },
        methods:{
            reset() {
                // reset form to initial state
                this.currentStatus = STATUS_INITIAL;
                this.uploadedFiles = [];
                this.fileNames = [];
            },
            save() {
                // upload data to the server


                // upload(formData)
                // .then(x => {
                //     this.uploadedFiles = [].concat(x);
                //     this.currentStatus = STATUS_SUCCESS;
                // })
                // .catch(err => {
                //     this.uploadError = err.response;
                //     this.currentStatus = STATUS_FAILED;
                // });
            },
            filesChange(fieldName, fileList) {
                // handle file changes
                if (!fileList.length) return;

                this.currentStatus = STATUS_SELECTED;
                // append the files to FormData

                const fd = new FormData()
                Array
                .from(Array(fileList.length).keys())
                .map(x => {
                    fd.append(fieldName, fileList[x], fileList[x].name);
                });
                
                this.category.formData = fd
                // append the filenames to array
                Array
                .from(Array(fileList.length).keys())
                .map(x => {
                    this.fileNames.push(fileList[x].name);
                });

                Array
                .from(Array(fileList.length).keys())
                .map(x =>{
                    this.uploadedFiles.push(fileList[x]);
                });

                console.log(this.formData)
                console.log(this.fileNames)
                console.log(this.uploadedFiles)
            },
            async create_risk_category(){

                try {
                    if (this.category.name !== '' && this.category.unique_reference !== '' && this.category.opening_date  !== '' && this.category.opening_date !== ''){

                        const response = await risk_management.createRiskCategory( this.category, this.$route.params.riskId)
                        console.log(response.status)
                        if(response.status == 201){
                            console.log(response.data)
                            window.toast.fire({icon: 'success', title: "Risk Management category created successfully"})
                            this.$router.push('/buyer/category/'+ this.$route.params.riskId +'/'+response.data['id'] + '/risk-management/')
                        }
                    } else {
                        // No Name
                        if(this.category.name == ''){
                            this.error_text = 'Please add job name !'
                        }
                        // No Unique Reference
                        if(this.category.unique_reference == ''){
                            this.error_text = 'Please add job code !'
                        }
                        
                        // No Opening Date
                        if(this.category.opening_date == ''){
                            this.error_text = 'Please add opening date !'
                        }
                        // No Closing Date
                        if(this.category.closing_date == ''){
                            this.error_text = 'Please add closing date !'
                        }

                        window.toast.fire({icon: 'error', title: this.error_text})

                    }
                } catch (error) {
                    console.log('Logging the error')
                    console.log(error.response)
                    window.toast.fire({icon: 'error', title: error.response.data['error']})
                }
            }
        },
    }
</script>
<style lang="scss" scoped>

.page {

    .nav-links__link {
        color: $color-blue-main;

        .text {
            font-size: font-size-major;
            font-weight: 600;
        }

        &:hover {
            cursor: pointer;
        }
    }

    &__content {
        padding: $line-height 5%;
        position: relative;
        z-index: 20; 
    
    .column-details {
        margin: 0 $line-height/4;
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: $line-height/2;
        padding: 0;
        margin-bottom: $line-height/2;

        &__head {
            background: $color-baby-blue;
            padding: $line-height $line-height;
            border-radius: $line-height/2 $line-height/2 0 0;

            &--title {
                color: rgba(18, 31, 62, 0.8);
                font-size: $font-size-title;
                font-weight: 600;
                margin-bottom: $line-height/6 !important;
            }

            &--desc {
                color: $color-black-medium;
                margin: $line-height/4 0;
            }
        }

        &__content {
            padding: $line-height/2 $line-height;
            margin-bottom: 0;

            .show_bids {
                display: inline-block;
                color: $color-blue-main;

                .text {
                    font-size: $font-size-text;
                    font-weight: 600;
                    padding: 12px;
                }
            }
            .detail {
                padding: $line-height 0;
                border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);

                &__title {
                    font-weight: 600;
                    margin-right: $line-height/2;
                    color: $color-black-main;
                }

                &__text {
                    color: $color-lightblue-text;
                }
            }

            .document {
                padding: $line-height 0;
                border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);
                position: relative;
                z-index: 1;

                &__status {
                    position: absolute;
                    z-index: 20;
                    padding: $line-height/6 $line-height/3;
                    color: $color-lightblue-text;
                    background: #F2F6FF;
                    border: 1px solid #073A82;
                    box-sizing: border-box;
                    box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
                    border-radius: 10px;
                    font-size: $font-size-small;
                    left: 60%;
                    display: none;
                }                    

                &__title {
                    width: 100%;
                    @include grid_row;

                    &--name {
                        font-weight: 600;
                        color: $color-black-main;
                    }

                    &--icon {
                        color: $color-gray-main;
                    }

                    .missing {
                        color: $color-red-main;
                    }
                }

                &__name {
                    width: 100%;
                    @include grid_row;
                    align-items: center;
                    margin-top: $line-height/3;
                    background: #F8F8F8;
                    box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
                    border-radius: $line-height/2;
                    padding: $line-height/4 $line-height/2;
                    font-size: $font-size-text;

                    &--text {
                        @include grid_row;
                        align-items: center;

                        .icon {
                            margin-right: $line-height/4;
                            height: $line-height;
                        }
                    }

                    &--delete {

                        .selected__icon {
                            margin: 0 $line-height/4;

                            &--img {
                                height: $line-height/1.2;
                                padding: $line-height/6;
                                background-color: $color-gray-main;
                                color: $color-white-main;
                                border-radius: 50%;
                                cursor: pointer;

                                &:hover {
                                    background-color: $color-red-main;
                                }
                            }
                        }
                    }
                }

                &:hover {
                    .doc-missing {
                        color: $color-red-main;
                        cursor: pointer;
                    }

                    .document__status {
                        display: block;
                    }
                }
            }

            .risk_submit {
                padding: $line-height/2 0;
                // margin: $line-height/2 0;
                
                .button-submit {
                    width: 100%;
                    color: $color-white-main;
                    background-color: $color-blue-main;
                    border: none;                
                    font-size: $font-size-text;
                }
            }
        }
    }

    }

}
</style>