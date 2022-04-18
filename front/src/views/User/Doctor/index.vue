<template>
  <div>
    <v-header />
    <div class="main-content">
      <div class="left">
        <el-affix :offset="80">
          <my-menu :user="user" @changeSelectedMenu="changeSelectedMenu" />
        </el-affix>
      </div>
      <div class="right">
        <div v-if="selectedMenu == 0">
          <my-info @getInfo="getUserInfo" :user="user" />
        </div>
        <div v-if="selectedMenu == 1">
          <photo-list />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import vHeader from "@/components/Doctor/Header";
import MyMenu from "./Menu";
import MyInfo from "./components/info/InfoCard";
import PhotoList from "./components/photo/Middle.vue";
export default {
  components: {
    MyMenu,
    MyInfo,
    vHeader,
    PhotoList,
  },
  data() {
    return {
      user: {},
      selectedMenu: 0,
    };
  },
  created() {
    this.getUserInfo();
    if (this.$route.query.id == this.$store.state.user_id) {
      this.$router.replace({
        path: "/doctor/user",
      });
    }
  },
  methods: {
    changeSelectedMenu(i) {
      this.selectedMenu = i;
    },
    async getUserInfo() {
      await new Promise((resolve) => {
        this.$http
          .post("/getDoctorInfo/", JSON.stringify({ id: this.$route.query.id }))
          .then((res) => {
            if (res.data.success === false)
              return this.$message.error(res.data.message);
            this.user = res.data.user;
          });
        resolve();
      }).then(() => {});
    },
  },
};
</script>

<style scoped>
.main-content {
  overflow: auto;
  height: calc(100vh - 70px);
  width: 100%;
  background-color: #f0f0f0;
}
.left {
  width: 450px;
  padding: 50px;
}
.right {
  width: calc(100vw - 450px);
  margin-left: 350px;
  margin-top: -220px;
  min-width: 800px;
}
</style>
