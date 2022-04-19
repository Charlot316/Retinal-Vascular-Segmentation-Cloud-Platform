<template>
  <div>
    <div v-loading="loadingNewPicture">
      <el-row :gutter="50">
        <el-col :span="8">
          <single-photo :singleImage="singleImage" index="origin" />
          <div
            style="width:100%;margin:0 auto;text-align:center;height:100px;line-height:100px"
          >
            <el-button
              type="primary"
              icon="el-icon-arrow-left"
              circle
              :disabled="!(index>-1)"
              @click="index>-1?index--:index=-1"
            ></el-button>
          </div>
        </el-col>
        <el-col :span="8">
          <div v-if="index == -1">
            <single-photo
              v-if="
                singleImage.photo_upload && singleImage.photo_upload.length > 0
              "
              :singleImage="singleImage"
              index="upload"
            />
            <div v-else>
              <el-upload
                class="avatar-uploader"
                :action="'http://10.251.0.251:8000/upload/'"
                :data="{
                  photo_id: singleImage.photo_id,
                  id: $store.state.user_id,
                }"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="checkFile"
                :on-error="handleUploadError"
                list-type="false"
                name="pic_img"
              >
                <el-card :body-style="{ padding: '0px' }">
                  <el-image
                    lazy
                    style="width: 297px;height:297px;"
                    src="https://img0.baidu.com/it/u=101714381,3578597708&fm=253&fmt=auto&app=138&f=JPEG?w=667&h=500"
                    class="image"
                  >
                  </el-image>
                  <div style="padding: 14px">
                    <span>金标准</span>
                    <div class="bottom">
                      <el-button type="text" class="button">点击上传</el-button>
                    </div>
                  </div>
                </el-card>
              </el-upload>
            </div>
            <div
              style="width:100%;margin:0 auto;text-align:center;height:100px;line-height:100px"
            >
              自己上传的图像
            </div>
          </div>
          <div v-else>
            <upload-photo :uploadImage="singleImage.photo_upload_list[index]" />
            <div style="width:100%;margin:0 auto;">
              <user-icon style="margin-left:200px;" :user="singleImage.photo_upload_list[index].doctor" />
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <single-photo :singleImage="singleImage" index="promap" />
          <div
            style="width:100%;margin:0 auto;text-align:center;height:100px;line-height:100px"
          >
            <el-button
              type="primary"
              icon="el-icon-arrow-right"
              circle
              :disabled="!(index+1<singleImage.photo_upload_list.length)"
              @click="index+1<singleImage.photo_upload_list.length?index++:index=singleImage.photo_upload_list.length-1"
            ></el-button>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import SinglePhoto from "@/components/Public/SinglePhoto.vue";
import UploadPhoto from "./UploadPhoto.vue";
import UserIcon from "@/components/Public/Icon.vue";
export default {
  components: { SinglePhoto, UploadPhoto, UserIcon },
  props: ["image"],
  data() {
    return {
      singleImage: this.image,
      newName: "",
      loadingNewPicture: false,
      index: -1,
    };
  },
  created() {},
  methods: {
    getPhotoInfo() {
      this.$emit("getPhotoInfo");
    },
    handleUploadError() {
      this.loadingNewPicture = false;
      this.$message.error("上传失败");
    },
    checkFile(file) {
      this.loadingNewPicture = true;
      var fileExtension = file.name.substring(file.name.lastIndexOf(".") + 1);
      if (file.type.startsWith("image")) {
        if (fileExtension === "gif") {
          this.$message.error("不支持上传gif图片");
          this.loadingNewPicture = false;
          return false;
        }
      } else {
        this.$message.error("请上传图片");
        this.loadingNewPicture = false;
        return false;
      }
    },
    handleAvatarSuccess() {
      this.$message({
        message: "上传成功",
        type: "success",
      });
      this.loadingNewPicture = true;
      setTimeout(() => {
        this.getPhotoInfo();
        this.loadingNewPicture = false;
      }, 2000);
    },
  },
};
</script>

<style>
.card-header {
  margin: 0 auto;
}
</style>
