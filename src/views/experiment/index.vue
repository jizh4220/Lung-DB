<template>
  <div class="app-container">
    <!-- Add Author Info Button -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" icon="el-icon-plus" size="mini" @click="handleAdd">Add</el-button>
      </el-col>
    </el-row>
    <!--Author Info List -->
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="id" width="180"></el-table-column>
      <el-table-column prop="first_name" label="first_name"></el-table-column>
      <el-table-column prop="last_name" label="last_name"></el-table-column>
      <el-table-column label="handle" width="180" align="center">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">edit</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">delete</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!--Add Author Info-->
    <el-dialog title="Add Author Info" :visible.sync="centerDialogVisible" width="50%" center>
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="first_name">
          <el-input v-model="form.first_name"></el-input>
        </el-form-item>
        <el-form-item label="last_name">
          <el-input v-model="form.last_name"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancel">cancel</el-button>
        <el-button type="primary" @click="save">save</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/user/list',
    method: 'get',
    params
  })
}
</script>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;
</style>
