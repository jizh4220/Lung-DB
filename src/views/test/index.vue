<template>
  <div class="ztree">
    <el-tree
      :data="treeData"
      show-checkbox
      default-expand-all
      node-key="id"
      ref="tree"
      highlight-current
      :props="defaultProps"
      @check="checkHandler" 
      :render-content="renderContent"
    >
    </el-tree>
    <el-button type="primary" @click="createData()">确定</el-button>
  </div>
</template>
<script>
//调用删除接口
// import { deleteSubject} from "@/api/data/organ";

export default {
  data() {
    return {
      setTree: [],
      defaultProps: {
        children: "children",
        label: "description",
      },
      treeData: [],
      organList: [],
      questionForm: {
      },
    };
  },
 
  created() {
    //加载树节点
    this.getZtreeList();
  },
  methods: {
     renderContent(h, { node, data, store }) {
      console.log(data);
      return (
        <span
          class="custom-tree-node"
          on-mouseenter={() => (data.isHover = true)}
          on-mouseleave={() => (data.isHover = false)}
        >
          <span>{data.description}</span>
          {data.parentId !== 0 && data.isHover && (
            <i
              class="el-icon-error danger"
              on-click={(e) => {
                e.stopPropagation();

                this.remove(node, data);
              }}
            ></i>
          )}
        </span>
      );
    },
    remove(node, data) {
      this.$confirm("此操作将永久删除该条目, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.handleDelete(null, data);
          if (data.parentId === 0) {
            return;
          }
          const parent = node.parent;
          const children = parent.data.children || parent.data;
          const index = children.findIndex((d) => d.id === data.id);
          children.splice(index, 1);
          // 发请求删除
          this.$message({
            type: "success",
            message: "删除成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },

     //调用删除接口
    handleDelete(index, row) {
     //这里不多说了，根据自己的实际情况，填写删除接口
    },

    //树文件勾选事件
    checkHandler(...value) {
      let a = value[1].checkedNodes.map((a) => a.description);
      let b = value[1].checkedNodes.map((a) => a.permissionToken);
      console.log(a);
      this.questionForm.description = a;
      this.questionForm.permissionToken = b;
    },

    //获取树权限节点接口定义
    getZtreeList() {
      this.dataLoading = true;
      import("./mock").then((res) => {
        this.setTree = res.data;
        this.organList = res.data.map((a) => ({
          label: a.description,
          value: a.id,
        }));

        this.getListData();
        this.dataLoading = false;
      });
    },

    //对json的格式的转化
    getListData() {
      let dataArray = [];
      this.setTree.forEach(function (data) {
        let parentId = data.parentId;
        if (parentId === 0) {
          let objTemp = {
            id: data.id,
            description: data.description,
            permissionToken: data.permissionToken,
            parentId: parentId,
          };

          dataArray.push(objTemp);
        }
      });
      this.treeData = this.data2treeDG(this.setTree, dataArray);
    },
    data2treeDG(datas, dataArray) {
      for (let j = 0; j < dataArray.length; j++) {
        let dataArrayIndex = dataArray[j];
        let childrenArray = [];
        let Id = dataArrayIndex.id;
        for (let i = 0; i < datas.length; i++) {
          let data = datas[i];

          let parentId = data.parentId;
          if (parentId == Id) {
            //判断是否为儿子节点
            let objTemp = {
              id: data.id,
              description: data.description,
              permissionToken: data.permissionToken,
              parentId: parentId,
              isHover: false,
            };
            childrenArray.push(objTemp);
          }
        }
        dataArrayIndex.children = childrenArray;
        if (childrenArray.length > 0) {
          this.data2treeDG(datas, childrenArray);
        }
      }

      return dataArray;
    },

    //添加
    async createData() {
      const params = this.questionForm;
      alert(JSON.stringify(params));
    },
  },
};
</script>
<style lang="scss">
.danger {
  color: red;
}
</style>