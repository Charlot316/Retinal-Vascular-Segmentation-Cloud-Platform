<template>
  <div>
   
  </div>
</template>

<script>
export default {
  props: {
    method: {
      type: String,
      default: 'mail'
    }
  },
  data() {
    return {
      code: '',
      errorCode: false,
      clicked: false
    }
  },
  updated() {
    //console.log(this.method);
  },
  methods: {
    submit() {
      this.clicked = true
      let authorId = this.$route.query.authorid
      //console.log(authorId);
      this.errorCode = !this.code.length > 0;
      if (!this.errorCode) {
        this.$http.get(`api/verifyEmail?code=${this.code}&authorId=${authorId}`).then(res => {
          if (res.data.code == 0) {
            this.$notify({
              title: '成功',
              message: '邮件验证成功',
              type: 'success',
            })
            this.$store.commit("login", {
              username: this.$store.state.user.username,
              isAdministrator: this.$store.state.user.isAdministrator,
              iconUrl: this.$store.state.user.iconUrl,
              authorId: this.$route.query.authorid,
              password: this.$store.state.user.password,
              isAdminLogin: this.$store.state.user.isAdminLogin,
            })
            this.$emit('next-step');
          }
          this.clicked = false;
        })
      }
      // this.$emit('next-step');
      return;
    }
  },
}
</script>

<style scoped>
.box-card {
  width: 900px;
  margin: 0 auto;
}
.identify-choose {
  display: inline-block;
  width: 230px;
  height: 120px;
  margin: 30px;
  border: solid 1px rgb(116, 179, 242);
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.identify-choose :hover {
  cursor: pointer;
}
.hint:hover {
  cursor: pointer;
}
.error-tip {
  color: red;
  font-size: 12px;
  padding-top: 10px;
}
</style>