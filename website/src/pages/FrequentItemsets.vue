<template>
    <div>
        <div class="md-layout">
            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Frequent-Itemsets</h4>
                        <p class="category">
                            Tabelle mit den Frequent-Itemsets
                        </p>
                    </md-card-header>
                    <md-card-content>
                        
                        <div class="md-layout">
                            <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
                                <md-field>
                                    <label>Number of entries</label>
                                    <md-input @input="searchOnTable" v-model="filter.numberOfEntries"  type="number"></md-input>
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
                                    <label>number of items</label>
                                    <md-input @input="searchOnTable" v-model="filter.numberOfItems" type="number"></md-input>
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
                                    <h1 class="md-title">Frequent Itemsets</h1>
                                </div>

                                <md-field
                                    md-clearable
                                    class="md-toolbar-section-end"
                                >
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

                            <md-table-row
                                slot="md-table-row"
                                slot-scope="{ item }"
                            >
                                <md-table-cell
                                    md-label="Support"
                                    md-sort-by="support"
                                    md-numeric
                                >
                                    {{ item.support }}
                                </md-table-cell>
                                <md-table-cell
                                    md-label="Itemset"
                                    md-sort-by="itemsets"
                                    
                                >
                                    {{ item.itemsets }}
                                </md-table-cell>
                            </md-table-row>
                        </md-table>
                    </md-card-content>
                </md-card>

                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Items</h4>
                        <p class="category">
                            Tabelle mit den vorkommenden Items
                        </p>
                    </md-card-header>
                    <md-card-content>
                        <md-table
                            v-model="searchedItems"
                            md-sort="id"
                            md-sort-order="desc"
                            md-card
                            md-fixed-header
                        >
                            <md-table-toolbar>
                                <div class="md-toolbar-section-start">
                                    <h1 class="md-title">Items</h1>
                                </div>

                                <md-field
                                    md-clearable
                                    class="md-toolbar-section-end"
                                >
                                    <md-input
                                        placeholder="Search by Item..."
                                        v-model="searchItems"
                                        @input="searchOnItemTable"
                                    />
                                </md-field>
                            </md-table-toolbar>

                            <md-table-empty-state
                                md-label="No Itemsets found"
                                :md-description="
                                    `No Itemsets found for this '${searchItems}' query. Try a different search term.`
                                "
                            >
                            </md-table-empty-state>

                            <md-table-row
                                slot="md-table-row"
                                slot-scope="{ item }"
                            >
                                <md-table-cell
                                    md-label="Item"
                                    md-sort-by="id"
                                >
                                    {{ item.id }}
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

const toLower = text => {
    return text.toString().toLowerCase();
};

const searchByName = (items, term, filter) => {
        return items
            .filter(item => {
              return toLower(item.itemsets).includes(toLower(term)) 
                            && parseFloat(item.support) >= filter.minsup
                            && item.itemsets.length >= filter.numberOfItems;
            })
            .slice(0, filter.numberOfEntries);
    

    
};

export default {
    props: {
        id: String
    },
    data: () => ({
        search: " ",
        searched: [],
        itemsets: [],
        searchItems: " ",
        searchedItems: [],
        items: [],
        data: null,
        fileinput: Object,
        filter: {
            numberOfEntries: 500,
            numberOfItems: 2,
            minsup: 0.001,
        }
    }),
    created() {},
    mounted() {
        this.init();
    },
    methods: {
        init() {
            
            this.items = require("../assets/json/UniqueValuesGESAMT.json");
            this.itemsets = require("../assets/json/frequent_itemsets.json");
            console.log(this.items);
            this.searched = this.searchOnTable();
            this.searchedItems = this.searchOnItemTable();
        },
        searchOnTable() {
            this.searched = searchByName(this.itemsets, this.search, this.filter);
        },
        searchOnItemTable(){
            this.searchedItems = this.searchByItemName(this.items, this.searchItems);
        },
        searchByItemName(items, term){
            if (term) {
                return items
                    .filter(item => toLower(item.id).includes(toLower(term)));
            }

            return items;
        }
    }
};
</script>
<style scoped></style>
