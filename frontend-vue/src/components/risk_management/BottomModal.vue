<template>
    <div class="risk_modal">
        <div class="modal custom show" id="trackModal" tabindex="-1" role="dialog" aria-labelledby="trackModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-body">
                        <p>Test Modal</p>
                    </div>
                    <div class="modal-footer">
                        <div class="btnmodal" data-dismiss="modal">Close &#10006;</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "BottomModal",
    data() {
        return{

        }
    },
}
</script>
<style lang="scss" scoped>
.modal.custom .modal-dialog {
    width:20%;
    position:fixed;
    bottom:0;
    right:0;
    margin:0;
}

</style>