<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card shadow="hover" class="mgb20" style="height: 252px">
          <div class="user-info">
            <img src="../assets/img/user.jpg" class="user-avator" alt />
            <div class="user-info-cont">
              <div class="user-info-name">{{ username }}</div>
              <div class="role">{{ role }}</div>
            </div>
          </div>
          <div class="user-operation">
            <el-button
              type="primary"
              class="operation"
              size="mini"
              @click="showSelfInfo"
              >查看个人信息</el-button
            >
            <el-button
              type="primary"
              class="operation"
              size="mini"
              @click="showChangePassword"
              >修改密码</el-button
            >
            <el-button
              type="primary"
              class="operation"
              size="mini"
              @click="showChangeInformation"
              >修改信息</el-button
            >
          </div>
        </el-card>
          <div v-if="Role===1">
            <el-card shadow="hover" style="height: 252px">
              <template #header>
                <div class="h2">
                  <span>已阅图书种类</span>
                </div>
              </template>
              <div
                v-for="(item, key, i) in progressData"
                :key="i"
                style="padding-bottom: 0.625rem"
              >
                {{ key
                }}<el-progress
                  :percentage="parseInt(item)"
                  :color="progressColor[i]"
                ></el-progress>
              </div>
              <div style="margin-top: 50px">
                <p><img src="../assets/img/搜索.png" /><h class="h">借阅分析</h></p>
                <p class="font">在所有读者中</p>
                <p class="font1">
                  排在<h class="font2">{{ getpercent+'%' }}</h
                  >的人之前
                </p>
                <p class="font3">
                  <el-progress
                    :text-inside="true"
                    :stroke-width="26"
                    :percentage="getpercent"
                  ></el-progress>
                </p>
              </div>
            </el-card>
          </div>
          <div v-if="Role!==1">
            <el-card shadow="hover" class="mgb20" style="height: 252px">
              <template #header>
                  <h1>发布通知</h1>
              </template>
              <el-row>
                <el-input
                  v-model="form.message"
                  placeholder="请输入需要发送的信息"
                  class="handle-input mr10"
                  @keyup.enter="sendMessage"
                ></el-input>
              </el-row>
              <el-row>
                <div>
                  <el-button
                      @click="sendMessage"
                      >发送</el-button
                    >
                </div>
              </el-row>
            </el-card>
            <div>
              <el-card shadow="hover">
                <template #header>
                  <h1>借阅情况</h1>
                </template>
                <keep-alive>
                <div class="pie">
                    <div id="pie1">
                        <!-- 为 ECharts 准备一个具备大小（宽高）的 DOM -->
                        <div id="main1" class="charts" style="float:left;width:100%;height: 300px"></div>
                    </div>
                </div>
                </keep-alive>
              </el-card>
            </div>
          </div>
      </el-col>
      <el-col :span="16">
        <el-card  v-if="Role!==1" shadow="hover" style="margin-bottom: 20px" >
          <template #header>
            <div class="clearfix">
                <h1>工作人员处理模块</h1>
            </div>
          </template>
          <el-row :gutter="20" class="mgb20">
            <el-col :span="8">
              <el-card :shadow="hover">
                <img fit="fit" src="../assets/img/数据.png" class="image" />
                <div style="padding: 14px">
                  <h2>图书管理</h2>
                  <div style="margin-top:20px">
                  <el-button @click=hrefone>操作</el-button>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card :shadow="hover">
                <img fit="fit" src="../assets/img/借书.png" class="image" />
                <div style="padding: 14px">
                  <h2>借阅管理</h2>
                  <div style="margin-top:20px">
                  <el-button @click=hreftwo>操作</el-button>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card :shadow="hover">
                <img fit="fit" src="../assets/img/用户管理.png" class="image" />
                <div style="padding: 14px">
                  <h2>用户管理</h2>
                  <div style="margin-top:20px">
                  <el-button @click=hrefthree>操作</el-button>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
        <div v-if="Role===1">
          <el-row :gutter="20" class="mgb20">
          <el-col :span="8">
            <el-card
              shadow="hover"
              :body-style="{ padding: '0px' }"
              @click="browseReserved"
            >
              <div class="grid-content grid-con-1">
                <i class="el-icon-reading grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ totalreserved }}</div>
                  <div>已预约图书</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card
              shadow="hover"
              :body-style="{ padding: '0px' }"
              @click="browseReturned"
            >
              <div class="grid-content grid-con-2">
                <i class="el-icon-reading grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ totalReturned }}</div>
                  <div>已归还图书</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card
              shadow="hover"
              :body-style="{ padding: '0px' }"
              @click="browseTobe"
            >
              <div class="grid-content grid-con-3">
                <i class="el-icon-reading grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ totalTobe }}</div>
                  <div>在借图书</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <div>
          <el-card shadow="hover" style="height: 100px">
            <template #header>
              <div class="clearfix">
                <span class="h1">超期未归还图书</span>
                <!-- <el-button style="float: right; padding: 3px 0" type="text">添加</el-button> -->
              </div>
            </template>
            <el-table :show-header="true" :data="todoList" style="width: 100%">
              <el-table-column type="index"></el-table-column>
              <el-table-column
                label="书籍名称"
                width="200px"
                prop="bName"
              ></el-table-column>
              <el-table-column label="借阅时间" prop="lDate"></el-table-column>
              <el-table-column label="应还时间" prop="dDate"></el-table-column>
              <el-table-column width="60">
                <template>
                  <i class="el-icon-edit"></i>
                  <i class="el-icon-delete"></i>
                </template>
              </el-table-column>
            </el-table>
            <div style="margin-top: 50px">
              <p>
                <img src="../assets/img/排行榜.png" /><h class="h"
                  >借阅时间分布</h
                >
              </p>
              <div id="volume" class="charts"></div>
            </div>
          </el-card>
        </div>
        </div>
        <div  v-if="Role!==1"  >
          <el-card shadow="hover" class="mgb20" >
              <template #header>
                  <div class="clearfix">
                      <h1>热门借阅</h1>
                  </div>
              </template>
              <el-table
              :data="rbInformation.slice(0,5)"
              style="width: 100%">
                <el-table-column type="index" label="排名" width="50px"></el-table-column>
                <el-table-column
                  label="书籍名称"
                  prop="bName"
                  width="150px"
                ></el-table-column
                ><!--prop用来表明显示数据的名字-->
                <el-table-column
                  label="书籍作者"
                  prop="bAuthor"
                  width="150px"
                ></el-table-column
                ><!--prop用来表明显示数据的名字-->
                <el-table-column label="书籍类型" prop="bType"></el-table-column
                ><!--prop用来表明显示数据的名字-->
                <el-table-column label="书籍出版社" prop="bPublisher"></el-table-column
                ><!--prop用来表明显示数据的名字-->
                <el-table-column
                  label="馆藏数量"
                  prop="bAllCount"
                  width="100px"
                ></el-table-column
                ><!--prop用来表明显示数据的名字-->

                <el-table-column
                  label="借阅次数"
                  prop="bLendCount"
                  width="100px"
                ></el-table-column>
              </el-table>
            </el-card>
        </div>

      </el-col>
    </el-row>

    <!--编辑用户查看个人信息的弹出框-->
    <el-dialog
      title="查看个人信息"
      v-model="editVisible_showUserInfo"
      width="30%"
    >
      <el-form label-width="100px" :model="userInfo">
        <el-form-item label="用户编号">
          <el-input v-model="userInfo.user_id" readonly></el-input>
        </el-form-item>
        <el-form-item label="用户名称">
          <el-input v-model="userInfo.username" readonly></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="userInfo.email" readonly></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-input v-model="userInfo.sex" readonly></el-input>
        </el-form-item>
        <el-form-item label="借阅数量">
          <el-input v-model="userInfo.uLendCount" readonly></el-input>
        </el-form-item>
      </el-form>
    </el-dialog>
    <!--编辑用户修改密码的弹出框-->
    <el-dialog
      title="修改密码"
      v-model="editVisible_changepassword"
      width="30%"
    >
      <el-form label-width="100px" :model="param" :rules="rules">
        <el-form-item label="原密码" prop="oldpassword">
          <el-input
            type="password"
            autocomplete="off"
            v-model="param.oldpassword"
          ></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newpassword">
          <el-input
            type="password"
            autocomplete="off"
            v-model="param.newpassword"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="ensurepassword">
          <el-input
            type="password"
            autocomplete="off"
            v-model="param.ensurepassword"
            @keyup.enter="changepassword"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="changepassword">确定</el-button>
          <el-button @click="quit_changepassword">返回</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <!--编辑用户修改信息的弹出框-->
    <el-dialog
      title="修改个人信息"
      v-model="editVisible_changeinformation"
      width="30%"
    >
      <el-form label-width="100px">
        <el-form-item label="新Email">
          <el-input
            autocomplete="off"
            v-model="newEmail"
            @keyup.enter="changeinformation"
          ></el-input>
        </el-form-item>
        <el-form-item label="新用户名">
          <el-input
            autocomplete="off"
            v-model="newName"
            @keyup.enter="changeinformation"
          ></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="newSex">
            <el-radio :label="1">男</el-radio>
            <el-radio :label="0">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="changeinformation">确定</el-button>
          <el-button @click="quit_changeinformation">返回</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
