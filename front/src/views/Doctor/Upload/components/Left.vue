<template>
  <div style="margin-left:6vw;">
    <el-row>
      <el-tooltip
        class="item"
        effect="dark"
        content="上传新的眼底血管图片"
        placement="right"
      >
        <el-upload
          class="upload-demo"
          :action="myProps.baseURL + 'receive/'"
          :data="{ user_id: $store.state.user_id }"
          :on-success="handleAvatarSuccess"
          list-type="false"
          :show-file-list="false"
          :before-upload="checkFile"
          name="pic_img"
        >
          <el-button
            show-file-list="false"
            type="primary"
            icon="el-icon-upload"
            circle
          ></el-button>
        </el-upload>
      </el-tooltip>
    </el-row>
    <el-row>
      <el-tooltip
        class="item"
        effect="dark"
        content="下载本页所有图片"
        placement="right"
      >
        <el-button
          style="margin-top:25px"
          type="success"
          icon="el-icon-download"
          @click="downloadAllImage()"
          circle
        ></el-button>
      </el-tooltip>
    </el-row>
    <el-row>
      <el-tooltip
        class="item"
        effect="dark"
        content="清空本页所有图片"
        placement="right"
      >
        <el-button
          style="margin-top:25px"
          @click="deleteAllImage()"
          type="danger"
          icon="el-icon-delete"
          circle
        ></el-button>
      </el-tooltip>
    </el-row>
    <el-row>
      <el-tooltip
        class="item"
        effect="dark"
        content="搜索图片"
        placement="right"
      >
        <div>
          <el-popover placement="right" :width="400" trigger="click">
            <template #reference>
              <el-button
                style="margin-top:25px"
                type="info"
                icon="el-icon-search"
                circle
              ></el-button>
            </template>
            <div>
              <el-input
                v-model="myProps.searchTitle"
                @keyup.enter="getImageList"
                placeholder="请输入图片名"
                clearable
              >
                <template #append>
                  <el-button
                    @click="getImageList"
                    icon="el-icon-search"
                  ></el-button>
                </template>
              </el-input>
            </div>
          </el-popover>
        </div>
      </el-tooltip>
    </el-row>
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
      this.myProps.loadingNewPicture = true;
    },
    handleAvatarSuccess() {
      this.$message({
        message: "上传成功",
        type: "success",
      });
      this.myProps.loadingNewPicture = true;
      this.getImageList();
      // setTimeout(() => {
      //   this.myProps.imageList = [];
      //   this.getImageList();
      // }, 7000);
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
