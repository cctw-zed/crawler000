module.exports = (app) => {
    // 申明变量名，实例化类
    const notes = require('../controllers/note.controller.js');
    // 定义api，对应，例如：localhost:3000/api/search
    // 第一个参数是路径，第二个参数对应note.controller.js里面的函数
    // 注意前面的函数
    // 分别对应 .get .post .put
    app.get('/api/search', notes.findAll);
    // 定义api，对应，例如：localhost:3000/api/spider
    app.get('/api/spider', notes.canbegin);
}
