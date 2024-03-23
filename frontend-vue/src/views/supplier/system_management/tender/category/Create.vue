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
        <div class="column-details column is-12">
          <form v-on:submit.prevent="create()">
            <div class="column-details__head">
              <p class="column-details__head--title">Add Category</p>
              <p class="column-details__head--desc">Fill in the required details</p>
            </div>
            <!-- Form Details -->
            <div class="column-details__content">

              <div class="columns">
                <div class="column">
                  <div class="field">
                    <label class="label">Category Title <span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="text" v-model="form.name" required>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Category Code<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="text" v-model="form.unique_reference" required>
                    </div>
                  </div>
                  <div class="field">
                    <label class="label">Opening Date<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="datetime-local" v-model="form.opening_date" required>
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Closing Date<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="datetime-local" v-model="form.closing_date" required>
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Supporting Documents<span class="required"></span></label>
                    <div class="control">
                      <input class="input" multiple="multiple" type="file" @change="selectSupportingDocuments($event)">
                    </div>
                  </div>


                  <div class="field">
                    <div class="risk_submit">
                      <button type="submit" class="button button-submit">
                        Create
                      </button>
                    </div>
                  </div>

                </div>

                <div class="column">
                  <div class="field">
                    <label class="label">Bid Fee Currency<span class="required">*</span></label>
                    <div class="control">
                      <select v-model="form.currency" class="input" required>
                        <option selected>Select Currency</option>
                        <option v-for="currency in defaults.currencies" v-bind:key="currency.id" :value="currency.id">
                          {{ currency.name }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Bid Fee<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="number" v-model="form.bid_charge" required>
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Category Type<span class="required">*</span></label>
                    <div class="control">
                      <select v-model="form.category_type" class="input" required>
                        <option selected>Select Category Type</option>
                        <option v-for="category_type in defaults.category_types" v-bind:key="category_type.id" :value="category_type.id">
                          {{ category_type.name }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Pass Score<span class="required">*</span></label>
                    <div class="control">
                      <input class="input" type="number" v-model="form.pass_score" required>
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Question Template<span class="required"></span></label>
                    <a href="#" class="button button-submit is-small">Download Template</a>
                    <div class="control" style="margin-top:2%;">
                      <input class="input" type="file" @change="selectQuestionTemplate($event)">
                    </div>
                  </div>

                  <div class="columns">
                    <div class="column">
                      <div class="field">
                        <div class="control">
                          <label class="checkbox">
                            <input type="checkbox" v-model="form.send_participant_list_to_supplier">
                            <strong> Send Participant List To Suppliers </strong>
                          </label>
                        </div>
                      </div>
                    </div>

                    <div class="column">
                      <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="form.invite_only">
                        <strong> Invite Only ? </strong>
                      </label>
                    </div>
                  </div>
                    </div>

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
import tender from "@/services/company/tender";

export default {
  name: "Create",
  data() {
    return {
      defaults: [],
      form: {
        "name": "",
        "bid_charge": "",
        "unique_reference": "",
        "pass_score": "",
        "opening_date": "",
        "closing_date": "",
        "currency": "",
        "questions_template": "",
        "send_participant_list_to_supplier": "",
        "category_type": "",
        "invite_only": "",
        "tender": "",
        "supporting_documents": ""
      },
    }
  },
  methods: {
    async create() {
      let form_data = new FormData();
      if (this.form.questions_template) {
        form_data.append("questions_template", this.form.questions_template, this.form.questions_template.name)
      }
      if (this.form.current_suppliers) {
        form_data.append("supporting_documents", this.form.supporting_documents, this.form.supporting_documents.name)
      }

      form_data.append("name", this.form.name);
      form_data.append("unique_reference", this.form.unique_reference);
      form_data.append("opening_date", this.form.opening_date);
      form_data.append("closing_date", this.form.closing_date);
      form_data.append("send_participant_list_to_supplier", this.form.send_participant_list_to_supplier);
      form_data.append("bid_charge", this.form.bid_charge);
      form_data.append("currency", this.form.currency);
      form_data.append("category_type", this.form.category_type);
      form_data.append("pass_score", this.form.pass_score);
      form_data.append("invite_only", this.form.invite_only);
      form_data.append("tender", this.$route.params.id);

      try {
        let response = await tender.category_create(form_data, this.$route.params.id)
        window.toast.fire({icon: 'success', title: "Tender category created successfully"})
        this.$router.push(`/company/tender/category/details/${this.$route.params.id}/${response.data['id']}`)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
    selectSupportingDocuments(event) {
      this.form.supporting_documents = event.target.files
    },
    selectQuestionTemplate(event) {
      this.form.questions_template = event.target.files[0]
    },

    async get_defaults(){
      try {
        let response = await tender.defaults()
        this.defaults = response.data
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.get_defaults()
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