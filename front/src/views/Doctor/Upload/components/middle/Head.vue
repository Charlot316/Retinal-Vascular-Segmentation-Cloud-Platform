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
        <el-button
          @click="myProps.visible = true"
          show-file-list="false"
          type="primary"
          icon="el-icon-upload"
          >上传</el-button
        >
      </el-tooltip>
      <!-- 下载全部图片的按钮 -->
      <el-tooltip
        class="item"
        effect="dark"
        content="下载本页所有图片"
        placement="top"
      >
        <el-button
          style="margin-left:30px"
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
        style="width:280px"
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
    downloadAllImage() {
      this.$emit("downloadAllImage");
    },
    deleteAllImage() {
      this.$emit("deleteAllImage");
    },
  },
};
</script>
