<template>
  <div class="risk-job-add">
    <div class="page__head">
            <span class="page__head--title">
                <span class="left nav-links__link">
                    <font-awesome-icon icon="chevron-left"/>  <span class="text">Back</span>
                </span>
            </span>
    </div>
    <div class="page__content">
      <div class="columns is-centered">
        <div class="column-details column is-4">
          <form v-on:submit.prevent="update()">
            <div class="column-details__head">
              <p class="column-details__head--title">Edit Job </p>
              <p class="column-details__head--desc">Fill in the required details</p>
            </div>
            <!-- Form Details -->
            <div class="column-details__content">
              <div class="field">
                <label class="label">Job Title <span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.title">
                </div>
              </div>
              <div class="field">
                <label class="label">Job Code<span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.unique_reference">
                </div>
              </div>
              <div class="risk_submit">
                <button type="submit" class="button button-submit">
                  Update
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import rfq from "@/services/company/rfq";

export default {
  name: "Edit",
  data(){
    return{
      form: {
        "title": "",
        "unique_reference": ""
      },
      rfq: {},
    }
  },
  methods: {
    async update(){
      let form_data = new FormData();
      form_data.append("title", this.form.title);
      form_data.append("unique_reference", this.form.unique_reference);
    
      try{
        let response = await rfq.update(this.$route.params.id,form_data)
        window.toast.fire({icon: 'success', title: "RFQ job updated successfully"})
        this.$router.push(`/company/rfq/details/${response.data['id']}`)
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_rfq(){
      try{
        let response = await rfq.rfq(this.$route.params.id)
        this.rfq = response.data
        this.form.title = response.data['title']
        this.form.unique_reference = response.data['unique_reference']
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.get_rfq()
  },
  created() {
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

        .risk_submit {
          padding: $line-height/2 0;
          margin: $line-height/1 0 50px;

          .button-submit {
            width: 100%;
            color: $color-white-main;
            background-color: $color-blue-main;
            border: none;
            font-size: $font-size-text;
          }

          &:hover {
            cursor: pointer;
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
    }

  }

}
</style>