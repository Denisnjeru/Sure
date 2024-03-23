<template>
    <div class="tiny">
        <editor 
            api-key='ilebf08k7e8o2y9rvuxb1tngrsz9ag0emag1yeqbb0oit0uu'
            :init="config" 
        />
    </div>
</template>

<script>
import { customHr } from '@/plugins/myHr/plugin'

export default {
    data() {
        return {
            config: {
                height: 400,
                plugins: [
                    'hrcustom hr export pagebreak emoticons advlist autolink lists link image charmap print preview anchor',
                    'searchreplace visualblocks code fullscreen directionality',
                    'insertdatetime media table paste code help wordcount autosave save',
                ],
                toolbar:
                    'export restoredraft pagebreak undo redo save | hrcustom hr | blocks fontfamily fontsize | formatselect | bold italic forecolor backcolor strikethrough | \
                    alignleft aligncenter alignright alignjustify | \
                    bullist numlist outdent indent | removeformat | help | ltr rtl',
                setup: function () {
                    window.tinymce.PluginManager.add('hrcustom', customHr)
                }
            }
        }
    }
}
</script>