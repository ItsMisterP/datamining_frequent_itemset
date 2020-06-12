<template>
    <div class="wrapper" :class="{ 'nav-open': $sidebar.showSidebar }">
        <notifications></notifications>

        <side-bar
            :sidebar-item-color="sidebarBackground"
            :sidebar-background-image="sidebarBackgroundImage"
        >
            <mobile-menu slot="content"></mobile-menu>
            <sidebar-link to="/dashboard">
                <md-icon>dashboard</md-icon>
                <p>Dashboard</p>
            </sidebar-link>
            <sidebar-link to="/graph">
                <md-icon>track_changes</md-icon>
                <p>Association Rules - Network</p>
            </sidebar-link>
            <sidebar-link to="/table">
                <md-icon>content_paste</md-icon>
                <p>Association Rules - Table</p>
            </sidebar-link>
            <sidebar-link to="/info">
                <md-icon>info</md-icon>
                <p>Information</p>
            </sidebar-link>
        </side-bar>

        <div class="main-panel">
            <top-navbar></top-navbar>

            <dashboard-content> </dashboard-content>

            <content-footer v-if="!$route.meta.hideFooter"></content-footer>
        </div>
    </div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "@/pages/Layout/MobileMenu.vue";

export default {
    components: {
        TopNavbar,
        DashboardContent,
        ContentFooter,
        MobileMenu
    },
    data() {
        return {
            sidebarBackground: "green",
            sidebarBackgroundImage: require("@/assets/img/sidebar-2.jpg")
        };
    }
};
</script>
