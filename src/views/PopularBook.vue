<template>
  <div>
    <!--卡片视图区-->
    <el-card>
      <el-select
        v-model="operationType"
        placeholder="查看类别"
        class="handle-select mr10"
        id="selecter"
        @change="handlecheck"
      >
        <el-option key="1" label="全部" value="全部"></el-option>
        <el-option key="2" label="航空航天" value="航空航天"></el-option>
        <el-option
          key="3"
          label="数理科学和化学"
          value="数理科学和化学"
        ></el-option>
        <el-option key="4" label="文学" value="文学"></el-option>
        <el-option key="5" label="历史" value="历史"></el-option>
        <el-option key="6" label="计算机" value="计算机"></el-option>
        <el-option key="7" label="社会科学" value="社会科学"></el-option>
        <el-option key="8" label="军事" value="军事"></el-option>
      </el-select>

      <el-button type="primary" icon="el-icon-search" @click="handlecheck"
        >查看</el-button
      >
      <!--table表格区域-->
      <el-table :data="booksList" border stripe class="table">
        <el-table-column type="index" label="排名"></el-table-column>
        <el-table-column
          label="书籍名称"
          prop="bName"
          width="300px"
        ></el-table-column
        ><!--prop用来表明显示数据的名字-->
        <el-table-column
          label="书籍作者"
          prop="bAuthor"
          width="200px"
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
        <!--prop用来表明显示数据的名字-->
        <el-table-column label="查看详情">
          <template #default="scope">
            <el-button
              type="primary"
              icon="el-icon-info"
              @click="viewdetail(scope.$index)"
              >图书详情</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <!--图书详情的弹出框-->
      <el-dialog
        title="图书详情"
        v-model="viewVisible"
        width="50%"
        class="el-dialog"
      >
        <div class="test">
          <el-form ref="form" :model="form" label-width="30%" class="el-form">
            <el-form-item label="图书索引号">
              <el-input v-model="form.book_index" readonly></el-input>
            </el-form-item>
            <el-form-item label="图书名称">
              <el-input v-model="form.bName" readonly></el-input>
            </el-form-item>
            <el-form-item label="图书作者">
              <el-input v-model="form.bAuthor" readonly></el-input>
            </el-form-item>
            <el-form-item label="图书类型">
              <el-input v-model="form.bType" readonly></el-input>
            </el-form-item>
            <el-form-item label="图书出版社">
              <el-input v-model="form.bPublisher" readonly></el-input>
            </el-form-item>
            <el-form-item label="图书馆藏书量">
              <el-input v-model="form.bAllCount" readonly></el-input>
            </el-form-item>
            <el-form-item label="图书在馆数量">
              <el-input v-model="form.bInCount" readonly></el-input>
            </el-form-item>
            <el-form-item label="图书被借次数">
              <el-input v-model="form.bLendCount" readonly></el-input>
            </el-form-item>
            <el-form-item label="图书简介">
              <el-input
                v-model="form.bIntroduction"
                type="textarea"
                :rows="7"
                readonly
              ></el-input>
            </el-form-item>
          </el-form>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="viewVisible = false">取 消</el-button>
            <el-button type="primary" @click="reserveBook1">预定</el-button>
          </span>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      //查询参数对象，与接口文档中传给后端的参数对应
      queryInfo: {
        bName: "", //搜索的关键词
        pageNum: 1, //第几页
        pageSize: 5, //每页显示多少个
      },
      //书籍列表
      booksList: [],
      //总数据条数
      total: "",
      operationType: "全部",
      viewVisible: false,
      form: {},
      reserveDate: "",
      a: "",
    };
  },

  //生命周期函数
  created() {
    this.getBooksList();
  },

  computed: {
    userid() {
      let userid = this.$store.state.user_id;
      return userid;
    },
    Role() {
      let role = this.$store.state.role;
      return role;
    },
  },

  methods: {
    async handlecheck() {
      if (this.operationType === "全部") {
        this.getBooksList();
      } else {
        const { data: res } = await this.$http.post("showTop50ByBType", {
          bType: this.operationType,
        });
        this.booksList = res.top;
      }
    },
    //获取所有书籍的信息
    async getBooksList() {
      const { data: res } = await this.$http.post("showTop50", this.queryInfo);
      this.booksList = res.top;
    },
    viewdetail(index) {
      this.viewVisible = true;
      this.form = this.booksList[index];
    },
    async reserveBook1() {
      if(!this.$store.state.islogin){
        return this.$message.error("请先登录!")
      }
      if(this.Role!==1){
        return this.$message.error("工作人员不允许预约图书，请使用私人账号预约");
      }
      const confirmResult = await this.$confirm("您是否确定预约本书?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).catch((err) => err);

      if (confirmResult !== "confirm") {
        this.viewVisible = false;
        return this.$message.info("已经取消预约!");
      }
      const year = new Date().getFullYear();
      const month =
        new Date().getMonth() + 1 < 10
          ? "0" + (new Date().getMonth() + 1)
          : new Date().getMonth() + 1;
      const date =
        new Date().getDate() < 10
          ? "0" + new Date().getDate()
          : new Date().getDate();
      const hh =
        new Date().getHours() < 10
          ? "0" + new Date().getHours()
          : new Date().getHours();
      const mm =
        new Date().getMinutes() < 10
          ? "0" + new Date().getMinutes()
          : new Date().getMinutes();
      const ss =
        new Date().getSeconds() < 10
          ? "0" + new Date().getSeconds()
          : new Date().getSeconds();
      this.reserveDate =
        year + "-" + month + "-" + date + " " + hh + ":" + mm + ":" + ss;
      const { data: res } = await this.$http.post("reserveBook", {
        user_id: this.userid,
        book_index: this.form.book_index,
        reserveDate: this.reserveDate,
      });
      if (res.status == 200) {
        this.$message.success("预约成功");
      } else {
        this.$message.error("此图书在馆数量为0，暂时无法预约");
      }
    },
  },
};
</script>
<style scoped>
.table {
  margin-top: 20px;
}
.center {
  margin-left: 20%;
}
.el-dailog {
  background: rgb(25, 27, 31);
}
.el-pagination {
  margin-top: 15px;
}
.el-form {
  margin-right: 50px;
}
</style>