<template>
    <div class="risk">
        // To do  add the css and page elements like on this page
        // https://www.bidspotter.com/en-us/auction-catalogues/stephint/catalogue-id-auctio6-10121#lot-37dd197f-2185-4ffa-8af3-af6700ee41cd    
    </div>
</template>
<script>
import auctions from '../../../../services/supplier/auction'
// import moment from 'moment'
// import Carousel from '../../../../components/auction/Carousel.vue'
import {mapGetters} from 'vuex'

const STATUS_INITIAL = 0, STATUS_SELECTED = 1;


export default {
  name: "bid-auction",
  data(){
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
  components:{
  },
  watch:{
  },
  filters:{
  },
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
  mounted(){
    this.web_socket_connect();
    this.getReverseAuction();
    this.get_responses();
  },
  methods:{
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

.page{
 width: auto;
 max-width: 1200px;
 float: none;
 display: block;
 margin-right: auto;
 margin-left: auto;

 &__head {
 }
}
</style>