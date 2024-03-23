<template>
  <div id="app" :class="{ fixHeight: isAuthenticated == true }">
    <div class="page columns">
      <div class="sidenav column is-one-fifth is-2-fullhd" v-if="isAuthenticated === true">
        <SideNav />
      </div>
      <div class="page__main column">
        <div class="columns is-multiline main" :class="{ loggedInContent: isAuthenticated == true }">
          <div class="topnav column is-12" v-if="isAuthenticated === true">
            <TopNav />
          </div>
          <div class="column is-12">
            <router-view/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const SideNav = () => import('@/components/SideNav')
const TopNav = () => import('@/components/TopNav')
import { mapGetters } from 'vuex'

export default {
  name: 'App',
  data() {
    return {
      login: true,
    }    
  },
  components: {
    SideNav,
    TopNav
  },
  computed: {
    ...mapGetters('Auth',['isAuthenticated']),
  },
  created() {
  }, 
}
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css?family=Roboto:400,900,700,500,300,100');
@import '~bulma';
@import '~@creativebulma/bulma-collapsible';

#app {
  font-family: Roboto;
  font-style: normal;
  line-height: 25px;
  background-color: $color-white-main;
  position: relative;

  .sidenav {
    background: #F9FBFF;
    height: 100vh;
    @include grid_column;
    overflow-y: scroll;
    overflow-x: hidden;
    @include scroll-bar;
    z-index: 100;
    position: relative;
  } 

  .topnav {
    width: 100%;
    padding: 0;
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .page__main {
    background-color: $color-white-main;
    overflow: hidden;
    padding: 0.75rem 0 !important;
    padding-bottom: 0;

    .main {
      width: 100%;
      margin: 0;
    }

    .loggedInContent {
      height: 100vh;
      @include grid_column;
      overflow-y: scroll;
      @include scroll-bar;
      justify-content: flex-start;
    }
  }

  .slick-dots {
    margin-left: $line-height*2 !important;
    margin-top: -10vh !important;
    text-align: left !important;
    position: relative !important;

    li {
      width: auto;
      margin: 0;
      
      button {
        width: 12px;
        height: 12px;
        // padding: 0;

        &:before { 
          width: 12px;
          height: 12px;
          color: $color-white-main !important;
        }
        // &:before {
        //   color: $color-white-main !important;
        //   height: 4px;
        //   width: 4px;
        //   line-height: 4px;
        //   background-color: $color-white-main;
        // }
      }
    }

    .slick-active {
      button {
        &:before { 
          // width: 24px;
          height: 6px;
          color: $color-white-main !important;
          border-radius: $line-height/4;
          // background-color: $color-white-main;
        }
        // &:before {      
        //   // width: 24px;
        //   // height: 6px;
        //   // border-radius: $line-height/4;
        //   color: $color-white-main !important;
        //   // background-color: $color-white-main !important;
        // }
      }
    }
  }
}

.fixHeight {
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

.vs__dropdown-toggle {
    border-radius: 12px !important;
    padding: 6px 12px !important;
}

.vs__dropdown-menu {
  margin-left: 0 !important;
}

.vs__search::placeholder {
  color: $color-gray-medium !important;
}

</style>
