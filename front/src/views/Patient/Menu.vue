<template>
  <div>
    <div class="icon-container">
      <img
        style="width:50px;height:50px;border-radius:50%;object-fit:fill;flex-shrink:0;"
        :src="thisUser.icon"
        onerror="onerror=null;src='https://img0.baidu.com/it/u=3730772664,138405132&fm=26&fmt=auto'"
      />
      <span
        class="user-name"
        style="text-overflow:ellipsis; overflow:hidden;"
        :title="thisUser.name"
      >{{thisUser.name}}</span>
    </div>
    <div class="menu-container">
      <el-menu
        default-active="0"
        class="el-menu-vertical-demo"
        style="width:15vw;"
        @select="handleSelectMenu"
      >
        <el-menu-item index="0">
          <i class="el-icon-document"></i>
          <span class="menu-text">患者信息</span>
        </el-menu-item>
        <el-menu-item index="1">
          <i class="el-icon-menu"></i>
          <span class="menu-text"></span>
        </el-menu-item>

        <el-menu-item index="2">
          <i class="el-icon-user"></i>
          <span class="menu-text">图像列表</span>
        </el-menu-item>
      </el-menu>
    </div>

  </div>
</template>
<script>
export default {
  props: ['user'],
  data() {
    return {
      thisUser: this.user,
    };
  },

  created() {
  },
  methods: {
    handleSelectMenu(index) {
      this.$emit("changeSelectedMenu", index)
    }
  },
  watch: {
    user() {
      this.thisUser = this.user
    }
  }
};
</script>
<style scoped>
.menu-title {
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 800;
  font-size: 25px;
  margin-bottom: 10px;
}
.menu-text {
  font-size: 1vw;
}
.user-name {
  font-size: 25px;
  font-weight: 800;
  margin-left: 10px;
}
.icon-container {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  width: 15vw;
}
.menu-container {
  width: 15vw;
  background-color: rgb(230, 230, 230);
  padding: 1px 0px 1px 1px;
}
</style>