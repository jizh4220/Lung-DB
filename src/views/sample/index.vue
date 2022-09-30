<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.params.accessionList"
        multiple
        :selectable="() => listQuery.params.accessionList.length < 5"
        clearable
        filterable
        allow-create
        reserve-keyword
        default-first-option
        placeholder="Accession Search"
        style="width: 200px;"
        class="filter-meta"
        @keyup.enter.native="handleFilter"
      />
      <el-select
        v-model="listQuery.params.diseaseType"
        multiple
        :selectable="() => listQuery.params.diseasetype.length < 5"
        clearable
        filterable
        allow-create
        reserve-keyword
        default-first-option
        placeholder="Disease Type"
        class="filter-meta"
        style="width: 150px"
      >
        <el-option v-for="item in diseaseTypeOptions" :key="item.key" :label="item.display_name+'('+item.key+')'" :value="item.key" />
      </el-select>
      <el-select
        v-model="listQuery.params.tissueType"
        multiple
        :selectable="() => listQuery.params.tissueType.length < 5"
        clearable
        filterable
        allow-create
        reserve-keyword
        default-first-option
        placeholder="Tissue Type"
        style="width: 150px"
        class="filter-meta"
      >
        <el-option v-for="item in tissueTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" style="width: 150px" />
      </el-select>
      <el-select
        v-model="listQuery.params.genderType"
        multiple
        :selectable="() => listQuery.params.genderType.length <= 3"
        clearable
        filterable
        allow-create
        reserve-keyword
        default-first-option
        placeholder="Gender Type"
        style="width: 130px"
        class="filter-meta"
      >
        <el-option v-for="item in genderTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
      </el-select>
      <el-select
        v-model="listQuery.params.collectionList"
        multiple
        :selectable="() => listQuery.params.collectionList.length < 5"
        clearable
        filterable
        remote
        :remote-method="selectBlur"
        allow-create
        reserve-keyword
        default-first-option
        placeholder="Collection Search"
        style="width: 200px;"
        class="filter-meta"
        @visible-change="handleVisible"
        @keyup.enter.native="handleFilter"
      >
        <el-option v-for="item in collectionOptions" :key="item.key" :label="item.display_name" :value="item.key" style="width: 150px" />
        <pagination v-show="total>0" :total="collectionTotal" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />
      </el-select>
      <!-- Age Range and Number of cells Input -->
      <el-form>
        <el-form-item label="Age range Min~Max" prop="age_range">
          <el-input v-model="listQuery.params.age_range.min" placeholder="Min Age" size="medium" style="width: 110px;" class="filter-meta" @keyup.enter.native="handleFilter" />
          ~
          <el-input v-model="listQuery.params.age_range.max" placeholder="Max Age" size="medium" style="width: 110px;" class="filter-meta" @keyup.enter.native="handleFilter" />
        </el-form-item>
        <el-form-item label="Cell num Min~Max" prop="cellnum_range">
          <el-input v-model="listQuery.params.cellnum_range.min" placeholder="Min CellNum" size="medium" style="width: 130px;" class="filter-cellnum-min" @keyup.enter.native="handleFilter" />
          ~
          <el-input v-model="listQuery.params.cellnum_range.max" placeholder="Max CellNum" size="medium" style="width: 130px;" class="filter-cellnum-max" @keyup.enter.native="handleFilter" />
        </el-form-item>
      </el-form>

      <!-- <el-select v-model="listQuery.sort" style="width: 130" class="filter-sort" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select> -->
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <!--
        <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        Export
      </el-button>
      -->
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleAnalyze">
        Analyze
      </el-button>
      <el-checkbox v-model="selectAll" :indeterminate="indeterminate" class="filter-item" style="margin-left:900px;" @change="handleSelectAll">
        select all
      </el-checkbox>
    </div>
    <!-- Key Table for Display and Select -->
    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :primary-key="tableData.accession"
      :data="tableData"
      border
      fit
      highlight-current-row
      selectable
      responsive="sm"
      style="width: 100%"
      @sort-change="sortChange"
      @selection-change="handleUserSelection"
    >
      <el-table-column label="Accession" prop="accession" sortable="custom" align="center" width="140" :class-name="getSortClass('id')" />
      <!--
      <template slot-scope="{row}">
          <span>{{ row.accession }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Date" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.timestamp | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Title" min-width="150px">
        <template slot-scope="{row}">
          <span class="link-type" @click="handleUpdate(row)">{{ row.title }}</span>
          <el-tag>{{ row.type | typeFilter }}</el-tag>
        </template>
      </el-table-column>
      -->
      <el-table-column label="Disease" prop="disease" width="250px" align="center" />
      <el-table-column label="Tissue" prop="tissue" width="250px" align="center" />
      <el-table-column label="Gender" prop="gender" width="180px" align="center" />
      <el-table-column label="Age" prop="age" width="180px" align="center" />
      <el-table-column label="Collection" prop="gse_alias" width="180px" align="center" />
      <el-table-column label="Number of Cell" prop="cellnum" sortable="custom" width="170px" align="center" :class-name="getSortClass('cellnum')" />

      <!-- User Actions-->
      <el-table-column label="Actions" align="center" width="300" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            Edit
          </el-button>
          <el-button v-if="row.status!='published'" size="mini" type="success" @click="handleModifyStatus(row,'published')">
            HG38
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleDelete(row,$index)">
            HG19
          </el-button>
        </template>
      </el-table-column>

      <!-- User Accession Selections-->
      <el-table-column label="Click to Select" align="center" width="120" :reserve-selection="true">
        <el-checkbox-group v-model="userSelect" slot-scope="{row}" label="checkbox">
          <el-checkbox
            v-for="item in row"
            :key="item"
            :label="item"
            :class="{unselected: item ? true:false}"
          >{{ item }}</el-checkbox>
        </el-checkbox-group>
        <template slot-scope="scope">
          <div style="margin-top: 20px">
            <el-checkbox v-model="selectedAccessions[scope.$index]" :indeterminate="indeterminate" border size="small" @change="handleUserSelection(scope)" />
            <!-- <el-checkbox v-model="userSelect" :indeterminate="indeterminate" label="备选项1" border size="medium" :value="row" />
            <el-checkbox-group v-model="checkboxGroup5" size="small">
              <el-checkbox :indeterminate="indeterminate" label="Select" border @change="handleUserSelection(row)" />
              @change="onPreviewClick($event, row.index, row.item)"
            </el-checkbox-group> -->
          </div>
          <!-- <el-checkbox
            v-model="row.item.check"
            border
            size="small"
          /> -->
        </template>
      </el-table-column>

    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <!-- Add/Update Form -->
    <!-- <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item label="Disease Type" prop="diseasetype">
          <el-select v-model="temp.diseasetype" class="filter-disease" placeholder="Please select">
            <el-option v-for="item in diseaseTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="Tissue Type" prop="tissuetype">
          <el-select v-model="temp.tissuetype" class="filter-tissue" placeholder="Please select">
            <el-option v-for="item in tissueTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>

        <el-form-item label="Gender Type" prop="gendertype">
          <el-select v-model="temp.gendertype" class="filter-gender" placeholder="Please select">
            <el-option v-for="item in genderTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="Age Range" prop="age_range">
          <el-select v-model="temp.age_range" class="filter-age" placeholder="Please select">
            <el-option v-for="item in age_range" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="Number of Cells Range" prop="cell_num_range">
          <el-select v-model="temp.cellnum_range" class="filter-cellnum" placeholder="Please select">
            <el-option v-for="item in cellnum_range" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="Date" prop="timestamp">
          <el-date-picker v-model="temp.timestamp" type="datetime" placeholder="Please pick a date" />
        </el-form-item>
        <el-form-item label="Title" prop="title">
          <el-input v-model="temp.title" />
        </el-form-item>
        <el-form-item label="Status">
          <el-select v-model="temp.status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="Tissue">
          <el-rate v-model="temp.importance" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" :max="3" style="margin-top:8px;" />
        </el-form-item>
        <el-form-item label="Remark">
          <el-input v-model="temp.remark" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          Confirm
        </el-button>
      </div>
    </el-dialog> -->

    <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel" />
        <el-table-column prop="pv" label="Pv" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getAccessionList, getCollectionList, analyzeAccessionQuery } from '@/api/accessiondata'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

