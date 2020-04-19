import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";

import Dashboard from "@/pages/Dashboard.vue";
import Itemsets from "@/pages/FrequentItemsets.vue";


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
        path: "itemsets",
        name: "Frequent-Itemsets",
        component: Itemsets
      },
      {
        path: "rules",
        name: "Association Rules - Table",
        component: Dashboard
      },
      {
        path: "graph",
        name: "Association Rules - Network",
        component: Dashboard
      },      
    ]
  }
];

export default routes;
