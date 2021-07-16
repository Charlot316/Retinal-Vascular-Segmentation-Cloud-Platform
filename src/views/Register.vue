<template>
    <div class="register-wrap">
        <div class="ms-register">
            <div class="ms-title">图书馆信息管理系统</div>
            <el-form :model="param" :rules="rules" ref="register" label-width="0px" class="ms-content">
                <el-form-item prop="username">
                    <el-input v-model="param.username" placeholder="username">
                        <template #prepend>
                            <el-button icon="el-icon-user">用户名</el-button>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input
                        type="password"
                        placeholder="password"
                        v-model="param.password"
                        @keyup.enter="submitForm()"
                    >
                        <template #prepend>
                            <el-button icon="el-icon-lock">密码</el-button>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="email">
                    <el-input v-model="param.email" placeholder="email">
                        <template #prepend>
                            <el-button icon="el-icon-lock">邮箱</el-button>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item label="" prop="sex">
                    <el-radio-group v-model="param.sex" size="medium">
                        <el-radio border label="男"></el-radio>
                        <el-radio border label="女"></el-radio>
                    </el-radio-group>
                </el-form-item>
                <div class="register-btn">
                    <el-button type="primary" @click="submitForm()">注册</el-button>
                </div>
                <h>已有帐号？</h>
                <h class="h"
                ><router-link to="/login">立即登录</router-link></h
                >
            </el-form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        var checkEmail = (rule, value, callback) => {
            const regEmail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((.[a-zA-Z0-9_-]{2,3}){1,2})$/;
            if (regEmail.test(value)) {
                return callback();
            }
            callback(new Error("请输入合法的邮箱"));
        };
        return {
            param: {
                username: "",
                password: "",
                email:"",
                sex:""
            },
            rules: {
                username: [
                    { required: true, message: "请输入用户名", trigger: "blur" },
                    { min: 1,max: 20,message:"用户名长度在1到20个字符",trigger: "blur"}
                ],
                password: [
                    { required: true, message: "请输入密码", trigger: "blur" },
                    {min: 6,max: 15,message: "密码长度在6到15个字符", trigger: "blur"}
                ],
                email: [
                    {required: true, message: "请输入邮箱", trigger: "blur"},
                    {
                        validator: checkEmail,
                        trigger: "blur",
                    }
                ],
                sex: [
                    {requierd: true, message: "请选择性别", trigger: "blur"}
                ]
            }
        };
    },
    created() {
        this.$store.commit("clearTags");
    },
    methods: {
        submitForm() {
            this.$refs.register.validate(async valid => {
                if(!valid){
                    return;
                }
                if(this.param.sex===""){
                    alert("请选择性别")
                }
                else{
                    if(this.param.sex==="男"){
                        this.param.sex = 1
                    }
                    else{
                        this.param.sex = 0
                    }
                    const {data: res } = await this.$http.post('register',this.param);
                    if (res.status !== 200) return this.$message.error('该用户名已被注册！')
                    this.$message.success('注册成功')
                    this.$router.push({path: "/login"})
                }
            })
        }
    }
}
</script>

<style scoped>
.register-wrap {
    position: relative;
    width: 100%;
    height: 100%;
    background-image: url(../assets/img/login.jpg);
    background-size: 100%;
}
.ms-title {
    width: 100%;
    line-height: 50px;
    text-align: center;
    font-size: 20px;
    color: rgb(141, 139, 151);
    border-bottom: 1px solid rgb(87, 107, 163);
}
.ms-register {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 350px;
    margin: -190px 0 0 -175px;
    border-radius: 5px;
    background: rgba(30, 30, 32, 0.3);
    overflow: hidden;
}
.ms-content {
    padding: 30px 30px;
    color: rgb(29, 29, 31);
}
.register-btn {
    text-align: center;
}
.register-btn button {
    width: 100%;
    height: 36px;
    margin-bottom: 10px;
}
.register-tips {
    font-size: 12px;
    line-height: 30px;
    color: #fff;
}
.h{
    color:rgb(129, 109, 83);
}
</style>