<template>
    <div>
    <div class="md-layout">
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
      >
        <md-card>
          <md-card-header data-background-color="gray">
            <h4 class="title">Association Rules</h4>
            <p class="category">Tabelle mit den Frequent-Itemsets</p>
          </md-card-header>
          <md-card-content>

            <div class="md-layout">
                <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
                    <md-field>
                        <label>Number of entries</label>
                        <md-input @input="searchOnTable" v-model="filter.numberOfEntries" type="number"></md-input>
                    </md-field>
                </div>

                <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
                    <md-field>
                        <label>min-support</label>
                        <md-input @input="searchOnTable" v-model="filter.minsup" type="number"></md-input>
                    </md-field>
                </div>

                <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
                    <md-field>
                        <label>Number of antecedents elements</label>
                        <md-input @input="searchOnTable" v-model="filter.numberOfAntecedents" type="number"></md-input>
                    </md-field>
                </div>

                <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
                    <md-field>
                        <label>Number of consequents elements</label>
                        <md-input @input="searchOnTable" v-model="filter.numberOfCosequents" type="number"></md-input>
                    </md-field>
                </div>
                
                <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
                    <md-field>
                        <label>min-confidence</label>
                        <md-input @input="searchOnTable" v-model="filter.minconf" type="number"></md-input>
                    </md-field>
                </div>

                <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
                    <md-field>
                        <label>min-kluc</label>
                        <md-input @input="searchOnTable" v-model="filter.minkluc" type="number"></md-input>
                    </md-field>
                </div>

                <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
                    <md-field>
                        <label>min-imb_ratio</label>
                        <md-input @input="searchOnTable" v-model="filter.minimb" type="number"></md-input>
                    </md-field>
                </div>
            </div>
            

            <md-table
              v-model="searched"
              md-sort="support"
              md-sort-order="desc"
              md-card
              md-fixed-header
              
            >
              <md-table-toolbar>
                <div class="md-toolbar-section-start">
                  <h1 class="md-title">Association Rules</h1>
                </div>

                <md-field md-clearable class="md-toolbar-section-end">
                  <md-input
                    placeholder="Search by Item..."
                    v-model.lazy="filter.search"
                    @input="searchOnTable"
                  />
                </md-field>
              </md-table-toolbar>

              <md-table-empty-state
                md-label="No Rules found"
                :md-description="
                  `No Rule found for this '${filter.search}' query. Try a different search term.`
                "
              >
                
              </md-table-empty-state>

              <md-table-row slot="md-table-row" slot-scope="{ item }">
                <md-table-cell md-label="Support" md-sort-by="support" md-numeric>
                  {{ item.support }}
                </md-table-cell>
                <md-table-cell md-label="Antecedents" md-sort-by="antecedents">
                  {{item.antecedents}}
                </md-table-cell>
                <md-table-cell md-label="Consequents" md-sort-by="consequents">
                  {{item.consequents}}
                </md-table-cell>
                <md-table-cell md-label="Confidence" md-sort-by="confidence">
                  {{item.confidence}}
                </md-table-cell>
                <md-table-cell md-label="Kluc" md-sort-by="kluc">
                  {{item.kluc}}
                </md-table-cell>
                <md-table-cell md-label="Imbalance Ratio" md-sort-by="imbratio">
                  {{item.imbratio}}
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

const searchByName = (items, filter) => {
    items = items.filter((item) => { 
                return toLower(item.antecedents).includes(toLower(filter.search)) 
                        && parseFloat(item.support) >= filter.minsup
                        && parseFloat(item.confidence) >= filter.minconf
                        && parseFloat(item.kluc) >= filter.minkluc
                        && parseFloat(item.imbratio) >= filter.minimb 
                        && item.antecedents.length >= filter.numberOfAntecedents
                        && item.consequents.length >= filter.numberOfCosequents;
            }).slice(0,filter.numberOfEntries);
    console.log("filtered")
    return items;
};

export default {
    
    data: () => ({
    
    searched: [],
    assoRules: [
      
    ],
    data: null,
    fileinput: Object,
    filter: {
        numberOfEntries: 500,
        numberOfCosequents: 1,
        numberOfAntecedents: 2,
        minsup: 0.001,
        minconf: 0.6,
        minkluc: 0.5,
        minimb: 0.5,
        search: " ",
    }
  }),
  mounted() {
    this.init();
  },
  methods: {
    init(){
      this.assoRules = require('../assets/json/association_rules.json');
      this.searched = this.searchOnTable();
    },
    newUser() {
      window.alert("Noop");
    },
    searchOnTable() {
        console.log("filter changed")
        console.log(this.filter.minsup)
      this.searched = searchByName(this.assoRules, this.filter);
    },
  },
}
</script>

<style scoped>

</style>