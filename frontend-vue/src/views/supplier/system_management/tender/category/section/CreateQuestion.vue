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
        <div class="column-details column is-5">
          <form v-on:submit.prevent="create()">
            <div class="column-details__head">
              <p class="column-details__head--title">Add Question</p>
              <p class="column-details__head--desc">Fill in the required details</p>
            </div>
            <!-- Form Details -->
            <div class="column-details__content">
              <div class="field">
                <label class="label">What is the question?<span class="required"> *</span></label>
                <div class="control">
                  <textarea class="input" type="text" v-model="form.description"></textarea>
                </div>
              </div>

              <div class="field">
                <label class="label">Question short description?<span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.trans_description">
                </div>
              </div>

              <div class="field">
                <label class="label">Type of response<span class="required"> *</span></label>
                <div class="control">
                  <select v-model="form.answer_type" class="input" @change="toggle_options">
                    <option selected>Select type of response</option>
                    <option value="1">Text</option>
                    <option value="2">Selection</option>
                    <option value="3">Checkbox</option>
                    <option value="4">True/False</option>
                    <option value="5">File Upload</option>
                    <option value="6">Number</option>
                    <option value="7">Date</option>
                  </select>
                </div>
              </div>

              <div class="field" id="max_score">
                <label class="label">Max score<span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="number" step="any" v-model="form.max_score">
                </div>
              </div>

              <div class="field" id="question_options">
                <label class="label">Set Options<span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.options" placeholder="1-10, 11-20">
                </div>
              </div>

              <div class="field" id="score_options">
                <label class="label">Set Scores<span class="required"> *</span></label>
                <div class="control">
                  <input class="input" type="text" v-model="form.score" placeholder="1, 5">
                </div>
              </div>

              <div class="columns">
                <div class="column">
                  <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="form.is_required">
                        <strong> Bidders must answer </strong>
                      </label>
                    </div>
                  </div>

                  <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="form.is_qa">
                        <strong> Goes through QA </strong>
                      </label>
                    </div>
                  </div>
                </div>

                <div class="column">
                  <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="form.is_dd">
                        <strong> Goes through DD </strong>
                      </label>
                    </div>
                  </div>

                  <div class="field">
                    <div class="control">
                      <label class="checkbox">
                        <input type="checkbox" v-model="form.is_scored" @change="toggle_max_score">
                        <strong> Response is scored </strong>
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              <div class="risk_submit">
                <button type="submit" class="button button-submit">
                  Save
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
  name: "CreateQuestion",
  data() {
    return {
      form: {
        "description": "",
        "trans_description": "",
        "section": this.$route.params.section_id,
        "answer_type": "",
        "is_required": "",
        "max_score": "",
        "is_scored": "",
        "is_qa": "",
        "is_dd": "",
        "options": "",
        "score": "",
      },
    }
  },
  methods: {
    toggle_max_score(){
      if(this.form.is_scored === true){
        document.getElementById('max_score').style.display = 'block'
      }else if(this.form.is_scored === false){
        document.getElementById('max_score').style.display = 'none'
      }else{
        document.getElementById('max_score').style.display = 'none'
      }
    },
    toggle_options(){
      if (parseInt(this.form.answer_type) === 2){
        document.getElementById('score_options').style.display = 'block'
        document.getElementById('question_options').style.display = 'block'
      }else{
        document.getElementById('score_options').style.display = 'none'
        document.getElementById('question_options').style.display = 'none'
      }
    },
    async create() {

      try {
        await tender.create_question(this.form, this.$route.params.section_id)
        window.toast.fire({icon: 'success', title: "Question created successfully"})
        this.$router.push(`/company/tender/section/questions/${this.$route.params.section_id}`)
      } catch (err) {
        window.toast.fire({icon: 'error', title: err})
      }
    },
  },
  mounted() {
    this.toggle_max_score()
    this.toggle_options()
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