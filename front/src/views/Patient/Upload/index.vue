<template>
  <div style="width: 70%;margin-left: 30px;margin-top: 30px;">
    <el-table
      :data="content"
      style="width: 100%;">
      <el-table-column
        prop="info"
        label="实时执行日志"
      >
      </el-table-column>
    </el-table>
    <br>
    <el-button type="primary" @click="onSubumit">提交</el-button>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        content:[],
      }
    },
    mounted: function() {

    },
    methods: {
      onSubumit(){
        // 清空消息
        this.content = []
        // 执行webSocket
        this.webSocket()
      },
      webSocket() {
        const _this = this;
        if (typeof (WebSocket) == 'undefined') {
          this.$notify({
            title: '提示',
            message: '当前浏览器无法接收实时报警信息，请使用谷歌浏览器！',
            type: 'warning',
            duration: 0
          });
        } else {
          // 实例化socket
          const socketUrl = 'ws://127.0.0.1:8000/wx/';
          this.socket = new WebSocket(socketUrl);
          // 监听socket打开
          this.socket.onopen = function() {
            console.log('浏览器WebSocket已打开');
            //发送字符:
            _this.socket.send(JSON.stringify({
              'username': "xiao",
              'msg': "hello",
            }));
          };
          // 监听socket消息接收
          this.socket.onmessage = function(msg) {
            // 追加到内容显示列表中
            _this.content.push({"info":msg.data})
          };
          // 监听socket错误
          this.socket.onerror = function() {
            _this.$notify({
              title: '错误',
              message: '服务器错误，无法接收实时报警信息',
              type: 'error',
              duration: 0
            });
          };
          // 监听socket关闭
          this.socket.onclose = function() {
            console.log('WebSocket已关闭');
          }
        }
      },
    }
  }
</script>

<style>
</style>