<template>
  <!-- <div
    class="icon-container"
    style="cursor:pointer;"
    @click="$router.push({ path: '/research', query: { id: user.id }})"
  > -->
  <router-link target="_blank" :to="{ path: '/patient' , query: { id: user.id } }">
  <div
    class="icon-container"
    style="cursor:pointer;"
  >
    <img
      style="width:70px;height:70px;border-radius:50%;object-fit:fill;"
      :src="user.icon"
      onerror="onerror=null;src='https://img0.baidu.com/it/u=3730772664,138405132&fm=26&fmt=auto'"
    />
    <div class="icon-info">
      <div>
        <el-row>
          <span
            class="user-name"
            :title="user.name"
          >{{user.name}}</span>
        </el-row>
        <el-row>
          <span
            class="info"
            :title="user.isDoctor ? '医生' : '患者'"
          > {{user.isDoctor ? '医生' : '患者'}}</span>
        </el-row>
        <el-row>
          <span
            class="info"
            :title="user.age+'岁'"
          > {{user.age?user.age+'岁':'未填写年龄'}}</span>
        </el-row>
      </div>
    </div>
  </div>
  </router-link>
</template>

<script>
export default {
  props: ['user'],
  data() {
    return {

    };
  },

  created() {
  },
  methods: {
   
  },
};
</script>

<style scoped>
.icon-container {
  display: flex;
  align-items: left;
  min-width: 20vw;
  overflow: hidden;
  text-overflow: ellipsis;
}
.icon-info {
  margin-left: 10px;
}
.user-name {
  text-align: center;
  font-size: 18px;
  max-width: 18vw;
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: rgb(4, 15, 47);
}
.info {
  font-size: 15px;
  color: #696969;
  max-width: 18vw;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>