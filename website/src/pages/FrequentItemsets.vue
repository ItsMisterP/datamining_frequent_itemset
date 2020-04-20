<template>
  <div>
    <div class="md-layout">
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
      >
        <md-card>
          <md-card-header data-background-color="gray">
            <h4 class="title">Frequent-Itemsets</h4>
            <p class="category">Tabelle mit den Frequent-Itemsets</p>
          </md-card-header>
          <md-card-content>
            <md-table
              v-model="searched"
              md-sort="support"
              md-sort-order="desc"
              md-card
              md-fixed-header
              
            >
              <md-table-toolbar>
                <div class="md-toolbar-section-start">
                  <h1 class="md-title">Frequent Itemsets</h1>
                </div>

                <md-field md-clearable class="md-toolbar-section-end">
                  <md-input
                    placeholder="Search by Item..."
                    v-model="search"
                    @input="searchOnTable"
                  />
                </md-field>
              </md-table-toolbar>

              <md-table-empty-state
                md-label="No Itemsets found"
                :md-description="
                  `No Itemsets found for this '${search}' query. Try a different search term.`
                "
              >
                
              </md-table-empty-state>

              <md-table-row slot="md-table-row" slot-scope="{ item }">
                <md-table-cell md-label="Support" md-sort-by="support" md-numeric>
                  {{ item.support }}
                </md-table-cell>
                <md-table-cell md-label="Itemset" md-sort-by="itemset">
                  {{item.itemsets}}
                </md-table-cell>
              </md-table-row>
            </md-table>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>
<script>
import * as d3 from "d3";

const toLower = (text) => {
  return text.toString().toLowerCase();
};

const searchByName = (items, term) => {
  if (term) {
    return items.filter((item) => toLower(item.itemsets).includes(toLower(term))).slice(0,500);
  }

  return items.slice(0,500);
};

export default {
  props: {
    id: String,
  },
  data: () => ({
    search: " ",
    searched: [],
    itemsets: [
      
    ],
    data: null,
    fileinput: Object,
  }),
  created() {
    
    
  },
  mounted() {
    this.init();
  },
  methods: {
    init(){
      this.itemsets = require('../assets/json/frequent_itemsets.json');
      this.searched = this.searchOnTable();
    },
    newUser() {
      window.alert("Noop");
    },
    searchOnTable() {
      this.searched = searchByName(this.itemsets, this.search);
    },
  },
};
</script>
<style scoped></style>
