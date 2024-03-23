//Denis will delete this file
//Kindly dont delete
//Some code here is useful

// import store from '../../store'

// const wsbaseURL = process.env.VUE_APP_WS_API_URL

// let reconnectInterval =  1000

// const auction_socket_service = {

//   Auctionconnect(){
//     let ws = new WebSocket(''.concat(wsbaseURL, 'auction/'))

//     ws.onopen = () => {
//       // Restart reconnect interval
//       reconnectInterval = 1000
//       handleOnAuctionConnect(1);
//     }

//     ws.onmessage = (event) => {
//       // New message from the backend - use JSON.parse(event.data)
//       console.log('Midnight oil')
//       console.log(event)
//     }
 
//     ws.onclose = (event) => {
//       if (event) {
//         // Event.code 1000 is our normal close event
//         if (event.code !== 1000) {
//           let maxReconnectInterval = 3000
//           setTimeout(() => {
//             if (reconnectInterval < maxReconnectInterval) {
//               // Reconnect interval can't be > x seconds
//               reconnectInterval += 1000
//             }
//             console.log(reconnectInterval);
//             this.Auctionconnect()
//           }, reconnectInterval)
//         }
//       }
//     }

//     ws.onerror = (error) => {
//       handleOnAuctionConnect(3);
//       console.log(error);
//       console.log('Denis')
//       // console.log('log'+process.env.VUE_APP_WS_API_URL)
//       ws.close()
//     }

//     return ws
//   },

//   AuctionDisconnect(ws){
//     // Our custom disconnect event
//     handleOnAuctionConnect(2);
//     ws.close()
//   },

//   AuctionSend(ws, data){
//     // Send data to the backend - use JSON.stringify(data)
//     console.log('On Send')
//     ws.send(JSON.stringify(data))

//     ws.onmessage=(event) => {
//       const data = JSON.parse(event.data)
//       console.log(''.concat('data: ', data))
//     }
//   }
//   /*
//     Here we write our custom functions to not make a mess in one function
//   */
//     // function handleNotification (params) {
//     //   console.log(params)
//     //   options.store.dispatch('notifications/setNotifications', params.data)
//     // }
// }

// function handleOnAuctionConnect(int) {
//   console.log('Ocean Eyes !')
//   store.dispatch('Auction/connect_socket', int)
// }

// export default auction_socket_service