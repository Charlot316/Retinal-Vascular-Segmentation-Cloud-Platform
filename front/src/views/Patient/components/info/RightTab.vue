<template>
  <div>
    <div class="icon-box">
      <img
        style="width:150px;height:150px;border-radius:50%;object-fit:fill;"
        :src="user.icon"
        onerror="onerror=null;src='https://img0.baidu.com/it/u=3730772664,138405132&fm=26&fmt=auto'"
      />
    </div>
    <br />
    <div v-if="mode==0">
      <el-upload
        class="upload-demo"
        action="http://119.3.233.208:8090/api/imageUpload"
        :on-success="onSuccess"
        :on-preview="handlePreview"
        accept=".jpg, .png"
        :limit="1"
        list-type=false
        :show-file-list="false"
        with-credentials="true"
      >
        <el-button
          class="edit-button-upload"
          type="info"
          plain
        >上传头像</el-button>
      </el-upload>
      <br />
      <el-button
        class="edit-button"
        type="info"
        @click="changeEditMode"
        plain
      >编辑信息</el-button>

    </div>
    <div v-else>
      <el-button
        class="edit-button"
        type="info"
        @click="editFinished"
        plain
      >修改完成</el-button>

      <el-button
        class="edit-button"
        type="info"
        @click="editCanceled"
        plain
      >取消修改</el-button>

    </div>
  </div>
</template>
<script>
import { ElNotification } from 'element-plus'
export default {
  props: ['user'],
  data() {
    return {
      thisUser: this.user,
      mode: 0,//0:展示信息的状态 1:编辑信息的状态
      changePassword: false,
      param: {
        oldPassword: '',
        newPassword: '',
        newPassword2: '',
      },
      tmpEducation: '',
    };
  },

  created() {
  },
  methods: {
    changeEditMode() {
      if (this.mode == 0) this.mode = 1;
      else this.mode = 0;
      this.$emit('fatherChangeEditMode', this.mode)
    },
    //编辑完成
    async editFinished() {
      if (this.mode == 0) this.mode = 1;
      else this.mode = 0;
      this.$emit('fatherChangeEditMode', this.mode)
     
      
      this.$emit('getInfo')
    },
   
    //上传头像
    onSuccess() {
      ElNotification({
        title: '成功',
        message: '上传成功！',
        type: 'success',
      });
      this.$emit('getInfo');
    },
    handlePreview(file) {
      window.open(file.response.url);
    },
    //取消修改
    async editCanceled() {
      this.$emit('getInfo');
      if (this.mode == 0) this.mode = 1;
      else this.mode = 0;
      this.$emit('fatherChangeEditMode', this.mode)
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
.edit-button {
  width: 60%;
  margin: 8px;
  margin-bottom: 26px;
}

.edit-button-upload {
  width: 100%;
  /* margin: 8px; */
}
.icon-box {
  display: flex;
  justify-content: center;
  align-items: center;
}
.upload-demo {
  width: 60%;
  margin-top: 6px;
  margin-bottom: 6px;
  margin-left: 20%;
  display: flex;
  justify-content: center;
  /* margin: 8px; */
}
</style>

<style>
.el-upload {
  width: 100%;
}
</style>