<template>
    <div class="columns myfooter is-multiline is-vcentered">
        <div class="column is-vcentered is-12 content copyright">
            <span>POWERED BY:</span>
            <img class="qed-logo" src="@/assets/qedlogo.png" alt="QED Solutions LTD.">
            <span>System requirements | © 2022. All rignts reserved</span>
        </div>
        <div class="column is-12 content">
            <p>
                WARNING: Do not proceed if you are not an Authorised User. This application is protected by appropriate security measures. Access to and use is restricted to Authorised Users only. Any attempt to use this system in a manner not authorised or any attempt to alter, destroy or damage any Information contained within it may constitute a breach of the provisions of the law and shall leave the user liable to both criminal and civil proceedings. It is strictly forbidden to attempt to access this system using any third party's logon identity. Anyone using this system consents to active monitoring for security policy compliance purposes.
            </p>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.myfooter {
    background-color: $color-blue-main;
    padding: $line-height 5%;
    font-size: $font-size-small;
    color: $color-white-main;
}

.copyright {
    margin-bottom: 0 !important;
    @include grid_row;
    justify-content: flex-start;
    flex-wrap: wrap;

    .qed-logo {
        height: $line-height*1.5;
        margin-right: $line-height/2;
    }
}

.content {
    font-size: $font-size-small;

    @media screen and (min-width: 1600px) { 
        font-size: $font-size-text;
    }
}

</style>

