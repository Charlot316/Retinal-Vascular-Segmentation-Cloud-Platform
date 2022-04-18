<template>
  <div class="container">
    <div class="display">
      <!-- 显示图片卡片 -->
      <div v-loading="myProps.loadingNewPicture">
        <div v-if="myProps.imageList.length > 0">
          <div
            v-for="singleImage in myProps.imageList"
            :key="singleImage"
            style="margin-top: 20px"
          >
            <photo-card
              :singleImage="singleImage"
              :props="myProps"
              @getImageList="getImageList"
            />
          </div>
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="myProps.pagenum"
            :page-sizes="[1, 3, 5, 10]"
            :page-size="myProps.pagesize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="myProps.total"
          >
          </el-pagination>
        </div>
        <div v-else>
          <el-empty description="暂未上传图片" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PhotoCard from "@/components/Public/PhotoCard.vue";
export default {
  components: {
    PhotoCard,
  },
  data() {
    return {
      myProps: {
        loadingNewPicture: false,
        pagenum: 1,
        pagesize: 5,
        total: 0,
        imageList: [],
      },
    };
  },
  created() {
    this.getImageList();
  },
  methods: {
    handleSizeChange(value) {
      this.myProps.pagesize = value;
      this.getImageList();
    },
    handleCurrentChange(value) {
      this.myProps.pagenum = value;
      this.getImageList();
    },
    async getImageList() {
      this.myProps.loadingNewPicture = true;
      await new Promise((resolve) => {
        this.$http
          .post(
            "/getListForDoctor/",
            JSON.stringify({
              user_id: this.$store.state.user_id,
              pagenum: this.myProps.pagenum,
              pagesize: this.myProps.pagesize,
              title:"",
              showAll:false
            })
          )
          .then((res) => {
            {
              if (res.data.message === "返回list成功") {
                this.myProps.imageList = res.data.imageList;
                this.myProps.total = res.data.total;
              } else {
                this.$message.error("获取列表失败");
              }
              this.myProps.loadingNewPicture = false;
            }
          });
        resolve();
      }).then(() => {});
    },
  },
};
</script>
<style scoped>
.container {
  width: 100%;
  text-align: center;
  background-color: rgb(255, 255, 255, 0);
  padding: 30px;
  border: 0px solid #ddd;
  border-radius: 5px;
}
.display {
  width: 100%;
  margin: 0 auto;
}
</style>
