<template>
  <div class="app-container">
        <el-form ref="nextProjectForm" :model="nextProjectForm" label-width="100px">
          <el-form-item label="insert">
            <el-upload
              class="avatar-uploader"
              :action="fileUpload"
              :before-upload="handleImagesUrlBefore"
              :headers="{ Authorization: token }"
              :show-file-list="false"
              :on-success="handleAvatarSuccess">
         
              <img
                v-if="nextProjectForm.publicWelfareUrl"
                :src="nextProjectForm.publicWelfareUrl"
                class="avatar"/>
              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
          </el-form-item>           
        </el-form>
  </div>
</template>
<script>
import { mapGetters } from "Vuex"
export default {
  data() {
    return {
      nextProjectForm: {
        publicWelfareUrl: "",
      },
    };
  },
  computed: {
    ...mapGetters(["fileUpload", "token"])
  },
  methods: {
    //对图片大小的限制
    handleImagesUrlBefore:function(file){
                var _this = this;
                return new Promise(function(resolve, reject) {
                    var reader = new FileReader();
                    reader.onload = function(event) {
                        var image = new Image();
                        image.onload = function () {
                            var width = this.width;
                            var height = this.height;
                            if (width>500 ){
                                _this.$alert('Width must be within 500', 'Notification', {confirmButtonText: 'Yes'});
                                reject();
                            }
                            if (height >300) {
                                _this.$alert('Height must be within 300', 'Notification', {confirmButtonText: 'Yes'});
                                reject();
                            }
                            resolve();
                        };
                        image.src = event.target.result;
                    }
                    reader.readAsDataURL(file);
                });
            },

    handleAvatarSuccess(response, file, fileList) {
      if (response && response.data && response.data.url) {
        this.$set(this.nextProjectForm, "publicWelfareUrl", response.data.url);
      }
    },
   
  }
};
</script>
<style lang='scss'>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>