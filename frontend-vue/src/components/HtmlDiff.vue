<template>
    <div class="htmldiff">
        <span @click="checkHtmlDiff()">View</span>
        <editor 
            api-key='ilebf08k7e8o2y9rvuxb1tngrsz9ag0emag1yeqbb0oit0uu'
            :init="config" 
            v-model="diffContent"
        />
        <div id="output">

        </div>
    </div>
</template>

<script>
import htmldiff from '@/htmldiff';

export default {
    props: ['current', 'old'],
    data() {
        return {
            diffContent: '',
            content_css: '@/styles/components/tinymce.css',
            config: {
                height: 400,
                content_css: '../../styles/components/tinymce.css',
                content_style: "ins { background-color: d4fcbc; } del { background-color: #fbb6c2; }",
                plugins: [
                    'hr pagebreak emoticons advlist autolink lists link image charmap print preview anchor',
                    'searchreplace visualblocks code fullscreen directionality',
                    'insertdatetime media table paste code help wordcount autosave save',
                ],
                toolbar:
                    'restoredraft pagebreak undo redo save | hr | blocks fontfamily fontsize | formatselect | bold italic forecolor backcolor strikethrough | \
                    alignleft aligncenter alignright alignjustify | \
                    bullist numlist outdent indent | removeformat | help | ltr rtl',
                setup: function () {
                    // window.tinymce.activeEditor.mode.set("readonly");
                }
            }
        }
    },
    mounted() {
        this.checkHtmlDiff()
    },
    methods: {
        checkHtmlDiff: function() {
            if (this.current && this.old) {
                // let originalHTML = `
                //     <p>Hello Mr. Wayne, decide what to do:</p>
                //     <ul>
                //         <li>Call Alfred</li>
                //         <li>Take Thalia Al Gul to the cinema</li>
                //         <li>Save Gotham</li>
                //     </ul>
                //     <span>Use the mouse to choose an option.</span>
                // `;

                // let newHTML = `
                //     <p>Hello Mrs. Batman, decide what to do:</p>
                //     <ul>
                //         <li>Kill The Joker</li>
                //         <li>Save Thalia Al Gul</li>
                //         <li>Save Gotham</li>
                //     </ul>
                //     <span>Use the matarang to choose an option.</span>
                // `;

                // Diff HTML strings
                let output = htmldiff(this.current, this.old);
                this.diffContent = output


                // Show HTML diff output as HTML (crazy right?)!
                // document.getElementById("output").innerHTML = output;
            }
        }          
    }
}
</script>

<style lang="scss">
ins {
    text-decoration: none;
    background-color: #d4fcbc;
}

del {
    text-decoration: line-through;
    background-color: #fbb6c2;
    color: #555;
}
</style>
