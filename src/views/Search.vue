<template>
  <div>
    <!--卡片视图区-->
    <el-card>
      <el-row :gutter="20">
          <!--绑定清空键-->
        <el-col :span="4">
          <el-select
            v-model="operationType"
            placeholder="查看类别"
            class="handle-select mr10"
            id="selecter"
            @change="handlechange"
          >
          <el-option key="1" label="任意词" value="任意词"></el-option>
          <el-option key="2" label="书名" value="书名"></el-option>
          <el-option key="3" label="作者" value="作者"></el-option>
          <el-option key="4" label="出版社" value="出版社"></el-option>
          </el-select>
        </el-col>
        <el-col :span="16">
          <el-input
            v-if="operationType==='任意词'"
            placeholder="请输入书名、作者或出版社的检索关键词"
            v-model="queryInfo.bName"
            clearable
            @clear="getBooksList"
            @keyup.enter="handleSearch"
          ></el-input>
          <el-input
            v-if="operationType==='书名'"
            placeholder="请输入书名检索关键词"
            v-model="queryInfo.bName"
            clearable
            @clear="getBooksList"
            @keyup.enter="handleSearch"
          ></el-input>
          <el-input
            v-if="operationType==='作者'"
            placeholder="请输入作者的关键词"
            v-model="queryInfo.bAuthor"
            clearable
            @clear="getBooksList"
            @keyup.enter="handleSearch"
          ></el-input>
          <el-input
            v-if="operationType==='出版社'"
            placeholder="请输入出版社的关键词"
            v-model="queryInfo.bPublisher"
            clearable
            @clear="getBooksList"
            @keyup.enter="handleSearch"
          ></el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-col>
      </el-row>
      <div class="hot">
        <ul class="myul" >
          <li class="li1">热门检索：</li>
          <li v-for="item in keyWords" :key="item.count" class="li2" @click="searchByKey(item.word)">
            <a>{{item.word}}</a>
          </li>
        </ul>
      </div>
      <!--table表格区域-->
      <el-table :data="booksList" border stripe class="table">
        <el-table-column type="index"></el-table-column>
        <el-table-column
          label="书籍名称"
          prop="bName"
          width="150px"
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
          width="50px"
        ></el-table-column
        ><!--prop用来表明显示数据的名字-->
        <el-table-column
          label="可借数量"
          prop="bInCount"
          width="50px"
        ></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button
              type="primary"
              icon="el-icon-info"
              size="mini"
              @click="viewdetail(scope.$index)"
              >图书详情</el-button
            >
            <el-button
              type="primary"
              icon="el-icon-check"
              size="mini"
              @click="reserveBook(scope.$index)"
              >预约</el-button
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
            <el-button type="primary" @click="reserveBook1">预约</el-button>
          </span>
        </template>
      </el-dialog>
      <!--分页区域-->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryInfo.pagenum"
        :page-sizes="[1, 5, 10, 20]"
        :page-size="queryInfo.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        class="el-pagination"
        background
      >
      </el-pagination>
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
        bAuthor:"",
        bPublisher:"",
        pageNum: 1, //第几页
        pageSize: 5, //每页显示多少个
      },
      operationType:"任意词",
      //书籍列表
      booksList: [],
      //总数据条数
      total: "",
      viewVisible: false,
      form: {},
      reserveDate: "",
      a: "",
      keyWords:[],
      result:[],
    };
  },

  //生命周期函数
  created() {
    this.getBooksList();
    this.getKeyWords();
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
    //点击热门关键词的显示对应的搜索信息
    async searchByKey(key){
      if((this.queryInfo.pageNum-1)*this.queryInfo.pageSize>this.total){
        this.queryInfo.pageNum = 1;
        this.pageSize = 5;
      }
      this.queryInfo.bName = key
      console.log(this.queryInfo)
      const { data: res } = await this.$http.post("searchBook", this.queryInfo);
      this.booksList = res.bookList
      this.getKeyWords()
      if(res.status==422){
        this.total = 0;
        this.queryInfo.pageSize =  5;
        this.queryInfo.pageNum = 1;
      }
      else{
        this.total = res.total;
      }
    },
    handlechange(){
      this.queryInfo.bName="";
      this.queryInfo.bAuthor="";
      this.queryInfo.bPublisher="";
    },
    //获取所有书籍的信息
    async getBooksList() {
      if((this.queryInfo.pageNum-1)*this.queryInfo.pageSize>this.total){
        this.queryInfo.pageNum = 1;
        this.pageSize = 5;
      }
      const { data: res } = await this.$http.post(
        "showAllBookInfo",
        this.queryInfo
      );
      this.booksList = res.bookList;
      this.total = res.total;
    },

    handleSizeChange(newSize) {
      this.queryInfo.pageSize = newSize;
      this.handleSearch();
    },
    handleCurrentChange(newpage) {
      this.queryInfo.pageNum = newpage;
      this.handleSearch();
    },
    viewdetail(index) {
      this.viewVisible = true;
      this.form = this.booksList[index];
    },

    //搜索函数
    async handleSearch() {
      if((this.queryInfo.pageNum-1)*this.queryInfo.pageSize>this.total){
        this.queryInfo.pageNum = 1;
        this.pageSize = 5;
      }
      if(this.operationType==='任意词'){
        const { data: res } = await this.$http.post("searchBook", this.queryInfo);
        this.getKeyWords();
        this.booksList = res.bookList;
        if(res.status==422){
          this.total = 0;
          this.queryInfo.pageSize =  5;
          this.queryInfo.pageNum = 1;
        }
        else{
          this.total = res.total;
        }
      }
      else if(this.operationType==='书名'){
        const { data: res } = await this.$http.post("searchBookByName", this.queryInfo);
        this.getKeyWords();
        this.booksList = res.bookList;
        if(res.status==422){
          this.total = 0;
          this.queryInfo.pageSize =  5;
          this.queryInfo.pageNum = 1;
        }
        else{
          this.total = res.total;
        }
      }
      else if(this.operationType==='作者'){
        const { data: res } = await this.$http.post("searchBookByAuthor", this.queryInfo);
        this.getKeyWords();
        this.booksList = res.bookList;
        if(res.status==422){
          this.total = 0;
          this.queryInfo.pageSize =  5;
          this.queryInfo.pageNum = 1;
        }
        else{
          this.total = res.total;
        }
      }
      else if(this.operationType==='出版社'){
        const { data: res } = await this.$http.post("searchBookByPublisher", this.queryInfo);
        this.getKeyWords();
        this.booksList = res.bookList;
        if(res.status==422){
          this.total = 0;
          this.queryInfo.pageSize =  5;
          this.queryInfo.pageNum = 1;
        }
        else{
          this.total = res.total;
        }
      }
    },
    //获取搜索关键词
    async getKeyWords() {
      const { data: res } = await this.$http.post("getKeyWords");
      this.keyWords = res.result;
    },
    //预约图书函数
    async reserveBook(index) {
      if(!this.$store.state.islogin){
        return this.$message.error("请先登录!")
      }
      if(this.Role!==1){
         return this.$message.error("工作人员不允许预约图书，请使用私人账号预约");
      }
      else{
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
          book_index: this.booksList[index].book_index,
          reserveDate: this.reserveDate,
        });
        if(res.status==410){
          this.$message.error("请先归还超期图书并缴纳罚款！")
        }
        else if(res.status==200){
          const confirmResult = await this.$confirm("您是否确定预约本书?", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
          }).catch((err) => err);

          if (confirmResult !== "confirm") {
            this.viewVisible = false;
            return;
            // return this.$message.info("已经取消预约!");
          }
          this.$message.success("预约成功!");
          this.getBooksList() ;
        }
        else{
          this.$message.error("此图书数量为0，暂时无法预约！")
        }
      }
    },
    async reserveBook1() {
      if(!this.$store.state.islogin){
        return this.$message.error("请先登录!")
      }
      if(this.Role!==1){
        return this.$message.error("工作人员不允许预约图书，请使用私人账号预约");
      }
      else{
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
        if(res.status==410){
          this.$message.error("请先归还超期图书并缴纳罚款！")
        }
        else if(res.status==200){
          const confirmResult = await this.$confirm("您是否确定预约本书?", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
          }).catch((err) => err);

          if (confirmResult !== "confirm") {
            this.viewVisible = false;
            return;
            // return this.$message.info("已经取消预约!");
          }
          this.$message.success("预约成功!")
        }
        else{
          this.$message.error("此图书数量为0，暂时无法预约！")
        }
      }
    },
  },
};
</script>
<style scoped>
.table {
  margin-top: 50px;
}
.center {
  margin-left: 10%;
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
.hot{
  margin-left: 10%;
  margin-top: 15px;
}
.h{
  color: brown;
  list-style-type: none;
  float: flex;
}
.myul{
  margin-top: 5px;
  width:100%;
  list-style-type: none;
}
.myul li{
  padding-left: 1em;
  float: left;
}
.li1{
  color:brown;
}
.li2{
  color:rgb(79, 79, 196);
}
a:hover
{
  background-color:rgb(158, 158, 149);
}
</style>