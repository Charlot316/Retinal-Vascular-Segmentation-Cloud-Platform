<template>
    <div class="card-header">
      <div>
        <!-- 上传新图片的按钮 -->
        <el-tooltip
          class="item"
          effect="dark"
          content="上传新的眼底血管图片"
          placement="top"
        >
          <el-upload
            class="upload-demo inline-block"
            :action="props.baseURL + 'receive/'"
            :data="{ user_id: $store.state.user_id }"
            :on-success="handleAvatarSuccess"
            list-type="false"
            :show-file-list="false"
            :before-upload="checkFile"
            :on-error="handleUploadError"
            name="pic_img"
          >
            <el-button
              show-file-list="false"
              type="primary"
              icon="el-icon-upload"
              >上传</el-button
            >
          </el-upload>
        </el-tooltip>
        <!-- 下载全部图片的按钮 -->
        <el-tooltip
          class="item"
          effect="dark"
          content="下载本页所有图片"
          placement="top"
        >
          <el-button
            type="success"
            @click="downloadAllImage()"
            icon="el-icon-download"
            >下载</el-button
          >
        </el-tooltip>
        <!-- 清空全部图片的按钮 -->
        <el-tooltip
          class="item"
          effect="dark"
          content="清空本页所有图片"
          placement="top"
        >
          <el-button
            style="margin-left:30px"
            @click="deleteAllImage()"
            type="danger"
            icon="el-icon-delete"
            >清空</el-button
          >
        </el-tooltip>
      </div>
      <div>
        <!-- 搜索框 -->
        <el-input
          v-model="myProps.searchTitle"
          @keyup.enter="getImageList"
          placeholder="请输入图片名"
          clearable
          style="width:20vw"
        >
          <template #append>
            <el-button @click="getImageList" icon="el-icon-search"></el-button>
          </template>
        </el-input>
      </div>
    </div>
</template>

<script>
export default {
  props: ["props"],
  data() {
    return {
      myProps: this.props,
    };
  },
  methods: {
    getImageList() {
      this.$emit("getImageList");
    },
    handleUploadError(){
      this.myProps.loadingNewPicture = false;
      this.$message.error("上传失败");
    },
    checkFile(file) {
      this.myProps.loadingNewPicture = true;
      var fileExtension = file.name.substring(file.name.lastIndexOf(".") + 1);
      if (file.type.startsWith("image")) {
        if (fileExtension === "gif") {
          this.$message.error("不支持上传gif图片");
          this.myProps.loadingNewPicture = false;
          return false;
        }
      } else {
        this.$message.error("请上传图片");
        this.myProps.loadingNewPicture = false;
        return false;
      }
    },
    handleAvatarSuccess() {
      this.$message({
        message: "上传成功",
        type: "success",
      });
      this.myProps.loadingNewPicture = true;
      setTimeout(() => {
        this.myProps.imageList = [];
        this.getImageList();
      }, 10000);
    },
    downloadAllImage() {
      this.$emit("downloadAllImage");
    },
    deleteAllImage() {
      this.$emit("deleteAllImage");
    },
  },
};
</script>
