<template>
  <div class="header">
    <!-- 折叠按钮 -->
    <div class="logo">眼底血管分割云平台</div>
    <div class="header-right">
      <div class="header-user-con">
        <!-- 消息中心 -->
        <!-- <div class="btn-bell">
          <el-tooltip effect="dark" placement="bottom">
            <router-link to="/Notification">
              <i class="el-icon-bell"></i>
            </router-link>
          </el-tooltip>
        </div> -->
        <!-- 用户头像 -->
        <div class="user-avator">
          <router-link to="/doctor/user"> </router-link>
        </div>
        <!-- 用户名下拉菜单 -->
        <el-dropdown class="user-name" trigger="click" @command="handleCommand">
          <span class="el-dropdown-link">
            {{ username }}
            <i class="el-icon-caret-bottom"></i>
          </span>
          <template #dropdown>
            <el-dropdown-menu v-if="islogin">
              <router-link to="/doctor/user" target="_blank">
                <el-dropdown-item>个人信息</el-dropdown-item>
              </router-link>
              <router-link to="/doctor/upload">
                <el-dropdown-item >图像处理</el-dropdown-item>
              </router-link>
              <el-dropdown-item command="loginout"
                >退出登录</el-dropdown-item
              >
            </el-dropdown-menu>
            <el-dropdown-menu v-else>
              <router-link to="/login">
                <el-dropdown-item>前往登录</el-dropdown-item>
              </router-link>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      fullscreen: false,
      name: "linxin",
      message: 2,
    };
  },
  computed: {
    username() {
      let username = this.$store.state.username;
      return username;
      // return username ? username : this.name;
    },
    collapse() {
      return this.$store.state.collapse;
    },
    islogin() {
      return this.$store.state.islogin;
    },
  },
  methods: {
    // 用户名下拉菜单选择事件
    handleCommand(command) {
      if (command == "loginout") {
        this.$store.commit("loginout");
        this.$router.push("/login");
      }
    },
    // 侧边栏折叠
    collapseChage() {
      this.$store.commit("hadndleCollapse", !this.collapse);
    },
  },
  mounted() {
    if (document.body.clientWidth < 1500) {
      this.collapseChage();
    }
  },
};
</script>
<style scoped>
.header {
  position: relative;
  box-sizing: border-box;
  width: 100%;
  height: 70px;
  font-size: 22px;
  color: #fff;
}
.collapse-btn {
  float: left;
  padding: 0 21px;
  cursor: pointer;
  line-height: 70px;
}
.header .logo {
  float: left;
  width: 250px;
  margin-left: 50px;
  line-height: 70px;
}
.header-right {
  float: right;
  padding-right: 50px;
}
.header-user-con {
  display: flex;
  height: 70px;
  align-items: center;
}
.btn-fullscreen {
  transform: rotate(45deg);
  margin-right: 5px;
  font-size: 24px;
}
.btn-bell,
.btn-fullscreen {
  position: relative;
  width: 30px;
  height: 30px;
  text-align: center;
  border-radius: 15px;
  cursor: pointer;
}
.btn-bell-badge {
  position: absolute;
  right: 0;
  top: -2px;
  width: 8px;
  height: 8px;
  border-radius: 4px;
  background: #f56c6c;
  color: #fff;
}
.btn-bell .el-icon-bell {
  color: #fff;
}
.user-name {
  margin-left: 10px;
}
.user-avator {
  margin-left: 20px;
}
.user-avator img {
  display: block;
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
.el-dropdown-link {
  color: #fff;
  cursor: pointer;
}
.el-dropdown-menu__item {
  text-align: center;
}
</style>
