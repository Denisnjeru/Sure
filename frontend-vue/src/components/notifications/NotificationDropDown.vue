<template>
  <li class="notification-card">
    <div class="media">
      <div class="media-left">
        <div class="media-object">
          <img src="@/assets/logo.png">
        </div>
      </div>

      <div class="media-body">
        <a href="#" class="notification-mark-read" title="Mark as read" @click.prevent="markAsRead">
          <i class="fa fa-times" aria-hidden="true" />
        </a>

        <span class="notification-card-title">{{ notification.verb }}</span>

        <blockquote class="blockquote text-right">
          <p>
            {{ notification.description }}
          </p>
        </blockquote>

        <div class="notification-meta">
          <small class="timestamp">
            <timeago :datetime="notification.timestamp" :auto-update="30" />
          </small>
          <span class="more">View More</span>
        </div>
      </div>
    </div>
  </li>
</template>

<script>
export default {
  props: {
    notification: {
      type: Object,
      required: true
    }
  },
  methods: {
    markAsRead () {
      this.$emit('read')
    }
  }
}
</script>
<style lang="scss" scoped>
@include page;

blockquote {
  font-size: 15px;
  margin-top: 10px;
  margin-bottom: 10px;
  // margin-left: 50px;
  font-weight: 400;
  padding-left: 7px;
  color: $color-black-light;
  border-left:2.5px solid #C4C4C4;
  // display:inline-flex;
} 

blockquote span {
  margin-top:-10px;
  margin-bottom:-10px;
}
.notification-card{
  display: block;
  padding: 9.6px 12px;
  border-bottom: 1px solid #eeeeee;
  color: #333333;
  background-color: $color-white-main;
  text-decoration: none;
}
  .notification-card .media-body {
    padding-top: 5.6px;
  }
  .notification-card .notification-card-title{
    color: black;
    font-size: 15px;
    font-weight: 600;
  }
  .dropdown-notifications {
    
    .dropdown-container {
      margin-top: 0px;
    }
  
    .notification-icon.hide-count:after {
      display: none;
    }
  
    .dropdown-toolbar .dropdown-toolbar-actions {
      margin-top: -2px;
      font-size: 13px;
    }
  
    .notification-mark-read {
      float: right;
      float: right;
      color: #333;
      opacity: 0.4;
  
      &:hover {
        opacity: .8;
      }
    }
  
    .notification-action {
      margin-top: 5px;
      margin-bottom: 2px;
    }
  
    .notification .media-body {
      padding-top: 0px;
    }
  
    .media-object img {
      width: 64px;
    }
    .notification-meta {
      .timestamp{
        color: $color-black-light;
        display: inline;
      }

      .more{
        font-size: 0.875em;
        font-weight: 600;
        // position: absolute;
        float: right;
        // margin-left: 2em;
        color: $color-blue-main;
        display: inline;
      }

    }
}
</style>