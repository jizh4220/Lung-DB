<template>
  <div class="app-container">
    <!-- Add Author Info Button -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" icon="el-icon-plus" size="mini" @click="handleAdd">Add</el-button>
      </el-col>
    </el-row>
    <!--Author Info List -->
    <el-table v-loading="listLoading" :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="id" width="180" />
      <el-table-column prop="first_name" label="first_name" />
      <el-table-column prop="last_name" label="last_name" />
      <el-table-column label="handle" width="180" align="center">
        <template slot-scope="scope">
          <el-button size="mini" @click="editDialog(scope.$index, scope.row)">edit</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">delete</el-button>
        </template>
      </el-table-column>
      <el-table-column label="Readings" align="center" width="95">
        <template slot-scope="{row}">
          <span v-if="row.pageviews" class="link-type" @click="handleFetchPv(row.pageviews)">{{ row.pageviews }}</span>
          <span v-else>0</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getAuthorList" />

    <!--Add Author Info-->
    <el-dialog title="Add Author information" :visible.sync="centerDialogVisible" width="50%" center>
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="first_name">
          <el-input v-model="form.first_name" />
        </el-form-item>
        <el-form-item label="last_name">
          <el-input v-model="form.last_name" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancel">cancel</el-button>
        <el-button type="primary" @click="saveEdit">save</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {
  createAuthorInfo,
  getAuthorInfo,
  getAuthorTableList,
  UpdateAuthorInfoById,
  DeleteAuthorInfoById
} from '@/api/author'
import Pagination from '@/components/Pagination'

export default {
  name: 'Author',
  components: { Pagination },
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
      },
      list: null,
      total: 20,
      total_pages: 5,
      listLoading: false,
      showFirstPage: true,
      showLastPage: true,
      showPrevPage: true,
      showNextPage: true,
      listQuery: {
        page: 1,
        limit: 5,
        sort: '+id'
      }
    }
  },
  created() {
    this.getAuthorList()
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
    handleFilter() {
      this.listQuery.page = 1
      this.getAuthorList()
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
            this.getAuthorList()
          } else {
            this.$message.error('Delete Failed')
          }
        })
        .catch(err => {
          this.$message.error('ERROR IN DELETE')
        })
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
    getAuthorList() {
      this.listLoading = true
      getAuthorTableList(this.listQuery)
        .then(res => {
          if (res.code === 'success') {
            this.tableData = res.items
            this.total_pages = res.total_pages
            // console.log(this.total_pages)
            this.total = this.total_pages * this.listQuery.limit
            this.listLoading = false
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

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;
</style>

