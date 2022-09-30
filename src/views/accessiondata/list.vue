<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column label="AccessionID" width="140" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.AccessionID }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Tissue" width="140" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.Tissue }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Disease" width="140" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.Disease }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Gender" width="140" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.Gender }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Age" width="140" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.Age }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Number of cells" width="185" align="center">
        <template slot-scope="scope">
          {{ scope.row.num_cells }}
        </template>
      </el-table-column>
      <el-table-column label="Collection" width="140" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.Collection }}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Status" width="140" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getList } from '@/api/table'
import {
  createAccessionInfo,
  getAllAccessionInfo,
  getAccessionInfoById,
  UpdateAccessionInfoById,
  DeleteAccessionInfoById
} from '@/api/accessiondata'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      listLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getList().then(response => {
        this.list = response.data.items
        this.listLoading = false
      })
    }
  },
  data() {
    return {
      tableData: [], // author info table
      dialogType: 'new',
      title: 'Add Author information',
      centerDialogVisible: false, // if visible
      id: 0,
      form: { // author info form
        first_name: '',
        last_name: ''
      }
    }
  },
  methods: {
    // add 
    handleAdd() {
      this.dialogType = 'new'
      this.title = 'Add Author information'
      this.centerDialogVisible = true
    },
    // cancel
    cancel() {
      this.centerDialogVisible = false
      this.resetAuthor()
    },
    // reset author info form
    resetAuthor() {
      this.form = {
        first_name: '',
        last_name: ''
      }
    },
    // save author info
    saveAuthor() {
      this.centerDialogVisible = false
      createAuthorInfo({
        first_name: this.form.first_name,
        last_name: this.form.last_name
      })
        .then(res => {
          if (res.code === 'success') {
            this.$message.success('Add succeeded')
            this.getAuthorList()
          } else {
            this.$message.error('Add failed')
          }
        })
        .catch(err => {
          console.log(err)
          this.$message.error('ERROR IN ADD')
        })
    },
    editDialog(index, row) {
      this.dialogType = 'edit'
      this.centerDialogVisible = true
      this.title = 'Edit Author information'
      this.id = row.id
    },
    updateAuthor() {
      // const authorID = row.id
      UpdateAuthorInfoById({
        first_name: this.form.first_name,
        last_name: this.form.last_name,
        id: this.id
      })
        .then(res => {
          if (res.code === 'success') {
            this.$message.success('Update Succeeded')
            this.getAuthorList()
          } else {
            this.$message.error('Update Failed')
          }
        })
        .catch(err => {
          this.$message.error('ERROR IN UPDATE')
        })
    },
    handleDelete(index, row) {
      const authorID = row.id
      DeleteAuthorInfoById(authorID)
        .then(res => {
          if (res.code === 'success') {
            this.$message.success('Delete Succeeded')
            this.getAuthorList();
          } else {
            this.$message.error('Delete Failed')
          }
        })
        .catch(err => {
          this.$message.error('ERROR IN DELETE')
        });
    },
    saveEdit() {
      if (this.dialogType === 'edit') {
        this.updateAuthor()
      } else {
        this.saveAuthor()
      }
      this.centerDialogVisible = false
    },
    // get author information
    getAccessionList() {
      getAccessionInfo()
        .then(res => {
          if (res.code === 'success') {
            this.tableData = res.accessions
          } else {
            this.$message.error('Failed to retrieve author information')
          }
        })
        .catch(err => {
          this.$message.error('ERROR IN GET AUTHOR')
        })
    },
    mounted() {
      this.getAuthorList()
    }
  }
}
</script>