const diseaseTypeOptions = [
  { key: 'COPD', display_name: 'COPD' },
  { key: 'IPF', display_name: 'IPF' },
  { key: 'LUAD', display_name: 'LUAD' },
  { key: 'NSCLC', display_name: 'NSCLC' },
  { key: 'Normal', display_name: 'Normal' }
]

const tissueTypeOptions = [
  { key: 'peripheral', display_name: 'Peripheral Lung' },
  { key: 'whole', display_name: 'Whole Lung' },
  { key: 'pleura', display_name: 'Pleura' },
  { key: 'upper', display_name: 'Upper Lung' },
  { key: 'lower', display_name: 'Lower Lung' }
]

const genderTypeOptions = [
  { key: 'F', display_name: 'Female' },
  { key: 'M', display_name: 'Male' },
  { key: 'NA', display_name: 'Unknown' }
]

// const ageRangeOptions = [
//   { key: 'min', display_name: 'Minimum: ', value: 1 },
//   { key: 'max', display_name: 'Maximum: ', value: 130 }
// ]

// const cellNumRangeOptions = [
//   { key: 'min', display_name: 'Minimum: ', value: 50 },
//   { key: 'max', display_name: 'Maximum: ', value: 1000000 }
// ]

// arr to obj, such as { CN : "China", US : "USA" }
const diseaseTypeKeyValue = diseaseTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})
// arr to obj, such as { CN : "China", US : "USA" }
const tissueTypeKeyValue = tissueTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})
const genderTypeKeyValue = genderTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})
// const ageRangeKeyValue = ageRangeOptions.reduce((acc, cur) => {
//   acc[cur.key] = cur.display_name
//   return acc
// }, {})
// const cellNumRangeKeyValue = cellNumRangeOptions.reduce((acc, cur) => {
//   acc[cur.key] = cur.display_name
//   return acc
// }, {})

