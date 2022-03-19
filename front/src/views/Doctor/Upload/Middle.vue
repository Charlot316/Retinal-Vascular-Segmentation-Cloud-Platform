<template>
  <div class="container">
    <!-- 顶部操作模块 -->
    <upload-head
      :props="myProps"
      @downloadAllImage="downloadAllImage"
      @deleteAllImage="deleteAllImage"
      @getImageList="getImageList"
    />
    <!-- 显示图片卡片 -->
    <div v-loading="myProps.loadingNewPicture">
      <div
        v-for="singleImage in myProps.imageList"
        :key="singleImage"
        style="margin-top: 20px"
      >
        <photo-card :singleImage="singleImage" :props="myProps" @getImageList="getImageList"/>
      </div>
    </div>
  </div>
</template>

<script>
import UploadHead from "./Head.vue";
import PhotoCard from "./PhotoCard.vue"
export default {
  props: ["props"],
  components: {
    UploadHead,
    PhotoCard,
  },
  data() {
    return {
      myProps: this.props,
    };
  },
  methods: {
    getImageList() {
      this.$emit("getImageList");
    },
    checkFile(file) {
      var fileExtension = file.name.substring(file.name.lastIndexOf(".") + 1);
      if (file.type.startsWith("image")) {
        if (fileExtension === "gif") {
          this.$message.error("不支持上传gif图片");
          return false;
        }
      } else {
        this.$message.error("请上传图片");
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
      }, 7000);
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
