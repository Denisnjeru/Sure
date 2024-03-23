<template>
    <div class="risk_provide_ra_instructions">
        <div class="page__head">
            <span class="page__head--title">
                <span class="left nav-links__link">
                    <font-awesome-icon icon="chevron-left" />  <span class="text">Back</span>
                </span>
            </span>
        </div>
        <div class="page__content">
            <div class="columns is-centered">
                <div class="column-details column is-6">
                    <form v-on:submit.prevent="finish_ra()">
                        <div class="column-details__head">
                            <p class="column-details__head--title">Provide risk assessment instructions to each
                                question in each of the tabs listed below
                            </p>
                        </div>
                        <!-- Form Details -->
                        <div class="column-details__content">
                            <span v-for="section in riskassessment.qa_sections" :key="section.id">
                                <div class="detail">
                                    <span class="collapsible_link" @click="toggle(section)">
                                        <a class="collapsible_link--link">{{ section.name }}</a><font-awesome-icon class="nav-links__link--icon" icon="chevron-right" v-if="activeSection == section.id"/><font-awesome-icon class="nav-links__link--icon" icon="chevron-down" v-else/>
                                    </span>
                                        <div v-if="activeSection == section.id">
                                            <span v-for="question in section.risk_questions" :key="question.id">
                                                <form v-on:submit.prevent="create_ra_questions(question)">
                                                    <div class="content">
                                                        <div class="detail">
                                                            <span class="detail__questiontitle">Question: </span><span class="detail__title"> {{ question.description }}</span>
                                                                <div class="field">
                                                                    <label class="label">Verification instructions</label>
                                                                    <div class="control">
                                                                        <textarea class="input" name="description" spellcheck="true" rows="200" cols="50" v-model="question.verification_instruction"/>
                                                                    </div>
                                                                </div>
                                                            <div class="risk_submit">
                                                                <input type="submit"  class="button button-submit" value="Submit">
                                                            </div>
                                                        </div>
                                                    </div>
                                                </form>
                                            </span>
                                        </div>
                                        <div v-else></div>
                                </div>
                            </span>
                        </div>
                        <div class="finish_button">
                            <input type="submit"  class="button button-submit" value="Finish">
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import risk_management from '@/services/company/risk_management'

    export default {
        name:'provide-risk-assessment-instruction-buyer',
        data(){
            return{
            showCollapsible: false,
            activeSection: null,
            riskassessment: {
                'id': 0,
                'title': '',
                'category': '',
                'qa_sections': [{
                    'category': null,
                    'description': '',
                    'id': null,
                    'name': '',
                    'risk_questions': [{
                        'answer_type': null,
                        'description': '',
                        'description_slug': '',
                        'id': null,
                        'is_dd': false,
                        'is_qa': false,
                        'is_required': false,
                        'is_scored': false,
                        'max_score': "0.00",
                        'section': "Declaration",
                        'short_description': '',
                        'trans_description': '',
                        'trans_short_description': '',
                        'verification_instruction': ''
                    }],
                    'short_name': ''

                }],
            },
            error_text: '',
            }
        },
        components:{
        },
        computed:{
        },
        mounted(){
            this.get_ra_sections()
        },
        created:{
        },
        methods:{
            toggle(section){
                this.showCollapsible = !this.showCollapsible
                this.activeSection = section.id
                console.log(this.activeSection)
            },
            async create_ra_questions(question){
                let payload =  {}
                payload['question'] = question.id
                payload['verification_instruction'] = question.verification_instruction

                try{
                    const response = await risk_management.createRiskAssessmentQuestion(payload, this.$route.params.raId)
                        
                    if(response.status == 201){
                        console.log(response.data)
                        window.toast.fire({icon: 'success', title: "QA instruction created successfully"})
                    }else{
                        window.toast.fire({icon: 'error', title: "Error creating QA question instruction"})
                    } 
                } catch (error){
                    console.log('Logging the error')
                    console.log(error.response)
                    window.toast.fire({icon: 'error', title: error.response.data['error']})
                }
            },
            async finish_ra(){
                let payload =  []
                for (let i in this.riskassessment.qa_sections) {
                    for (let y in  this.riskassessment.qa_sections[i].risk_questions) {
                        let x = {}
                        x['question'] = this.riskassessment.qa_sections[i].risk_questions[y].id
                        x['verification_instruction'] = this.riskassessment.qa_sections[i].risk_questions[y].verification_instruction
                        payload.push(x);
                    }
                }
                console.log(payload)
                try{
                    const response = await risk_management.createRiskAssessmentQuestions(payload, this.$route.params.raId)
                    
                    if(response.status == 201){
                        console.log(response.data)
                        window.toast.fire({icon: 'success', title: "QA questions created successfully"})
                        this.$router.push('/buyer/section/'+ this.$route.params.categoryId +'/'+response.data['id']+'/risk-management/')
                    }else{
                        window.toast.fire({icon: 'error', title: "Error QA questions !"})
                    } 

                }catch(error){
                    console.log('Logging the error')
                    console.log(error.response)
                    window.toast.fire({icon: 'error', title: error.response.data['error']})
                }
            },
            async get_ra_sections(){
                try {
                    const response = await risk_management.getRiskAssessmentRASections(this.$route.params.categoryId)
                    console.log(response.data)
                    this.riskassessment = response.data
                } catch (error) {
                    console.log('Logging the error')
                    console.log(error.response)
                    window.toast.fire({icon: 'error', title: error.response.data['error']})
                }
            },
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
        &__collapsible {
            background-color: #777;
            color: white;
            cursor: pointer;
            padding: 18px;
            width: 100%;
            border: none;
            text-align: left;
            outline: none;
            font-size: 15px;
            .active, &:hover{
                background-color: #073A82;
            }
        }
        &__content {
            padding: $line-height/2 $line-height;
            margin-bottom: $line-height*2;

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

                .content{
                    padding: $line-height/2 $line-height;
                    .detail{
                        padding: $line-height 0;
                        border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);

                        &__questiontitle{
                            color: $color-blue-main;
                            display: inline;
                        }
                        &__title {
                            font-weight: 600;
                            display: inline;
                            margin-right: $line-height/2;
                            color: $color-black-main;
                        }
                    }
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
            .collapsible_link{
                text-align: center;
                
                &--link{
                    display: inline;
                    margin-right: 0.5em;
                    color: $color-blue-main;
                }

                &:hover, :focus {
                    box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                    transform: translateY(-0.25em);
                }
            }

        }
    }

    .finish_button{
        padding: $line-height/2 $line-height/2;
        margin: $line-height/2 0;
        
        .button-submit {
            width: 100%;
            color: $color-white-main;
            background-color: $color-blue-main;
            border: none;                
            font-size: $font-size-text;
        }

        &:hover, :focus {
            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
            transform: translateY(-0.25em);
        }
    }

    }

}
</style>