// 引入饼状图组件
// require('echarts/lib/chart/pie')
// // 引入提示框和title组件
// require('echarts/lib/component/tooltip')
// require('echarts/lib/component/title')
export default {
  type: "user",
  data() {
    return {
      //借阅量占比
      percentage: "",
      //超期图书列表
      todoList: [],
      //不同借阅比例对应的颜色
      progressColor: [
        "#1bf8f3",
        "#f1e05a",
        "#3196e8",
        "#feb046",
        "#e8484f",
        "#9174e4",
        "#f56c6c",
      ],
      //已借图书种类排行
      progressData: [],
      //已预约图书弹出框信息
      bookInfo: {
        user_id: "",
        pageSize: 1,
        pageNum: 1,
      },
      //修改密码的信息
      param: {
        oldpassword: "",
        newpassword: "",
        ensurepassword: "",
      },
      //密码校验规则
      rules: {
        oldpassword: [
          { required: true, message: "请输入原密码", trigger: "blur" },
          { min: 6, max: 15, message: "长度在6到15个字符", trigger: "blur" },
        ],
        newpassword: [
          { required: true, message: "请输入新密码", trigger: "blur" },
          { min: 6, max: 15, message: "长度在6到15个字符", trigger: "blur" },
        ],
        ensurepassword: [
          { required: true, message: "请确认密码", trigger: "blur" },
          { min: 6, max: 15, message: "长度在6到15个字符", trigger: "blur" },
        ],
      },
      oldEmail: "",
      newEmail: "",
      newName:"",
      userName: "",
      newSex: "",
      totalreserved: "",
      totalReturned: "",
      totalTobe: "",
      data: [],
      form:{},
      userInfo: {},
      options: {
        type: "bar",
      },
      options2: {
        type: "line",
      },
      viewVisible: false,
      editVisible_reserved: false,
      editVisible_returned: false,
      editVisible_tobe: false,
      editVisible_changepassword: false,
      editVisible_changeinformation: false,
      editVisible_showUserInfo: false,
      reservedList: [],
      returnedList: [],
      tobeList: [],
      rbInformation:[],
      lendingTime: []
    };
  },
  computed: {
    top() {
      let tmp = 200;
      return tmp;
    },
    role() {
      if (this.Role===1)
      return "普通用户";
      else if(this.Role===2)
      return "工作人员";
      else
      return "超级管理员" ;
    },
    username() {
      let username = this.$store.state.username;
      return username;
    },
    userid() {
      let userid = this.$store.state.user_id;
      return userid;
    },
    Role() {
      let role = this.$store.state.role;
      return role;
    },
    getpercent(){
      let per = 100 - parseFloat(this.percentage);
      return per;
    }
  },

  created() {
    this.getNum();
    this.showUserLendingBookType();
    this.showOverdueBook();
    this.showLendingBoard();
    this.getUserName();
    this.getrbInformation();
    this.getLendingTime();
  },
  mounted() {
    // this.drawBar();
    this.initPieData();
  },
  activated(){
    this.drawBar();
  },
  methods: {
    async getrbInformation(){
      const { data: res } = await this.$http.post("showTop50", this.queryInfo);
      this.rbInformation = res.top;
    },
    getUserName() {
      this.userName = this.$store.state.username
    },
    hrefone() {
      this.$router.push({ path: "/adminbook" });
    },
    hreftwo() {
      this.$router.push({ path: "/adminrb" });
    },
    hrefthree() {
      this.$router.push({ path: "/adminuser" });
    },
    hreffour() {
      this.$router.push({ path: "/adminpunish" });
    },
    //展示不同种类借书排行的颜色
    customColorMethod(val) {
      return this.progressColor[val];
    },
    showChangePassword() {
      this.editVisible_changepassword = true;
    },
    showChangeInformation() {
      this.editVisible_changeinformation = true;
      this.getUserInfo();
    },
    async showLendingBoard() {
      const { data: res } = await this.$http.post("showLendingBoard", {
        user_id: this.userid,
      });
      this.percentage = res.percentage;
    },
    async showOverdueBook() {
      const { data: res } = await this.$http.post("showOverdueBook", {
        user_id: this.userid,
      });
      this.todoList = [];
      if (res.status == 200) {
        for (let i = 0; i < res.list.length; i++) {
          let model = {};
          model["user_id"] = res.list[i].user_id;
          model["book_id"] = res.list[i].book_id;
          model["dDate"] = res.list[i].dDate;
          model["lDate"] = res.list[i].lDate;
          model["bName"] = res.bookList[i];
          this.todoList[i] = model;
        }
      }
    },
    async getNum() {
      this.bookInfo.user_id = this.userid;
      const { data: res1 } = await this.$http.post(
        "showReservedBook",
        this.bookInfo
      );
      const { data: res2 } = await this.$http.post(
        "showLendingBook",
        this.bookInfo
      );
      const { data: res3 } = await this.$http.post(
        "showReturnedBook",
        this.bookInfo
      );
      if (res1.status == 200) {
        this.totalreserved = res1.total;
      } else {
        this.totalreserved = 0;
      }
      if (res2.status == 200) {
        this.totalTobe = res2.total;
      } else {
        this.totalTobe = 0;
      }
      if (res3.status == 200) {
        this.totalReturned = res3.total;
      } else {
        this.totalReturned = 0;
      }
    },
    browseReserved() {
      this.user_id = this.userid;
      this.$router.push({
        name: "ShowReserveBook",
        params: { user_id: this.user_id },
      });
    },
    browseReturned() {
      this.user_id = this.userid;
      this.$router.push({
        name: "ShowReturnedBook",
        params: { user_id: this.user_id },
      });
    },
    browseTobe() {
      this.user_id = this.userid;
      this.$router.push({
        name: "ShowTobeList",
        params: { user_id: this.user_id },
      });
    },
    async changepassword() {
      const { data: res } = await this.$http.post("showUserInfo", {
        user_id: this.userid,
      });
      if (this.param.newpassword !== this.param.ensurepassword) {
        alert("新密码与确认密码不一致，请重新输入");
      } else if (this.param.oldpassword !== res.password) {
        alert("旧密码输入错误");
      } else if (this.param.oldpassword === this.param.newpassword) {
        alert("您输入的新密码和旧密码不能相同");
      } else {
        const { data: tmp } = await this.$http.post("changeUserPassword", {
          user_id: this.userid,
          password: this.param.newpassword,
        });
        if (tmp.status == 200) {
          alert("修改密码成功");
          (this.editVisible_changepassword = false),
            (this.param.oldpassword = ""),
            (this.param.newpassword = ""),
            (this.param.ensurepassword = "");
        }
      }
    },
    async sendMessage(){
      const confirmResult = await this.$confirm("按下确定后所有用户都将收到这条消息，是否确认发布？", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }).catch((err) => err);

        if (confirmResult !== "confirm") {
          return this.$message.info("已经取消信息发布");
        }
      const { data: res } = await this.$http.post("sendMessage", this.form);
      //this.$message.success(JSON.stringify(this.form));
      if (res.status !== 200) {
        return this.$message.error(res.message);
      } else {
        this.$message.success("消息发布成功");
      }
    },
    async changeinformation() {
      const { data: res } = await this.$http.post("showUserInfo", {
        user_id: this.userid,
      });
      if (this.newName === "") {
        alert("用户名不能为空")
      }
      else {
        const { data: tmp } = await this.$http.post("updateUserInfo", {
          user_id: this.userid,
          username: this.newName,
          email: this.newEmail,
          sex: this.newSex,
          // sex: (res.sex = res.sex === "男" ? 1 : 0),
          password: res.password,
        });
        if (tmp.status == 200) {
          this.$store.commit("changeName",this.newName);
          this.getUserName();
          alert("修改个人信息成功！");
          this.editVisible_changeinformation = false;
        }
        else if(tmp.status == 422){
          alert("用户名已存在！")
        }
      }
    },
    async showUserLendingBookType() {
      const { data: res } = await this.$http.post("showUserLendingBookType", {
        user_id: this.userid,
      });
      this.progressData = res.map;
    },
    quit_changepassword() {
      this.editVisible_changepassword = false;
    },
    quit_changeinformation() {
      this.editVisible_changeinformation = false;
    },
    viewdetail(index, type) {
      this.viewVisible = true;
      if (type === 1) this.form = this.reservedList[index];
      else if (type === 2) this.form = this.returnedList[index];
      else this.form = this.tobeList[index];
    },
    async showSelfInfo() {
      this.editVisible_showUserInfo = true;
      const { data: res } = await this.$http.post("showUserInfo", {
        user_id: this.userid,
      });
      console.log(res);
      this.userInfo = res;
    },
    async getUserInfo(){
      const { data: res } = await this.$http.post("showUserInfo", {
        user_id: this.userid,
      });
      this.newEmail = res.email
      this.newName = res.username
      this.newSex = (res.sex === '男') ? 1 : 0
    },
    async initPieData() {
      if(this.Role===1) return;
      // 基于准备好的dom，初始化echarts实例
      var ele1 = document.getElementById("main1")
      ele1.removeAttribute('_echarts_instance_')
      let myChart = this.$echarts.init(ele1);
      const { data: res } = await this.$http.post("getRateByType",this.form);
      myChart.setOption({
          title : {
              text: '分类借阅占比',//主标题
              x:'center',//x轴方向对齐方式
          },
          tooltip : {
              trigger: 'item',
              formatter: "{a} <br/>{b} : {c} ({d}%)"
          },
          legend: {
              orient: 'vertical',
              bottom: 'bottom',
          },
          series : [
              {
                  name: '借阅分布',
                  type: 'pie',
                  radius : '55%',
                  center: ['50%', '60%'],
                  data:[
                      {value:res.result["航空航天"], name:'航空航天'},
                      {value:res.result["数理科学和化学"], name:'数理科学化学'},
                      {value:res.result["文学"], name:'文学'},
                      {value:res.result["历史"], name:'历史'},
                      {value:res.result["计算机"], name:'计算机'},
                      {value:res.result["社会科学"], name:'社科'},
                      {value:res.result["军事"], name:'军事'},
                  ],
                  itemStyle: {
                      emphasis: {
                          shadowBlur: 10,
                          shadowOffsetX: 0,
                          shadowColor: 'rgba(0, 0, 0, 0.5)'
                      }
                  }
              }
          ]
      });
    },
    async getLendingTime() {
      const { data: res } = await this.$http.post("showLendingTime", {
        user_id: this.userid,
      });
      this.lendingTime = res.month
      this.drawBar()
    },
    async drawBar() {
      if(this.Role!==1) return;
      var ele = document.getElementById("volume")
      ele.removeAttribute('_echarts_instance_')
      let charts = this.$echarts.init(ele);
      console.log("绘制")
      charts.setOption({
        title: { text: "" },
        tooltip: {},
        legend: {
          data: ["借阅数量"],
        },
        xAxis: {
          data: [
            "1月",
            "2月",
            "3月",
            "4月",
            "5月",
            "6月",
            "7月",
            "8月",
            "9月",
            "10月",
            "11月",
            "12月",
          ],
        },
        yAxis: {
          type: 'value',
          interval: 1,
          // min: 0,
          // max: 10
        },
        series: [
          {
            name: "借阅数量",
            type: "line",
            data: Object.values(this.lendingTime),
            areaStyle: {
                normal: {}
            }
          },
        ],
      });
    },
  },
};
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
}

