<template>
  <div class="app-container">
    <div class="dashboard-container">
      <header>
        <div class="dashboard-text"> <center>Differential Expression Module:</center> {{ name }}</div>
      </header>
      <p class="card-title-desc"> This module aims to assist researchers to extensively investigate human lung transcriptomic data with cells or genes of interest on their expressional and pathological information. So far, researchers are able to perform
        <code class="highlighter-rouge">Differential Expression Genes (DEG) Heatmap</code>, <code class="highlighter-rouge">Differential Expression Genes (DEG) Violin Plot</code>,
        <code class="highlighter-rouge">Differential Expression Genes (DEG) Fraction Plot</code>, <code class="highlighter-rouge">GO Enrichment Analysis</code>, and <code class="highlighter-rouge">KEGG enrichment</code>.
        Researchers can choose to download the table or the plot image</p>

      <footer>
        <p>Download(how to get users faster download)</p>
      </footer>

      <p>Data Use Guidelines: </p>
      <!-- <div class="dashboard-age-description">
            Age Spans:
            Minimum Age: {{ age_range.min }} ~ Maximum Age: {{ age_range.max }},
          </div>
          <div class="dashboard-cellnum-description">
            Number of Cells in total:
            {{ cell_num_total }} cells
            Minimum Cell Num: {{ cell_num_range.min }} ~ Maximum Cell Num: {{ cell_num_range.max }},
          </div> -->
      <!-- <img style="width:180px" :src="img_list"></img> -->
    </div>
    <el-table
      :data="img_list"
      border
      fit
      responsive="sm"
      style="width: 100%"
    >
      <el-table-column label="Overall Distribution of Meta Data" align="center" width="1500" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <img style="width:1280px" :src="'data:image/png;base64,'+scope.row">
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getAccessionSummary, getAccessionPlot } from '@/api/accessiondata'
// import Pagination from '@/components/Pagination' // Secondary package based on el-pagination

export default {
  name: 'AccessionList',
  // components: { Pagination },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      total: 0,
      fontSize: 10,
      accession_counts: undefined,
      collection_counts: undefined,
      tissue_counts: undefined,
      disease_counts: undefined,
      age_range: undefined,
      cell_num_range: undefined,
      cell_num_total: undefined,
      gender_list: [
        { id: 'Male', count: 40 },
        { id: 'Femal', count: 60 },
        { id: 'NA', count: 200 }],
      img_list: []
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  created() {
    this.getAccessionInfo()
  },
  methods: {
    getAccessionInfo() {
      getAccessionSummary()
        .then(res => {
          if (res.code === 'success') {
            this.$message.success('Successfully retrieve accession info')
            this.accession_counts = res.accession_counts
            this.collection_counts = res.collection_counts
            this.tissue_counts = res.tissue_counts
            this.disease_counts = res.disease_counts
            // this.age_range = res.age_range
            // this.cell_num_range = res.cell_num_range
            this.cell_num_total = res.cell_num_total
            setTimeout(() => {
              this.listLoading = false
            }, 1.5 * 1000)
          } else {
            this.$message.error('Get Accession Meta Information Failed')
          }
        })
        .catch(err => {
          console.log(err)
          this.$message.error('Get Accession Meta Information Failed')
        })
      getAccessionPlot()
        .then(res => {
          if (res.code === 'success') {
            this.$message.success('Successfully retrieve MetaData Plots')
            this.img_list = res.img_list
            setTimeout(() => {
              this.listLoading = false
            }, 1.5 * 1000)
          } else {
            this.$message.error('Get MetaData Plots Failed')
          }
        })
        .catch(err => {
          console.log(err)
          this.$message.error('Get MetaData Plots Failed')
        })
    }
    /*
    UpdateCurrentSum() {
      getQuerySum(this.listQuery)
        .then(res => {
          if (res.code === 'success') {
            this.$message.success('Add succeeded')
            this.tableData = res.items
            // console.log(this.tableData)
            this.total_pages = res.total_pages
            this.total = this.listQuery.limit * this.total_pages
            // Just to simulate the time of the request
            setTimeout(() => {
              this.listLoading = false
            }, 1.5 * 1000)
          } else {
            this.$message.error('Get Accession Table FAILED')
          }
        })
        .catch(err => {
          console.log(err)
          this.$message.error('Get Accession Table FAILED')
        })
  }
  */
  }
}
</script>

<style scoped>
.edit-input {
  padding-right: 100px;
}
.cancel-btn {
  position: absolute;
  right: 15px;
  top: 10px;
}
</style>
<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    // margin: 150px;
    line-height: 46px;
  }
}
</style>
