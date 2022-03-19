<template>
  <el-card shadow="hover">
    <!-- 卡片头栏 -->
    <template #header>
      <div class="card-header">
        <span>
          <span>{{ singleImage.photo_realname }}</span>
          <!-- 修改名字 -->
          <el-popover placement="right" width="400" trigger="click">
            <template #reference>
              <el-button
                style="margin-right:10px"
                icon="el-icon-edit"
                type="text"
                circle
                @click="myProps.newName = singleImage.photo_realname"
              ></el-button>
            </template>
            <el-input
              v-model="myProps.newName"
              @keyup.enter="revisePictureName(singleImage)"
              placeholder="请输入修改后的图片名称"
              clearable
            >
              <template #append>
                <el-button
                  @click="revisePictureName(singleImage)"
                  icon="el-icon-check"
                ></el-button>
              </template>
            </el-input>
          </el-popover>
        </span>
        <span>
          <!-- 下载图片 -->
          <el-button
            @click="downloadASetOfImage(singleImage)"
            style="margin-right:10px"
            icon="el-icon-download"
            >下载全部</el-button
          >
          <!-- 删除图片 -->
          <el-button
            @click="deleteAGroupOfImage(singleImage)"
            type="danger"
            icon="el-icon-delete"
            >删除全部</el-button
          >
        </span>
      </div>
    </template>
    <!-- 三张图片 -->
    <el-row>
      <el-col :span="8">
        <el-card :body-style="{ padding: '0px' }">
          <el-image
            lazy
            style="width: 100%;"
            :src="singleImage.photo_origin"
            class="image"
            :preview-src-list="[
              singleImage.photo_origin,
              singleImage.photo_upload,
              singleImage.photo_promap,
            ]"
          >
            <!-- 图片加载出错的情况 -->
            <template #error>
              <div class="image-slot">
                <el-image
                  lazy
                  style="width: 100%;"
                  :src="require('../../../assets/img/loading.gif')"
                  class="image"
                />
                <div style="text-align:center;">
                  <h3 style="text-align:center">
                    图片加载中，请稍后刷新
                  </h3>
                  <el-button @click="getImageList">强制刷新</el-button>
                </div>
              </div>
            </template>
          </el-image>
          <div style="padding: 14px">
            <span>原始图片</span>
            <div class="bottom">
              <el-button
                type="text"
                class="button"
                @click="
                  downloadIamge(
                    singleImage.photo_origin,
                    singleImage.photo_savename + '_origin'
                  )
                "
                >下载图片</el-button
              >
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card :body-style="{ padding: '0px' }">
          <el-image
            lazy
            style="width: 100%;"
            :src="singleImage.photo_upload"
            class="image"
            :preview-src-list="[
              singleImage.photo_upload,
              singleImage.photo_promap,
              singleImage.photo_origin,
            ]"
          >
            <template #error>
              <div class="image-slot">
                <el-image
                  style="width: 100%;"
                  :src="require('../../../assets/img/loading.gif')"
                  class="image"
                />
                <div style="text-align:center;">
                  <h3 style="text-align:center">
                    图片加载中，请稍后刷新
                  </h3>
                  <el-button @click="getImageList">强制刷新</el-button>
                </div>
              </div>
            </template>
          </el-image>
          <div style="padding: 14px">
            <span>黄金指标</span>
            <div class="bottom">
              <el-button
                type="text"
                class="button"
                @click="
                  downloadIamge(
                    singleImage.photo_upload,
                    singleImage.photo + '_upload'
                  )
                "
                >下载图片</el-button
              >
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card :body-style="{ padding: '0px' }">
          <el-image
            style="width: 100%;"
            :src="singleImage.photo_promap"
            class="image"
            :preview-src-list="[
              singleImage.photo_promap,
              singleImage.photo_origin,
              singleImage.photo_upload,
            ]"
          >
            <template #error>
              <div class="image-slot">
                <el-image
                  style="width: 100%;"
                  :src="require('../../../assets/img/loading.gif')"
                  class="image"
                />
                <div style="text-align:center;">
                  <h3 style="text-align:center">
                    图片加载中，请稍后刷新
                  </h3>
                  <el-button @click="getImageList">强制刷新</el-button>
                </div>
              </div>
            </template>
          </el-image>
          <div style="padding: 14px">
            <span>生成图片</span>
            <div class="bottom">
              <el-button
                type="text"
                class="button"
                @click="
                  downloadIamge(
                    singleImage.photo_promap,
                    singleImage.photo_savename + '_promap'
                  )
                "
                >下载图片</el-button
              >
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </el-card>
</template>
<script>
import { ElMessageBox, ElMessage } from "element-plus";
export default {
  
  props: ["props","singleImage"],
  components: {
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
    async deleteASetOfImage(singleImage) {
      await new Promise((resolve) => {
        this.$http
          .post(
            "/deletePicture/",
            JSON.stringify({ photoID: singleImage.photo_id })
          )
          .then((res) => {
            {
              if (res.data.message === "删除成功") {
                this.getImageList();
              } else {
                this.$message.error("删除失败");
              }
            }
          });
        resolve();
      }).then(() => {});
    },
    deleteAGroupOfImage(singleImage) {
      ElMessageBox.confirm(
        "本操作无法撤回，您确认要清空这三张图片吗？",
        "Warning",
        {
          confirmButtonText: "OK",
          cancelButtonText: "Cancel",
          type: "warning",
        }
      )
        .then(() => {
          this.deleteASetOfImage(singleImage);
          ElMessage({
            type: "success",
            message: "删除成功",
          });
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "删除被取消",
          });
        });
    },
    async revisePictureName(singleImage) {
      if (this.props.newName.trim().length == 0)
        return this.$message.error("图片命名不能为空");
      await new Promise((resolve) => {
        this.$http
          .post(
            "/revisePictureName/",
            JSON.stringify({
              photoID: singleImage.photo_id,
              newName: this.props.newName,
            })
          )
          .then((res) => {
            {
              if (res.data.message === "修改成功") {
                singleImage.photo_realname = this.props.newName;
                this.$message.success("图片名修改成功");
              } else {
                this.$message.error("修改失败");
              }
            }
          });
        resolve();
      }).then(() => {});
    },
  },
};
</script>