.grid-content {
  display: flex;
  align-items: center;
  height: 100px;
}

.grid-cont-right {
  flex: 1;
  text-align: center;
  font-size: 14px;
  color: #999;
}

.grid-num {
  font-size: 30px;
  font-weight: bold;
}

.grid-con-icon {
  font-size: 50px;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
  color: #fff;
}

.grid-con-1 .grid-con-icon {
  background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
  color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
  background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
  color: rgb(45, 140, 240);
}

.grid-con-3 .grid-con-icon {
  background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
  color: rgb(242, 94, 67);
}

.handle-input {
  width: 600px;
  display: inline-block;
}

.user-info {
  display: flex;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #ccc;
  margin-bottom: 20px;
}

.role {
  margin-top: 30px;
}

.user-avator {
  width: 120px;
  height: 120px;
  border-radius: 50%;
}

.user-info-cont {
  padding-left: 50px;
  flex: 1;
  font-size: 14px;
  color: #999;
}

.user-info-cont div:first-child {
  font-size: 30px;
  color: #222;
}

.user-info-list {
  font-size: 14px;
  color: #999;
  line-height: 25px;
}

.user-opertion span {
  margin-left: 70px;
}

.mgb20 {
  margin-bottom: 20px;
}

.todo-item {
  font-size: 14px;
}

.todo-item-del {
  text-decoration: line-through;
  color: #999;
}
.operation1 {
  margin-left: 15%;
}
.operation2 {
  margin-left: 20%;
}
.el-card {
  border: 1 #222;
}
.h {
  margin-left: 20px;
  margin-top: 5px;
  font-size: 20px;
  font-weight: bold;
  color: rgb(37, 40, 190);
}
.h1 {
  color: red;
  font-size: 20px;
  font-weight: bold;
}
.h2 {
  color: blue;
  font-size: 20px;
  font-weight: bold;
}
.charts {
  width: 600px;
  height: 400px;
}
.calc {
  width: 900px;
  margin-top: 200px;
}
.font {
  font-size: 20px;
  margin-top: 10px;
}
.font1 {
  margin-left: 50px;
  margin-top: 10px;
}
.font2 {
  font-size: 30px;
  color: coral;
}
.font3 {
  margin-top: 10px;
}
</style>
