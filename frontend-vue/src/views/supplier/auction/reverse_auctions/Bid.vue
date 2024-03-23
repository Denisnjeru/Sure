<template>
    <div class="risksdsdsdsd">

        <div class="page__head">
            <span class="page__head--title">
                {{auctionObject.name}}
            </span>

            <div class="dates">
                <p class="close_date">You are logged in for this auction: {{socketStatus}}</p>
            </div>

            <div class="page__auction_header_details">
                <div class="auction-image-header-details">
            </div>
        </div>
        
        </div>

        
        <div class="page_content">
            <div class="column-details">
                <div>
                    <li v-for="auction_item in auctionItems"  v-bind:key="auction_item.id" :id="auction_item.id">
                        <AuctionItem :auctionitem="auction_item">
                        </AuctionItem>
                    </li>
                </div>
            </div>
        </div>

    </div>
</template>
<script>
import auctions from '../../../../services/supplier/auction'
import moment from 'moment'
// import Carousel from '../../../../components/auction/Carousel.vue'
import AuctionItem from '../../../../components/auction/AuctionItem'
import {mapGetters} from 'vuex'

const STATUS_INITIAL = 0, STATUS_SELECTED = 1;

export default {
    name: "risk-auction-participate-supplier",
    data() {
        return {
            auct: {
                "id": 0,
                "name": "",
                "auction_type": "",
                "category_type": "",
                "pricing_method": "",
                "closed_auction": false,
                "closing_date": "",
                "opening_date": "",
                "company": "",
                "is_open": false,
                "created_by": "",
                "created_at": "",
                "overtime_count": 0,
                "overtime_duration": 0,
                "auction_items": [],
            },
            bid_responses: [],
            wordextensions: ['.doc', '.docx'],
            excelextensions: ['.xlsx', '.xls'],
            pdfextensions: ['.pdf'],
            fileName: [],
            currentStatus: 0,
            formData : new FormData(),
            error_text: '',
            options: {
                headings: {},
                sortable: ["#", "Item Name", "Reserve Price"],
                sortIcon: {
                    is: "glyphicon-sort",
                    base: "glyphicon",
                    up: "glyphicon-chevron-up",
                    down: "glyphicon-chevron-down"
                },
            },
            page: 1,
            dataCount: 200,
            dataPerPage: 20,
        };
    },
    components: {
        // Carousel,
        AuctionItem,
    },
    filters: {
        moment: function (date) {
            return moment(date).format("MMMM Do YYYY, h:mm:ss a");
        }
    },
    mounted() {
        this.web_socket_connect();
        this.getReverseAuction();
        this.get_responses();
    },
    beforeDestroy() {
        console.log('Called before destroy')
        this.$socket.close()
        this.$store.dispatch('Auction/setReset')
    },
    // watch: {

    // },
    // created(){
    //     this.web_socket_connect();
    //     this.getReverseAuction();
    //     this.get_responses();
    //     this.test();
    // },
    computed:{
            isInitial() {
                return this.currentStatus === STATUS_INITIAL;
            },
            isSelected() {
                return this.currentStatus === STATUS_SELECTED;
            },
            ItemResponse(){
                return Item => {
                    let res = null
                    for(var i = 0, l = this.bid_responses.length; i < l; i++){
                        if( this.bid_responses[i].auction_item === Item.id){
                            res =  this.bid_responses[i].bid_price;
                        }
                    }
                    return res
                }
            },
            ...mapGetters('Auth', ['authUser']),
            ...mapGetters('Auction', ['socketStatus', 'auctionNotifications', 'auctionObject', 'auctionItems']),
    },
    methods: {
        reset() {
            // reset form to initial state
            this.currentStatus = STATUS_INITIAL;
            this.fileName = [];
        },
        getclosingtime: function(){
            return this.auct.closing_date
        },
        extensionsource: function(){
            return require('@/assets/excel.png')
        },
        async ProceedToBid() {
            this.$router.push("/supplier/bid/" + this.auct.id + "/reverse/auction");
        },
        async getReverseAuction() {
            try {
                this.$store.dispatch('Auction/setReset')
                const response = await auctions.getSupplierAuction(this.$route.params.auctionId);
                this.$store.dispatch('Auction/setAuctionObject', response.data)
                console.log('Yes')
                console.log(this.auctionItems)
            }
            catch (error) {
                console.log(error);
            }
        },
        async bid_auction(Item){
            try{
                let bid_amount = document.getElementById('bid_response_'+Item.id).value;
                let payload = {
                    'auction_item': Item.id,
                    'bid_price': bid_amount
                }
                console.log(payload)
                let response = await auctions.bid(Item.id, payload)
                if ((response.status === 200) || (response.status === 201)){
                    this.get_responses()
                    window.toast.fire({icon: 'success', title: "Bid Submitted"})
                }else{
                    window.toast.fire({icon: 'info', title: 'Have at it'})
                }
            }catch (err){
                console.log(err.response)
                window.toast.fire({icon: 'error', title: err.response})
            }
        },
        async get_responses(){
            try{
                let responses = await auctions.auctionResponses(this.$route.params.auctionId)
                this.bid_responses = responses.data
                console.log('Football', this.bid_responses)
            }catch(err){
                window.toast.fire({icon: 'error', title: err.response})
            }
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
            
            // this.category.formData = fd
            // append the filenames to array
            Array
            .from(Array(fileList.length).keys())
            .map(x => {
                this.fileName.push(fileList[x].name);
            });


            console.log(this.formData)
            console.log(this.fileName)
        },
        // On connection open
        socket_open: function(event) {
            // Send get lots function
            console.log(event)
            let payload = {
                pk: this.$route.params.auctionId,
                action: 'subscribe_to_activity_in_auction',
                request_id: this.authUser.user_id
            }
            this.$socket.send(JSON.stringify(payload));
        },
        // On connection close
        socket_close: function(event) {
            console.log(event)
        },
        // On connection error
        socket_error: function(error) {
            console.log(error)
        },
        // On connection message
        socket_message: function(event) {
            const data = JSON.parse(event.data)
            console.log([data.data])
            console.log('Event')
            const payload = [data.data]
            //console.log(payload.current)
            this.$store.dispatch('Auction/setAuctionItem', payload)
        },
        async web_socket_connect(){
            this.$socket = this.$WSClient;
            this.$socket.debug = true;
            this.$socket.reconnectInterval = 20000;
            this.$socket.open(''.concat(this.$socket.wss_url, 'auction/'));
            this.$socket.onopen = this.socket_open;
            this.$socket.onclose = this.socket_close;
            this.$socket.onerror = this.socket_error;
            this.$socket.onmessage = this.socket_message;
        }
    },
}
</script>
<style lang="scss" scoped>
@include page;
@include form;

