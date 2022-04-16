<template>
  <div>
    <div class="main-content">
      <el-row>
        <el-col :span="4">
          <div class="info-sider">
            <el-affix :offset="80">
              <my-menu
                :user="user"
                @changeSelectedMenu="changeSelectedMenu"
              />
            </el-affix>
          </div>
        </el-col>
        <el-col :span="1">
        </el-col>
        <el-col
          :span="18"
          class="info-content"
        >
          <div>
            <div v-if="selectedMenu==0">
              <my-info
                @getInfo="getUserInfo"
                :user="user"
              />
            </div>
            <div v-if="selectedMenu==1">
              
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import MyMenu from './Menu'
import MyInfo from './components/info/InfoCard'
export default {
  components: {
    MyMenu,
    MyInfo,
  },
  data() {
    return {
      user: {
       
      },
      currentUser: {},
      selectedMenu: 0,
    }
  },
  created() {
   

  },
  methods: {
    changeSelectedMenu(i) {
      this.selectedMenu = i
    },

     getUserInfo() {
     
    }
  }
}
</script>

<style scoped>
.main-content {
  overflow: auto;
  height:100vh;
}
.info-sider {
  margin-left: 30px;
}
.info-content {
  margin-top: 70px;
  width: 100%;
}
</style>