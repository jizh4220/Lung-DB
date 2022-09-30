<template>
  <div class="app-container">
    <div class="dashboard-container">
      <header>
        <div class="dashboard-text"> <center>Single-cell RNA-seq Lung DB (SRLDB) hosted by Li Lab</center> {{ name }}</div>
      </header>
      <img class="Lung_respiratory_3D_model" src="@/assets/Lung_images/human-respiratory-system-lungs-3d-model-obj-3ds-fbx-c4d-stl-blend.jpeg" alt="lung_respiratory">
      <main>
        <h1>
          <div class="dashboard-text"> <center>Introduction and Summary of data stored in SRLDB</center> {{ name }}</div>
          <p> SRLDB is the first auto-updating, self-checking database which focuses on standardizing every data accession in SRLDB of the genome build, metadata categorization and description, and proper integration with minimal batch-effect across experiment.  the well-specifically designed to integrate, standardize, and investigate the circRNA transcriptome of human diseases.</p>
        </h1>
        <div :style="{ fontSize: fontSize }" class="dashboard-description">
          <div class="dashboard-cellnum-description">
            Total Cell Number in the DB:
            {{ cell_num_total }} 5072516
          </div>
          <div class="dashboard-accession-description">
            Number of Samples:
            {{ accession_counts }} samples
          </div>
          <div class="dashboard-collection-description">
            Number of Collections:
            {{ collection_counts }} collections
          </div>
          <div class="dashboard-disease-description">
            Number of Disease Types:
            {{ disease_counts }} disease types
          </div>
          <div class="dashboard-tissue-description">
            Number of Tissue Types:
            {{ tissue_counts }} tissue types
          </div>
          <div class="dashboard-tissue-description">
            Number of Gender Types:
            3 gender types
          </div>
          <!-- <div class="dashboard-age-description">
            Age Spans:
            Minimum Age: {{ age_range.min }} ~ Maximum Age: {{ age_range.max }},
          </div>
          <div class="dashboard-cellnum-description">
            Number of Cells in total:
            {{ cell_num_total }} cells
            Minimum Cell Num: {{ cell_num_range.min }} ~ Maximum Cell Num: {{ cell_num_range.max }},
          </div> -->
        </div>
      </main>
      <footer>
        <p>Here are some meta data distribution: </p>
      </footer>

      <footer>
        <p>Download(how to get users faster download)</p>
      </footer>

      Please
    </div>

    <div class="card-body" style="margin-bottom: -30px;">
      <h4 class="card-title">
        Biological Related Metadata Information
      </h4>
    </div>

    <div class="card DataUsageGuideline" style="height: 226.219px;">
      <div class="card-body">
        <h2 class="card-title-desc" style="font-size: medium; padding-top: 5px;">
          <p>Data Usage Guidelines: </p>
          "TO all users of Lung DB, please follow the data usage guidelines."
        </h2>
      </div>
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
