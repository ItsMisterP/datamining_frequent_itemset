import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";

import Dashboard from "@/pages/Dashboard.vue";
import Itemsets from "@/pages/FrequentItemsets.vue";
import AssoTable from "@/pages/AssociationRulesTable.vue";


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
        component: AssoTable
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
