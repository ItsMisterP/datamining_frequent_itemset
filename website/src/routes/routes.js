import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";

import Dashboard from "@/pages/Dashboard.vue";
import Itemsets from "@/pages/FrequentItemsets.vue";
import AssoTable from "@/pages/AssociationRulesTable.vue";
import Graph from "@/pages/NetworkGraph.vue";
import Parcoords from "@/pages/ParcoordsTable.vue";
import Information from "@/pages/Information.vue";

const routes = [
    {
        path: "/",
        component: DashboardLayout,
        redirect: "/dashboard",
        children: [
            {
                path: "dashboard",
                name: "Dashboard",
                component: Dashboard
            },
            {
                path: "graph",
                name: "Association Rules - Network",
                component: Graph
            },
            {
                path: "table",
                name: "Association Rules - Table",
                component: Parcoords
            },
            {
                path: "info",
                name: "Information",
                component: Information
            }
        ]
    }
];

export default routes;
