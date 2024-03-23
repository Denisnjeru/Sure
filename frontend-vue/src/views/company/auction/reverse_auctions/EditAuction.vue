<template>
    <div class="risk_category_add">
        <div class="page__head">
            <span class="page__head--title">
                <span class="left nav-links__link">
                    <router-link
                        to="{this.router.go(-1)}"
                    >
                        <font-awesome-icon icon="chevron-left" />  <span class="text">Back</span>
                    </router-link>
                </span>
            </span>
        </div>
        <div class="page__content">
            <div class="columns is-centered">
                <div class="column-details column is-12">
                    <form v-on:submit.prevent="edit_reverse_auction()" enctype="multipart/form-data">
                        <div class="column-details__head">
                            <p class="column-details__head--title">Edit a Reverse Auction</p>
                            <p class="column-details__head--desc">Fill in the required details</p>
                        </div>
                        <!-- Form Details -->
                        <div class="column-details__content">
                            <div class="columns">
                                <div class="column">
                                    <div class="field">
                                        <label class="label">Auction Name <span class="required">*</span></label>
                                        <div class="control">
                                            <input class="input" type="text" placeholder="Enter category name" v-model="reverse_auction.name" required>
                                        </div>
                                    </div>
                                    <!-- @change="onTypeChange($event)" -->
                                    <div class="field">
                                        <label class="label">Type<span class="required">*</span></label>
                                        <div class="select"> 
                                            <select v-model="selectedType" id="selectType" required>
                                                <option>Reverse Auction</option>
                                            </select>
                                        </div>                                    
                                    </div>
                                    <div class="selected">
                                        <span v-if="selectedType !='' ">
                                            <span class="selected__item currency">
                                                {{selectedType}}
                                                <span class="selected__icon">
                                                    <img class="selected__icon--img" src="@/assets/Vector.png" alt="">
                                                </span>
                                            </span>
                                        </span>
                                    </div>
                                    <div class="field expiry">
                                        <label class="label">Opening Time <span class="required">*</span></label>
                                        <div class="control">
                                            <input class="input" type="datetime-local" placeholder="Enter Opening Date" v-model="reverse_auction.opening_date" required>
                                        </div>
                                    </div>
                                    <div class="field expiry">
                                        <label class="label">Closing Time <span class="required">*</span></label>
                                        <div class="control">
                                            <input class="input" type="datetime-local" placeholder="Enter Closing Date" v-model="reverse_auction.closing_date" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="column">

                                    <div class="field">
                                        <div class="control">
                                            <div class="show_bids">
                                                <input type="checkbox" v-model="reverse_auction.closed_auction">
                                                <span class="text"> Closed Auction </span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="field">
                                        <label class="label">Overtime Count </label>
                                        <div class="control">
                                            <input class="input" type="number" min="0" max="10" oninput="this.value = Math.round(this.value);" v-model="reverse_auction.overtime_count"/>
                                        </div>
                                    </div>
                                    <div class="field">
                                        <label class="label">Overtime Duration (Minute(s)) </label>
                                        <div class="control">
                                            <input class="input" type="number" min="0" max="10" oninput="this.value = Math.round(this.value);" v-model="reverse_auction.overtime_duration"/>
                                        </div>
                                    </div>
                                    <div class="document">
                                        <p class="document__title">
                                            <span class="document__title--name">Supporting Document</span>
                                            <span class="document__title--icon">
                                                <font-awesome-icon class="icon" icon="folder-plus" />
                                            </span>
                                        </p>
                                        <span v-if="SupportingfileNames[0]" class="document__name">
                                            <span class="document__name--text">
                                                <img src="@/assets/support_doc.png" class="icon">
                                                <span class="name">{{ SupportingfileNames[0] }}</span>
                                            </span>
                                            <span class="document__name--delete" @click="removesupportingdocfile()">
                                                <span class="selected__icon">
                                                    <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                                                </span> 
                                            </span>
                                        </span>
                                        <div class="file has-name">
                                            <label class="file-label">
                                                <input class="file-input" type="file" name="resume" @change="selectSupportingDocument($event)">
                                                <span class="file-cta">
                                                <span class="file-icon">
                                                    <i class="fas fa-upload"></i>
                                                </span>
                                                <span class="file-label">
                                                    Choose a file…
                                                </span>
                                                </span>
                                                <span v-if="SupportingfileNames[0]" class="file-name">{{ SupportingfileNames[0] }}</span>
                                                <span v-else class="file-name">Upload Supporting Document</span>
                                            </label>
                                        </div>
                                    </div>
                                    <div class="document">
                                        <p class="document__title">
                                            <span class="document__title--name">Excel Template</span>
                                            <span class="document__title--icon">
                                                <font-awesome-icon class="icon" icon="folder-plus" />
                                            </span>
                                        </p>
                                        <span v-if="ExcelfileNames[0]" class="document__name">
                                            <span class="document__name--text">
                                                <img src="@/assets/excel.png" class="icon">
                                                <span class="name">{{ExcelfileNames[0]}}</span>
                                            </span>
                                            <span class="document__name--delete" @click="removeexcelfile()">
                                                <span class="selected__icon">
                                                    <img class="selected__icon--img" src="@/assets/circle-xmark-solid.png" alt="">
                                                </span> 
                                            </span>
                                        </span>
                                        <div class="file has-name">
                                            <label class="file-label">
                                                <input class="file-input" type="file" @change="selectExcelDocument($event)">
                                                <span class="file-cta">
                                                <span class="file-icon">
                                                    <i class="fas fa-upload"></i>
                                                </span>
                                                <span class="file-label">
                                                    Choose a file…
                                                </span>
                                                </span>
                                                <span v-if="ExcelfileNames[0]" class="file-name">{{ExcelfileNames[0]}}</span>
                                                <span v-else class="file-name">Upload Items Template</span>
                                            </label>
                                        </div>
                                    </div>
                                    <div class="risk_submit">
                                        <input type="submit" class="button button-submit" value="Update">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import auctions from '@/services/company/auction'

    export default {
        name:'edit-reverse-auction-buyer',
        data(){
            return{
                selectedType: '',
                selectedPricingMethod: '',
                reverse_auction: {},
                error_text: '',
                ExcelfileNames: [],
                SupportingfileNames: [],
                ExceluploadedFiles: [],
                SupportinguploadedFiles: [],

            }
        },
        mounted(){
            this.setTypeTo(),
            this.get_auction()
        },
        methods:{
            onTypeChange(e){
                if (e.target.value != 'Select Auction Type'){
                    this.selectedType = e.target.value
                    this.reverse_auction.auction_type = e.target.value
                }else{
                    this.selectedType = ''
                }
            },
            setTypeTo(){
                this.reverse_auction.auction_type = 'Reverse Auction'
                this.selectedType = 'Reverse Auction'
            },
            onMethodChange(e){
                if (e.target.value != 'Select Pricing Method'){
                    this.selectedPricingMethod = e.target.value
                    this.reverse_auction.pricing_method = e.target.value
                }else{
                    this.selectedPricingMethod = ''
                    this.reverse_auction.pricing_method = ''
                }
            },
            removeexcelfile(){
                this.reverse_auction.event_template = null;
                this.ExcelfileNames = []
            },
            removesupportingdocfile(){
                this.reverse_auction.supporting_document = null;
                this.SupportingfileNames = []
            },
            removeselectedpricing() {
                this.selectedPricingMethod = ''
            },  
            selectSupportingDocument(event){ 
                let fieldName = event.target.name;
                let fileList =  event.target.files;

                if (!fileList.length) return;
                this.reverse_auction.supporting_document = event.target.files[0]
            
                const fd = new FormData()
                Array
                .from(Array(fileList.length).keys())
                .map(x => {
                    fd.append(fieldName, fileList[x], fileList[x].name);
                });
                
                this.SupportingfileNames = [];
                Array
                .from(Array(fileList.length).keys())
                .map(x => {
                    this.SupportingfileNames.push(fileList[x].name);
                });
                

                console.log(this.SupportingfileNames)
                console.log(this.reverse_auction.supporting_document)
            },
            selectExcelDocument(event){
                let fieldName = event.target.name;
                let fileList =  event.target.files;

                if (!fileList.length) return;
                this.reverse_auction.excel_template = event.target.files[0]
            
                const fd = new FormData()
                Array
                .from(Array(fileList.length).keys())
                .map(x => {
                    fd.append(fieldName, fileList[x], fileList[x].name);
                });
                
                
                Array
                .from(Array(fileList.length).keys())
                .map(x => {
                    this.ExcelfileNames.push(fileList[x].name);
                });

                console.log(this.ExcelfileNames)
                console.log(this.reverse_auction.excel_template)
            },
            async edit_reverse_auction(){
                try {
                    if (this.reverse_auction.name !== ''  && this.reverse_auction.opening_date  !== '' && this.reverse_auction.closing_date !== ''){
                        
                        const fd = new FormData()
                        fd.append('name',this.reverse_auction.name)
                        fd.append('auction_type',this.reverse_auction.auction_type)
                        fd.append('opening_date',this.reverse_auction.opening_date)
                        fd.append('closing_date',this.reverse_auction.closing_date)
                        fd.append('auction_type',this.reverse_auction.auction_type)
                        fd.append('closed_auction',this.reverse_auction.closed_auction)
                        fd.append('category_type',this.reverse_auction.category_type)

                        if ((this.reverse_auction.supporting_document !== null) && (typeof this.reverse_auction.supporting_document != 'string')){
                            fd.append('supporting_document',this.reverse_auction.supporting_document)
                        }

                        if ((this.reverse_auction.excel_template !== null) && (typeof this.reverse_auction.excel_template != 'string')){
                            fd.append('excel_template', this.reverse_auction.excel_template)
                        }
                        
                        fd.append('overtime_count',this.reverse_auction.overtime_count)
                        fd.append('overtime_duration',this.reverse_auction.overtime_duration)
                        
                        console.log(fd)
                        const response = await auctions.updateAuction(this.$route.params.auctionId, fd)
                        console.log(response.status)
                        if(response.status == 200){
                            console.log(response.data)
                            window.toast.fire({icon: 'success', title: "Auction updated successfully"})
                            this.$router.push('/buyer/'+ response.data.id +'/reverse/auction')
                        }
                    }else{
                        // No Name
                        if(this.reverse_auction.name == ''){
                            this.error_text = 'Please add auction name !'
                        }
                        // No Opening Date
                        if(this.reverse_auction.opening_date == ''){
                            this.error_text = 'Please add opening date !'
                        }
                        // No Closing Date
                        if(this.reverse_auction.closing_date == ''){
                            this.error_text = 'Please add closing date !'
                        }
                        window.toast.fire({icon: 'error', title: this.error_text})
                    }
                }catch(error){
                    console.log('Logging the error')
                    console.log(error.response)
                    window.toast.fire({icon: 'error', title: JSON.stringify(error.response.data)})
                }
            },
            async get_auction(){
                try{
                    let response = await auctions.getRetrieveAuction(this.$route.params.auctionId)
                    console.log('Fecthed Items !')
                    
                    if(response.data['supporting_document'] !== null){
                        let filename = ''
                        try{
                            filename = new URL(response.data['supporting_document']).pathname.split('/').pop();
                            this.SupportingfileNames.push(filename)
                            console.log(`filename: `, filename)
                        }catch(e){
                            console.log('error: ',e)
                        }
                    }

                    if(response.data['excel_template'] !== null){
                        let filename = ''
                        try{
                            filename = new URL(response.data['excel_template']).pathname.split('/').pop();
                            this.ExcelfileNames.push(filename)
                            console.log(`filename: `, filename)
                        }catch(e){
                            console.log('error: ',e)
                        }
                    }
                    this.reverse_auction = response.data
                    console.log(this.reverse_auction)
                }catch (err){
                    window.toast.fire({icon: 'error', title: err})
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

        &__content {
            padding: $line-height/2 $line-height;
            margin-bottom: 0;

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
            .show_bids {
                display: inline-block;
                color: $color-blue-main;

                .text {
                    font-size: $font-size-text;
                    font-weight: 600;
                    padding: 12px;
                }
            }
        }

        input[type="number"] {
            -webkit-appearance: textfield !important;
            -moz-appearance: textfield !important;
            appearance: textfield !important;
        }

        input[type=number]::-webkit-inner-spin-button,
        input[type=number]::-webkit-outer-spin-button {
            -webkit-appearance: none;
        }

        .wrapper {
            border: 2px #dcd3d3 solid;
            display: flex;
            border-radius: 15px;
        }

        .plusminus {
            height: 100%;
            width: 30%;
            background: white;
            border: none;
            font-size: 40px;
            color: #5f5fce;
        }

        .num {
            height: 10%;
            width: 10%;
            border: none;
            font-size: 30px;
        }
    }

    }

}
</style>