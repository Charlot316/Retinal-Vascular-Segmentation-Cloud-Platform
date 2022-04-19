<template>
   <div>
    <v-header />
    <div class="main-content">
      <div class="doctor-left">
        <my-menu :user="user" @changeSelectedMenu="changeSelectedMenu" />
      </div>
      <div class="doctor-right">
        <div class="right-content">
        <div v-if="selectedMenu == 0">
          <my-info @getInfo="getUserInfo" :user="user" />
        </div>
        <div v-if="selectedMenu == 1">
          <photo-list />
        </div>
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
  },
  methods: {
    changeSelectedMenu(i) {
      this.selectedMenu = i;
    },
    async getUserInfo() {
      await new Promise((resolve) => {
        this.$http
          .post(
            "/getDoctorInfo/",
            JSON.stringify({ id: this.$store.state.user_id})
          )
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
  min-width:1120px;
  background-color: #f0f0f0;
}
.doctor-left {
  width: 200px;
  padding: 50px;

}
.doctor-right {
  width: calc(100vw - 450px);
  float:left;
  margin-top:-220px;
  margin-left:300px;
}
.right-content{
  width:940px;
  margin: 0 auto;
}
</style>
