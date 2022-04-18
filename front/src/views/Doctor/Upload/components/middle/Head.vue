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
          style="margin-left:20px"
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
        v-if="!myProps.showAll"
      >
        <el-button
          style="margin-left:20px"
          @click="deleteAllImage()"
          type="danger"
          icon="el-icon-delete"
          >清空</el-button
        >
      </el-tooltip>
    </div>
    <div>
       <el-tooltip
        class="item"
        effect="dark"
        style="margin-right:20px"
        :content="myProps.showAll?'当前：全部显示 点按以只显示自己上传的图片':'当前：只显示自己上传的图片 点按以显示所有图片'"
        placement="top"
      >
        <el-switch active-text="全部"
    inactive-text="自己" v-model="myProps.showAll" @change="getImageList"/>
      </el-tooltip>
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
