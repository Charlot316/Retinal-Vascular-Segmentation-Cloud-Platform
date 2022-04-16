<template>
  <div>
    <v-header/>
    <div class="main-content">
      <el-row>
        <el-col :span="4">
          <div class="info-sider">
            <el-affix :offset="80">
              <my-menu :user="user" @changeSelectedMenu="changeSelectedMenu" />
            </el-affix>
          </div>
        </el-col>
        <el-col :span="1"> </el-col>
        <el-col :span="18" class="info-content">
          <div>
            <div v-if="selectedMenu == 0">
              <my-info @getInfo="getUserInfo" :user="user" />
            </div>
            <div v-if="selectedMenu == 1"></div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import vHeader from "../../../components/Doctor/Header";
import MyMenu from "./Menu";
import MyInfo from "./components/info/InfoCard";
export default {
  components: {
    MyMenu,
    MyInfo,
    vHeader
  },
  data() {
    return {
      user: {},
      selectedMenu: 0,
    };
  },
  created() {
    this.getUserInfo()
  },
  methods: {
    changeSelectedMenu(i) {
      this.selectedMenu = i;
    },
    async getUserInfo() {
      await new Promise((resolve) => {
        this.$http.post("/getPatientInfo/", JSON.stringify({id:this.$route.query.id})).then((res) => {
          if (res.data.success === false)
            return this.$message.error(res.data.message);
          this.user=res.data.user

          console.log(res)
        });
        resolve();
      }).then(() => {

      });
    },
  },
};
</script>

<style scoped>
.main-content {
  overflow: auto;
  height:calc(100vh - 70px)
}
.info-sider {
  margin-left: 30px;
}
.info-content {
  margin-top: 70px;
  width: 100%;
}
</style>
