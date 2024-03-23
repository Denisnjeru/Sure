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
          <form v-on:submit.prevent="create()">
            <div class="column-details__head">
              <p class="column-details__head--title">Edit Section</p>
              <p class="column-details__head--desc">Fill in the required details</p>
            </div>
            <!-- Form Details -->
            <div class="column-details__content">
              <div class="field">
                <label class="label">Section Name<span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.name" required>
                </div>
              </div>

              <div class="field">
                <label class="label">Section Translation Name<span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.trans_name" required>
                </div>
              </div>

              <div class="field">
                <label class="label">Section Short Name<span class="required">*</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.short_name" required>
                </div>
              </div>

              <div class="field">
                <label class="label">Section Description<span class="required">*</span></label>
                <div class="control">
                  <textarea class="input" v-model="form.description" required></textarea>
                </div>
              </div>

              <div class="field">
                <label class="label">Parent Section<span class="required">*</span></label>
                <div class="control">
                  <select v-model="form.parent_section" class="input" >
                    <option selected>Select Section</option>
                    <option v-for="section in sections" v-bind:key="section.id" :value="section.id">
                      {{ section.name }}
                    </option>
                  </select>
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
import tender from "@/services/company/tender";

export default {
  name: "CreateSection",
  data(){
    return{
      form: {
        "name": "",
        "trans_name": "",
        "short_name": "",
        "description": "",
        "parent_section": "",
        "category": this.$route.params.category_id
      },
      sections: [],
      section: {},
    }
  },
  methods: {
    async create(){
      try{
        await tender.update_section(this.$route.params.category_id, this.$route.params.section_id, this.form)
        window.toast.fire({icon: 'success', title: "Section updated successfully"})
        this.$router.push(`/company/tender/category/details/${this.$route.params.tender_id}/${this.$route.params.category_id}`)
      }catch (err){
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_defaults(){
      try {
        let response = await tender.section_defaults(this.$route.params.category_id)
        this.sections = response.data['results']
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    async get_section(){
      try {
        let response = await tender.section(this.$route.params.category_id, this.$route.params.section_id)
        this.section = response.data
        this.form.name = response.data['name']
        this.form.trans_name = response.data['trans_name']
        this.form.short_name = response.data['short_name']
        this.form.description = response.data['description']
        this.form.parent_section = response.data['parent_section']
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    }
  },
  mounted() {
    this.get_defaults()
    this.get_section()
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