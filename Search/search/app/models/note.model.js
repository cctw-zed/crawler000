const mongoose = require('mongoose');

//按照什么格式去读取
const NoteSchema = mongoose.Schema({
    title : String,
	time : String,
	real_url : String,
	abstract : String,
	keyword : String,
	site : String
});

// 将上面的格式与 Baidu_info 这张表绑定
// Baidu_info 数据库中 Baidu_infos
// 用于保存爬取数据的表
module.exports = mongoose.model('Baidu_info', NoteSchema);
