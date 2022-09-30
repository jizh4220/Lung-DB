<div id="dropbox">
    <dropbox-viewer></dropbox-viewer>
</div>
<script id="dropbox-viewer-template" type="text/x-template">
<h1>Dropbox</h1>
</script>

<script>
export default {
  name: 'dropbox-viewer',
  template: '#dropbox-viewer-template',
  data() {
    return {
      accessToken: 'XXXX'
    }
  },
  methods: {
    dropbox() {
      return new Dropbox({
        accessToken: this.accessToken
      })
    },
    // cancel
    getFolderStructure(path) {
      this.dropbox().filesListFolder({path: path})
      .then(res => {
        console.log(res.entries)
        this.structure = res.entries
      })
      .catch(err => {
        console.log(err)
      })
    }
    // reset author info form
    resetAuthor() {
      this.form = {
        first_name: "",
        last_name: ""
      }
    },
    //save author info
    saveAuthor() {
      this.centerDialogVisible = false
      createAuthorInfo({
        first_name: this.form.first_name,
        last_name: this.form.last_name
      })
        .then(res => {
          if (res.code === "success") {
            this.$message.success("Add succeeded")
            this.getAuthorList()
          } else {
            this.$message.error("Add failed")
          }
        })
        .catch(err => {
          console.log(err)
          this.$message.error("ERROR IN ADD")
        })
    },
    editDialog(index, row) {
      this.dialogType = 'edit'
      this.centerDialogVisible = true
      this.title = "Edit Author information"
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
          if (res.code === "success") {
            this.$message.success("Update Succeeded")
            this.getAuthorList()
          } else {
            this.$message.error("Update Failed")
          }
        })
        .catch(err => {
          this.$message.error("ERROR IN UPDATE")
        })
    },
    handleDelete(index, row) {
      const authorID = row.id
      DeleteAuthorInfoById(authorID)
        .then(res => {
          if (res.code === "success") {
            this.$message.success("Delete Succeeded")
            this.getAuthorList();
          } else {
            this.$message.error("Delete Failed")
          }
        })
        .catch(err => {
          this.$message.error("ERROR IN DELETE")
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
    getAuthorList() {
      getAuthorInfo()
        .then(res => {
          if (res.code === "success") {
            this.tableData = res.authors
          } else {
            this.$message.error("Failed to retrieve author information")
          }
        })
        .catch(err => {
          this.$message.error("ERROR IN GET AUTHOR")
        })
    },
    mounted() {
      this.getAuthorList()
    }
  }
}
</script>

