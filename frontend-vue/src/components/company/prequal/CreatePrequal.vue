<template>
  <div class="modal" id="create_prequal" >
  <div class="modal-background"></div>
<!--    style="width: 69%; margin-left: 23%;"-->
  <div class="modal-card" style="margin-left: 37%; background-color: #DBE9FE !important; border-radius: 12px">
    <header class="modal-card-head is-danger" style="background-color: #DBE9FE !important;">
      <p class="modal-card-title">Create Prequalification Job</p>
      <button class="delete" @click="closeModal" aria-label="close"></button>
    </header>
    <section class="modal-card-body" style="padding: 2%">
      <form>
        <div class="field">
          <label class="label">Job Title *</label>
          <div class="control">
            <input class="input" type="text" placeholder="Title">
          </div>
        </div>

        <div class="field">
          <label class="label">Job Code</label>
          <div class="control">
            <input class="input" type="text" placeholder="QED_2021">
          </div>
        </div>
        <br>
        <div class="field">
          <div class="control">
            <label class="checkbox">
              <input type="checkbox">
              Show supplier bids
            </label>
          </div>
        </div>
      </form>
    </section>

    <section class="modal-card-body">
      <button class="button is-fullwidth is-primary ">Submit</button>
    </section>
<!--    <footer class="modal-card-foot">-->
<!--      <button class="button is-success ">Submit</button>-->
<!--      <button class="button" @click="closeModal">Cancel</button>-->
<!--    </footer>-->
  </div>
</div>
</template>

<script>
export default {
  name: "CreatePrequal",
  methods: {
      closeModal() {
        document.getElementById('create_prequal').classList.remove('is-active');
      }
    },
}
</script>

<style lang="scss" scoped>
.page__content {
    margin: 0 !important;
    @include grid_column;
}
.is-primary{
  background-color: #073A82 !important;
}
</style>