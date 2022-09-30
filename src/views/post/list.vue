<template>
  <div class="app-container">
    <div>
      <el-button type="primary" class="add-button" size="normal" @click="openAddDialog">Add</el-button>
      <br><br>
    </div>
    <el-table
      v-loading="listLoading"
      :data="page.list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>
      <el-table-column label="postCode" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.postCode }}</span>
        </template>
      </el-table-column>
      <el-table-column label="postName" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.postName }}</span>
        </template>
      </el-table-column>
      <el-table-column label="postSort" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.postSort }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="created_time">
        <template slot-scope="scope">
          <span>{{ scope.row.createTime }}</span>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="modify" width="200">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="mini"
            @click="handleEdit(scope.row.postId)"
          >
            edit
          </el-button>
          <el-button
            type="danger"
            size="mini"
            @click="handleDelete(scope.row.postId)"
          >
            delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <br><br>
    <!-- Next Page -->
    <el-pagination
      class="pagination"
      :current-page="page.currentPage"
      :page-sizes="[10,20,50,100]"
      :page-size="page.pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="page.totalCount"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
    <!-- Add Dialog API -->
    <el-dialog title="Add" :visible.sync="addDialog">
      <el-form ref="form" :model="post" label-width="200px" size="normal">
        <el-form-item label="postCode">
          <el-input v-model="post.postCode" />
        </el-form-item>
        <el-form-item label="postName">
          <el-input v-model="post.postName" />
        </el-form-item>
        <el-form-item label="postSort">
          <el-input v-model="post.postSort" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="normal" @click="onSubmit">Submit</el-button>
          <el-button size="normal" @click="onCancel">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <!-- update Dialog API-->
    <el-dialog title="Update" :visible.sync="updateDialog">
      <el-form ref="form" :model="post" label-width="200px" size="normal">
        <el-form-item label="postCode">
          <el-input v-model="post.postCode" />
        </el-form-item>
        <el-form-item label="postName">
          <el-input v-model="post.postName" />
        </el-form-item>
        <el-form-item label="postSort">
          <el-input v-model="post.postSort" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="normal" @click="onSubmitUpdate">Submit</el-button>
          <el-button size="normal" @click="onCancel">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { save, delById, findPage, getById, updateById } from '@/api/post'

export default {
  components: {
    // eslint-disable-next-line vue/no-unused-components
  },
  data() {
    return {
      list: null,
      listLoading: true,
      // ADD Dialog API
      addDialog: false,
      //  UPDATE Dialog API
      updateDialog: false,
      post: {},
      page: {
        currentPage: 1, // current page
        pageSize: 10, // 10 posts per page
        totalPage: 0, // total pages
        totalCount: 0, // total post counts
        params: {}, // parameters
        list: [] // post list format
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      findPage(this.page).then(response => {
        this.page = response.page
        // console.log(response.data)
        this.listLoading = false
      })
    },
    handleEdit(id) {
      // modify
      getById(id).then(res => {
        // eslint-disable-next-line no-empty
        if (res.code !== 'success') {
          this.$message.success(res.error)
        }
        this.post = res.data
        this.updateDialog = true
      })
    },
    closeUpdateDialog() {
      // close UPDATE Dialog API
      this.updateDialog = false
    },
    openAddDialog() {
      // open UPDATE Dialog API
      this.addDialog = true
    },
    closeAddDialog() {
      // close ADD Dialog API
      this.addDialog = false
    },
    handleDelete(id) {
      // delete
      this.$confirm('If Delete?', 'Suggestion', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'error'
      }).then(() => {
        delById(id).then(res => {
          this.$message.success(res.message)
          this.fetchData()
        })
      })
    },
    //  change page size
    handleSizeChange(val) {
      this.page.pageSize = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.page.currentPage = val
      this.fetchData()
    },
    // call the entire API
    onSubmit() {
      save(this.post).then(res => {
        // console.log(res)
        if (res.code !== 'success') {
          this.$message.error(res.message)
          this.fetchData()
          this.addDialog = false
          this.post = {}
        } else {
          this.$message.success(res.message)
          this.fetchData()
          this.addDialog = false
          this.post = {}
        }
      })
    },
    onCancel() {
      this.addDialog = false
      this.updateDialog = false
    },
    onSubmitUpdate() {
      updateById(this.post).then(res => {
        this.$message.success(res.message)
        this.fetchData()
        this.updateDialog = false
      })
    }
  }
}
</script>

<style scoped>
.pagination-container {
  background: #fff;
  padding: 32px 16px;
}
.pagination-container.hidden {
  display: none;
}
</style>
