<template>
  <div style="margin:0 auto;text-align:center">
    <div style="margin:0 auto;text-align:center"> 
      <el-tooltip
        class="item"
        effect="dark"
        content="上传新的眼底血管图片"
        placement="right"
      >
          <el-button
            show-file-list="false"
            type="primary"
            icon="el-icon-upload"
            circle
            @click="myProps.visible=true"
          ></el-button>
      </el-tooltip>
    </div>
    <div style="margin:0 auto;text-align:center">
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
    </div>
    <div style="margin:0 auto;text-align:center">
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
    </div>
    <div style="margin:0 auto;text-align:center">
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
