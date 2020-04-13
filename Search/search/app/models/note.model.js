const mongoose = require('mongoose');

const NoteSchema = mongoose.Schema({
    title : String,
	time : String,
	real_url : String,
	abstract : String,
	keyword : String,
	site : String
});
// 表的名字
module.exports = mongoose.model('Baidu_info', NoteSchema);