export default {
  name: 'AccessionTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    diseasetypeFilter(type) {
      return diseaseTypeKeyValue[type]
    },
    tissuetypeFilter(type) {
      return tissueTypeKeyValue[type]
    },
    gendertypeFilter(type) {
      return genderTypeKeyValue[type]
    }
    // agerangeFilter(type) {
    //   return ageRangeKeyValue[type]
    // },
    // cellnumrangeFilter(type) {
    //   return cellNumRangeKeyValue[type]
    // }
  },
  props: {
    select: {
      type: [String, Array, Number],
      default: ''
    },
    filterKey: {
      type: String,
      default: ''
    },
    value: {
      type: [String, Array, Number],
      default: ''
    }
  },
  data() {
    return {
      tableData: [], // accession data table
      accessionTotal: 10000,
      collectionOptions: [],
      collectionTotal: 1000,
      cellnumThreshold: 50000,
      tableKey: 0,
      list: null,
      total: 20,
      total_pages: 5,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        params: {
          accessionList: [],
          tissueType: [],
          diseaseType: [],
          genderType: [],
          age_range: { min: undefined, max: undefined },
          cellnum_range: { min: undefined, max: undefined },
          collectionList: []
        },
        if_params: false,
        sort: '+id'
      },
      analyzeQuery: [],
      userSelect: [],
      selectAll: false,
      selectionChecked: false,
      selectedAccessions: [],
      indeterminate: false,
      tissueTypeOptions,
      genderTypeOptions,
      diseaseTypeOptions,
      // ageRangeOptions: [
      //   { key: 'min', display_name: 'Minimum: ', value: undefined },
      //   { key: 'max', display_name: 'Maximum: ', value: undefined }
      // ],
      // cellNumRangeOptions: [
      //   { key: 'min', display_name: 'Minimum: ', value: undefined },
      //   { key: 'max', display_name: 'Maximum: ', value: undefined }
      // ],
      // collectionOptions,
      sortOptions: [{ label: 'Ascending', key: '+id' }, { label: 'Descending', key: '-id' }],
      statusOptions: ['published', 'hg38', 'hg19'],
      // user selection of specific parameters
      temp: {
        id: undefined,
        accession: [],
        diseasetype: [],
        tissuetype: [],
        gendertype: [],
        collection: [],
        age_range: [1, 30],
        cellnum_range: [50, 100000],
        remark: '',
        timestamp: new Date(),
        title: '',
        type: '',
        status: 'published'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        type: [{ required: true, message: 'type is required', trigger: 'change' }],
        timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        title: [{ required: true, message: 'title is required', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getAccessionList(this.listQuery)
        .then(res => {
          if (res.code === 'success') {
            this.$message.success('Add succeeded')
            this.tableData = res.items
            // console.log(this.tableData)
            this.total_pages = res.total_pages
            this.total = this.listQuery.limit * this.total_pages
            // res.items.forEach(item => {
            //   this.collectionOptions.push({
            //     key: item[this.key],
            //     display_name: item[this.key]
            //   })
            // })
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
      this.getCheckList()
    },
    getCheckList() {
      for (let i = 0; i < this.listQuery.limit; i++) {
        this.selectedAccessions[i] = false
      }
    },
    // getDiseaseOptions(query = {}) {
    //   // TODO
    //   this.loading = true
    //   this.collectionOptions = []
    //   // const that = this
    //   const params = Object.assign({
    //     pageSize: 30,
    //     pageNum: 1
    //   }, query)
    //   // getDiseaseList(params)
    //   //   .then(res => {
    //   //     if (res.code === 'success') {
    //   //       this.$message.success('Add succeeded')
    //   //       this.tableData = res.items
    //   //       // console.log(this.tableData)
    //   //       this.total_pages = res.total_pages
    //   //       this.total = this.listQuery.limit * this.total_pages
    //   //       // Just to simulate the time of the request
    //   //       setTimeout(() => {
    //   //         this.listLoading = false
    //   //       }, 1.5 * 1000)
    //   //     } else {
    //   //       this.$message.error('Get Accession Table FAILED')
    //   //     }
    //   //   })
    //   //   .catch(err => {
    //   //     console.log(err)
    //   //     this.$message.error('Get Accession Table FAILED')
    //   //   })
    // },
    // getTissueOptions(query = {}) {
    //   // TODO
    //   this.loading = true
    //   this.collectionOptions = []
    //   // const that = this
    //   const params = Object.assign({
    //     pageSize: 30,
    //     pageNum: 1
    //   }, query)
    //   // getTissueList(params)
    //   //   .then(res => {
    //   //     if (res.code === 'success') {
    //   //       this.$message.success('Add succeeded')
    //   //       this.tableData = res.items
    //   //       // console.log(this.tableData)
    //   //       this.total_pages = res.total_pages
    //   //       this.total = this.listQuery.limit * this.total_pages
    //   //       // Just to simulate the time of the request
    //   //       setTimeout(() => {
    //   //         this.listLoading = false
    //   //       }, 1.5 * 1000)
    //   //     } else {
    //   //       this.$message.error('Get Accession Table FAILED')
    //   //     }
    //   //   })
    //   //   .catch(err => {
    //   //     console.log(err)
    //   //     this.$message.error('Get Accession Table FAILED')
    //   //   })
    // },
    // getGenderOptions(query = {}) {
    //   // TODO
    //   this.loading = true
    //   this.collectionOptions = []
    //   // const that = this
    //   const params = Object.assign({
    //     pageSize: 30,
    //     pageNum: 1
    //   }, query)
    //   // getGenderList(params)
    //   //   .then(res => {
    //   //     if (res.code === 'success') {
    //   //       this.$message.success('Add succeeded')
    //   //       this.tableData = res.items
    //   //       // console.log(this.tableData)
    //   //       this.total_pages = res.total_pages
    //   //       this.total = this.listQuery.limit * this.total_pages
    //   //       // Just to simulate the time of the request
    //   //       setTimeout(() => {
    //   //         this.listLoading = false
    //   //       }, 1.5 * 1000)
    //   //     } else {
    //   //       this.$message.error('Get Accession Table FAILED')
    //   //     }
    //   //   })
    //   //   .catch(err => {
    //   //     console.log(err)
    //   //     this.$message.error('Get Accession Table FAILED')
    //   //   })
    // },
    // getAgeRangeOptions(query = {}) {
    //   // TODO
    //   this.loading = true
    //   this.collectionOptions = []
    //   // const that = this
    //   const params = Object.assign({
    //     pageSize: 30,
    //     pageNum: 1
    //   }, query)
    //   // getAgeRangeList(params)
    //   //   .then(res => {
    //   //     if (res.code === 'success') {
    //   //       this.$message.success('Add succeeded')
    //   //       this.tableData = res.items
    //   //       // console.log(this.tableData)
    //   //       this.total_pages = res.total_pages
    //   //       this.total = this.listQuery.limit * this.total_pages
    //   //       // Just to simulate the time of the request
    //   //       setTimeout(() => {
    //   //         this.listLoading = false
    //   //       }, 1.5 * 1000)
    //   //     } else {
    //   //       this.$message.error('Get Accession Table FAILED')
    //   //     }
    //   //   })
    //   //   .catch(err => {
    //   //     console.log(err)
    //   //     this.$message.error('Get Accession Table FAILED')
    //   //   })
    // },
    // getCellNumOptions(query = {}) {
    //   // TODO
    //   this.loading = true
    //   this.collectionOptions = []
    //   // const that = this
    //   const params = Object.assign({
    //     pageSize: 30,
    //     pageNum: 1
    //   }, query)
    //   // getCellNumList(params)
    //   //   .then(res => {
    //   //     if (res.code === 'success') {
    //   //       this.$message.success('Add succeeded')
    //   //       this.tableData = res.items
    //   //       // console.log(this.tableData)
    //   //       this.total_pages = res.total_pages
    //   //       this.total = this.listQuery.limit * this.total_pages
    //   //       // Just to simulate the time of the request
    //   //       setTimeout(() => {
    //   //         this.listLoading = false
    //   //       }, 1.5 * 1000)
    //   //     } else {
    //   //       this.$message.error('Get Accession Table FAILED')
    //   //     }
    //   //   })
    //   //   .catch(err => {
    //   //     console.log(err)
    //   //     this.$message.error('Get Accession Table FAILED')
    //   //   })
    // },
    getCollectionOptions(query = {}) {
      // TODO
      this.loading = true
      this.collectionOptions = []
      // const that = this
      const params = Object.assign({
        pageSize: 30,
        pageNum: 1
      }, query)
      getCollectionList(params)
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
    },
    handleFilter() {
      this.listQuery.if_params = true
      // this.listQuery.page = 1
      this.getList()
    },
    handleAgeFilter() {
      console.log(this.listQuery.age_range)
      if (this.listQuery.age_range.min > 0 && this.listQuery.age_range.min < 120) {
        this.$message.success('Add succeeded')
      } else {
        this.$message.error('ILLEGAL INPUT AGE')
      }
    },
    handleCellNumFilter() {
      console.log(this.listQuery.cellnum_range)
      if (this.listQuery.cellnum_range.min > 0 && this.listQuery.cellnum_range.min < 120) {
        this.$message.success('Add succeeded')
      } else {
        this.$message.error('ILLEGAL INPUT AGE')
      }
    },
    // handleVisible(val) {
    //   // this.listLoading = true
    //   if (!val) {
    //     getCollectionOptions()
    //   }
    // },
    handleAddSelection(row, index) {
      if (this.selectionchecked === true) {
        console.log('Current row information is: ', row) // copy obj
        this.userSelect.push(row)
        console.log('Current User Selection Queue is: ', this.userSelect)
      }
    },
    handleUserSelection(scope) {
      console.log(this.selectedAccessions[scope.$index])
      if (this.selectedAccessions[scope.$index] === true) {
        console.log('Current row information is: ', scope.row) // copy obj
        this.userSelect.push(scope.row)
        console.log('Current User Selection Queue is: ', this.userSelect)
      }
      if (this.selectedAccessions[scope.$index] === false) {
        if (this.userSelect.indexOf(scope.row) !== -1) {
          this.userSelect.splice(this.userSelect.indexOf(scope.row), 1)
        }
      }
    },
    handleSelectAll() {
      console.log(this.selectAll)
      if (this.selectAll) {
        for (const i in this.tableData) {
          this.userSelect.push(this.tableData[i])
        }
      } else {
        for (const i in this.tableData) {
          this.userSelect.splice(this.userSelect.indexOf(i), 1)
        }
      }
      console.log(this.userSelect)
    },
    handleAnalyze() {
      // console.log(this.userSelect)
      let cur_sum = this.userSelect.cellnum
      for (const i in this.userSelect) {
        cur_sum = cur_sum + this.userSelect[i]
        if (cur_sum > this.cellnumThreshold) {
          this.$message({
            message: 'Selected Cell Num Exceeds Threshold',
            type: 'error'
          })
          break
        }
        this.analyzeQuery.push(this.userSelect[i].accession)
      }
      analyzeAccessionQuery(this.analyzeQuery)
        .then(res => {
          if (res.code === 'success') {
            this.$message.success('Submit Analyze Query Successfully')
            // this.tableData = res.items
            // // console.log(this.tableData)
            // this.total_pages = res.total_pages
            // this.total = this.listQuery.limit * this.total_pages
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
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: 'Successful Modification',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    selectBlur(value = '') {
      let params = {}
      const that = this
      if (value) {
        params = {
          queryConfig: [{
            name: that.filterKey,
            condition: 'like',
            value: value
          }]
        }
        this.getCollectionOptions(params)
      }
    },
    resetQuery() {
      this.listQuery = {
        page: 1,
        limit: 20,
        params: {
          accessionList: [],
          tissueType: [],
          diseaseType: [],
          genderType: [],
          age_range: { min: undefined, max: undefined },
          cellnum_range: { min: undefined, max: undefined },
          collectionList: []
        },
        if_params: false,
        sort: '+id'
      }
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        importance: 1,
        remark: '',
        timestamp: new Date(),
        title: '',
        status: 'published',
        type: ''
      }
    },
    /*
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          this.temp.author = 'vue-element-admin'
          createArticle(this.temp).then(() => {
            this.list.unshift(this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Created Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          updateArticle(tempData).then(() => {
            const index = this.list.findIndex(v => v.id === this.temp.id)
            this.list.splice(index, 1, this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row, index) {
      this.$notify({
        title: 'Success',
        message: 'Delete Successfully',
        type: 'success',
        duration: 2000
      })
      this.list.splice(index, 1)
    },
    handleFetchPv(pv) {
      fetchPv(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2CSV').then(excel => {
        const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
        const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    */
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    },
    mounted() {
      this.getList()
    }
  }
}
</script>

<!-- <style>
.y-checkbox {
    position: relative;
    margin-right: 30px;
}
.y-checkbox:last-child {
    margin-right: 0;
}
.y-checkbox__input {
    position: relative;
}
.y-checkbox__inner {
    display: inline-block;
    position: relative;
    width: 14px;
    height: 14px;
    border: 1px solid #dcdfe6;
    border-radius: 2px;
    box-sizing: border-box;
    vertical-align: middle;
}
.y-checkbox__inner::after {
    content: '';
    display: content-box;
    width: 3px;
    height: 7px;
    position: absolute;
    top: 2px;
    left: 4px;
    box-sizing: border-box;
    border: 1px solid #fff;
    border-top: 0;
    border-left: 0;
    transform: rotate(0deg) scale(0);
}
/* 选中样式 */
.y-checkbox__input.is-checked .y-checkbox__inner {
    background-color: #409eff;
    border-color: #409eff;
}
/* 选中后中间的对号,通过旋转45度得到 */
.y-checkbox__input.is-checked .y-checkbox__inner::after {
    transform: rotate(45deg) scale(1);
}
/* 半选中状态 */
.y-checkbox__input.is-indeterminate .y-checkbox__inner {
    background-color: #409eff;
    border-color: #409eff;
}
/* 半选中状态 中间的横杠 */
.y-checkbox__input.is-indeterminate .y-checkbox__inner::after {
    content: none;
}
.y-checkbox__input.is-indeterminate .y-checkbox__inner::before {
    content: '';
    display: inline-block;
    height: 2px;
    background-color: #fff;
    position: absolute;
    top: 5px;
    right: 0;
    left: 0;
    transform: scale(.5);
}
/* 隐藏原生多选框 */
.y-checkbox__original {
    opacity: 0;
    outline: none;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: -1;
    margin: 0;
}
.y-checkbox__label {
    font-size: 14px;
    display: inline-block;
    padding-left: 10px;
}
</style> -->