ul{
    display: block;
    margin-block-start: 0em;
    margin-block-end: 0em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    padding-inline-start: 0px;
}
.page{
    height: 100vh;

    .column{
        display: block;
        // flex-basis: 0;
        // flex-grow: 1;
        // flex-shrink: 1;
        // flex-direction: column;
    }

    .column-page{
        border-radius: 15px;
        padding: 20px 20px;
        align-items: normal;
        max-height: 80vh;
    }

    &__head {
        .unread-link {
            font-size: 1em;
            font-weight: 500;
            color: $color-blue-main;
            transform: rotate(0.02deg);
            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em #FEFEFE;
                transform: translateY(-0.25em);
            }
        }
        &--title {
            font-size: 25px;
            color: $color-lightblue-text;
            font-weight: 600;

            .title__active {
                color: $color-green-light;
            }

            @media screen and (max-width: 1600px) {
                font-size: $font-size-normal;
            }
        }
    }

    .column-details {
        margin: 0 $line-height/4;
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: 15px;
        padding: 0;
        background-color: red;
        width: 71%;
        justify-content: center;


        &__head {
            background: $color-baby-blue;
            padding: $line-height/2 $line-height;
            border-radius: 15px;
            margin: $line-height/4 0;
            display: flex;
            flex-flow: row nowrap;
            align-items: flex-end;
            .header_item{
                display: inline-block;
                flex-grow: 1;
            }
            .header_item2{
                display: inline-block;
                flex-grow: 0;
                // width: 100px;
                margin: 0 1.6em;
                padding: 0 0.5em;
            }

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
            margin-bottom: $line-height*20;

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

                &__button-detail {

                    width: 200px;
                    color: $color-blue-main;
                    font-size: $font-size-text;
                    background-color: $color-white-main;
                    border: 1px solid $color-blue-main;
                    border-radius: 5px;
                    transform: rotate(0.02deg);

                    &__button-text{
                        display: inline;
                        margin-right: 1em;
                    }

                    &:hover, :focus {
                        box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                        transform: translateY(-0.25em);
                    }
                }
            }
        }

        &__content_documents{
            padding: $line-height*2 0;
            margin-bottom: $line-height;
            display: block;
            text-align: center;


            .detail_button {
                padding: $line-height $line-height*2;

                .button-detail {
                    width: 300.51px;
                    color: $color-white-main;
                    background-color: $color-blue-main;
                    border: none;                
                    font-size: $font-size-text;
                    border-radius: 5px;
                    box-sizing: border-box;
                    transform: rotate(0.02deg);


                    &:hover, :focus {
                        box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                        transform: translateY(-0.25em);
                    }
                }
            }
        }
    }

    &__content2{

        .--scroll-box {
            height: 100vh;
            overflow-y: scroll;
            scrollbar-width: thin;
        }
        .auct_item{
            display: flex;
            justify-content: space-around;
            flex-flow: row nowrap;
            flex-wrap: nowrap;
            border-bottom: 2px solid #eeeeee;

            .as-1 {
                ///flex: 1px;
                display: flex;
                flex: 0 1 auto;
                margin: 0.5em;
                ////padding: $line-height/6 $line-height/3;
                //border: 1pt solid #EEEEEE;
                width: 100%;
                border-radius: $line-height/2;

                .product_image{
                    max-width: 37.5%;
                    min-width: 37.5%;
                    width: 37.5%;
                    padding:$line-height/6  $line-height/3;

                    img {
                        height: auto; /* maintain aspect ratio*/
                        width: 100%;
                        margin: 0px; /*optional centering of image*/
                        padding: 0px;

                    }
                }
                .product_description{
                    max-width: 62.5%;
                    min-width: 62.5%;
                    width: 62.5%;
                    padding: 0px;

                    .section{
                        border-bottom: 1px solid #eeeeee;
                        padding:0;
                        margin: 0 $line-height/12;
                        text-align: left;

                        p {
                            color: black;
                            font-size: $font-size-tiny;
                            line-height: $line-height;
                            margin-bottom: $line-height/12;

                        }

                        &--title{
                            color: rgba(18, 31, 62, 0.8);
                            font-size: $font-size-small;
                            font-weight: 700;
                        }
                        &--product-details{
                            padding-top: $line-height/12;
                            color: rgba(18, 31, 62, 0.8);
                            font-size: $font-size-small;
                            font-weight: 700;
                            width: 100%;
                            border-bottom: 1px solid #eeeeee;
                        }
                        .reserve_price , .best_bid, .bid_increment{
                            padding-top: $line-height/12;
                            font-weight: 600;
                        }
                        .reserve_price{
                            color:  black;
                            font-size: $font-size-small;
                        }
                        .bid_increment{
                            color:  black;
                            font-size: $font-size-small/1.2;
                        }
                        .best_bid{
                            color: $color-green-main;
                            font-size: $font-size-small;
                            background-color: rgba(13, 143, 65, 0.04);
                            box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.15);
                            width: 70%;
                            padding-left: $line-height/12;

                            &--good{
                               color: $color-green-main;
                            }
                            &--bad{
                                color: $color-red-main;
                            }
                        }
                        .additional_details{
                            padding: $line-height/4 0;
                            line-height: $line-height/1.5;
                            font-weight: 700;
                            .addit{
                                font-size: $font-size-tiny;
                                color: #344767;
                                .desc{
                                    font-weight: 600px;
                                }
                            }
                        }
                    }
                }
                
                .bid-box{
                    width: 100%;
                }
                .place_bid{
                    display: grid;
                    grid-template-columns: auto auto;
                    grid-gap: 0.5px;
                    height: 20vh;
                    padding: $line-height/10 $line-height/1.5;
                    margin-bottom: $line-height;
                    color: black;
                    border: 1pt solid #EEEEEE;
                    border-radius: $line-height/2;
                    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
                    .bid_details{
                        display: grid;
                        grid-column: 1/3;
                        grid-template-columns: auto auto auto;
                        grid-gap: 2.5px;
                    }
                    .proceed{
                        //text-align: center;

                        form{
                            input[type="number"]{
                                width: 80%; 
                                height: 4.5vh;
                                padding: $line-height/10 $line-height/1.5;
                                color: black;
                            }
                        }
                        .tt{
                            color: rgba(18, 31, 62, 0.8);
                            border-bottom: 0.5px solid rgba(0, 0, 0, 0.4);
                            font-weight: 600;
                            margin: 0.5em;
                            padding: 0.5em;

                            &--money{
                                font-style:italic;
                            }
                        }
                        .bid{
                            width: 8em;
                            height: 2em;
                            color: $color-white-main;
                            background-color: $color-blue-main;               
                            font-size: $font-size-text;
                            border-radius: $line-height/2;
                            box-sizing: border-box;
                            transform: rotate(0.02deg);
                            margin-top: 0.3em;

                            &__bid-text{
                                display: inline;
                            }

                            &:hover, :focus {
                                box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                                transform: translateY(-0.15em);
                                color: $color-white-main;
                            }
                        }
                    }
                    &:hover, :focus {
                        box-shadow: 0 1em 1em -0.4em rgba(227, 6, 6, 0.05);
                        transform: translateX(-0.15em);
                        color: $color-white-main;
                    }
                }
                .dates{
                    width: 100%;
                    height: 8.0vh;
                    background-color: $color-baby-blue;
                    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.25);
                    //transform: translateY(-0.15em);
                    border-radius: $line-height/2;
                    padding: $line-height/10 $line-height/1.5 0;
                    margin: $line-height/10 0 0;
                    white-space: pre-line;
                    overflow: auto;
                    text-overflow: ellipsis;

                    &__info {
                        margin:auto;

                        &--title {
                            font-weight: 700;
                            font-size: $font-size-small;
                            color: #344767;
                            
                            @media screen and (min-width: 1600px) {
                                font-size: $font-size-normal;
                            }
                            @media screen and (max-width: 1300px){
                                font-size: $font-size-tiny;
                                word-wrap: break-word;
                            }
                            .fa-fw{
                                text-align: center;
                                padding-right: 5px;
                            }
                        }

                        &--desc {
                            color: #344767;
                            font-weight: 500;
                            font-size: $font-size-tiny;
                            width: auto;
                            display: inline;          


                            @media screen and (min-width: 1600px) {
                                font-size: $font-size-small;
                            }
                            @media screen and (max-width: 1300px){
                                font-size: ($font-size-tiny - 2);
                                word-wrap: break-word;
                            }
                        }
                    }
                    
                    &:hover, :focus {
                        box-shadow: 0 1em 1em -0.4em rgba(227, 6, 6, 0.05);
                        transform: translateX(-0.15em);
                        color: $color-white-main;
                    }
                }
            }
            .as-1-width{
                width: 62%;
            }
            .as-2-width{
                width: 33%;
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
                            height: $line-height/4;
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
        }
        .notification-card{
            display: block;
            padding: 25px, 12px;
            color: #333333;
            background-color: $color-white-main;
            text-decoration: none;
            .media{
                align-items: flex-start;
                display: flex;
                flex-direction: row;
                flex-wrap: nowrap;
                text-align: inherit;

                .media-body{
                    padding-top: 5.6px;
                    border-bottom: 1px solid #eeeeee;
                    .media-img{
                        float: left;
                        padding-right: 20px;
                    }

                    .media-text{
                        display: block;
                        float: right;
                        width:90%;
                    }
                    .paragraph_text{
                        color: $color-black-light;
                    }
                }
                .media-object img {
                    width: 64px;
                }
            }

            .notification-mark-read{
                display: inline;

                .notification-card-title{
                    color: black;
                    font-size: 15px;
                    font-weight: 600;
                }
            }
            .mark_as_read{
                float: right;
                color: #121F3ECC;

                &__mark_text{
                    font-size: 15px;
                    font-weight: 500;
                    text-align: justify;
                }

                &__delete{
                    color: $color-gray-main;
                    margin-left: 1em;

                    &:hover, :focus {
                        box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                        transform: translateY(-0.25em);
                    }
                }
            }

            .notification-meta {
                padding-top: 10px;
                padding-bottom: 10px;
                .timestamp{
                    color: $color-black-light;
                    display: inline;
                }
                .more{
                    font-size: 0.875em;
                    font-weight: 600;
                    position: absolute;
                    right:2ch;
                    color: $color-blue-main;
                    display: inline;
                }
            }
        }

    }
    .row-link{
        text-align: center;

        &__link{
            display: inline;
            margin-right: 0.5em;
            color: #4CAF50;
        }

        &__text{
            display: inline;
            color: $color-blue-main;
        }

        &__button-detail {
            width: 300.51px;
            color: $color-white-main;
            background-color: $color-blue-main;
            border: none;                
            font-size: $font-size-text;
            border-radius: 5px;
            box-sizing: border-box;
            transform: rotate(0.02deg);

            &__button-text{
                display: inline;
                margin-right: 1em;
            }

            &:hover, :focus {
                box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                transform: translateY(-0.25em);
            }
        }
    }
    .button-link{
        width: 300.51px;
        margin-right: $line-height;
        color: $color-white-main;
        background-color: $color-green-light;
        border: none;                
        font-size: $font-size-text;
        border-radius: 5px;
        box-sizing: border-box;
        transform: rotate(0.02deg);

        &__button-text{
            display: inline;
            margin-right: 1em;
        }

    }

    &__auction_header_details{
        width: 97%;
        -webkit-box-orient: vertical;
        display: flex;
        flex-direction: column; 
        box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05),
            4px 4px 10px rgba(0, 0, 0, 0.05);
        border-radius: 15px;
        padding: 0;
        margin: 0 $line-height/2;

        .auction-image-header-details{
            background-image: url('../../../../assets/Auction_Image.jpeg');
            height: 159px; 
            max-height: 159px;
            width: 190px;
            background-position: center;
            background-size:cover;
            background-repeat: no-repeat;
            margin-left: 0;
            border-radius: 15px;
        }

        .column-details {
            margin: 0 $line-height/4;
            box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.05), 4px 4px 10px rgba(0, 0, 0, 0.05);
            border-radius: $line-height/2;
            padding: 0;
            margin-bottom: $line-height/2;

            &__head {
                background: $color-baby-blue;
                padding: $line-height/2 $line-height;
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
                margin-bottom: $line-height/20;

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

                    &__button-detail {

                        width: 200px;
                        color: $color-blue-main;
                        font-size: $font-size-text;
                        background-color: $color-white-main;
                        border: 1px solid $color-blue-main;
                        border-radius: 5px;
                        transform: rotate(0.02deg);

                        &__button-text{
                            display: inline;
                            margin-right: 1em;
                        }

                        &:hover, :focus {
                            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                            transform: translateY(-0.25em);
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
                    .ufile{
                        align-items: stretch;
                        margin:20px 0;
                        .ufile-label{
                            cursor: pointer;
                            overflow: hidden;
                            .ufile-input{
                                height: 100%;
                                width: 100%;
                            }

                        }
                    }
                }
            }
            &__content_documents{
                padding: $line-height*2 0;
                margin-bottom: $line-height;
                display: block;
                text-align: center;


                .detail_button {
                    padding: $line-height $line-height*2;

                    .button-detail {
                        width: 300.51px;
                        color: $color-white-main;
                        background-color: $color-blue-main;
                        border: none;                
                        font-size: $font-size-text;
                        border-radius: 5px;
                        box-sizing: border-box;
                        transform: rotate(0.02deg);


                        &:hover, :focus {
                            box-shadow: 0 0.5em 0.5em -0.4em rgba(0, 0, 0, 0.05);
                            transform: translateY(-0.25em);
                        }
                    }
                }
            }
        }

    }
}
</style>