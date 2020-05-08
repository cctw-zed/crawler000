const mongoose = require('mongoose');

const WorkingSchema = mongoose.Schema({
	keyword: String
});

// 用于保存当前是否在爬取的关键字表
module.exports = mongoose.model('Working', WorkingSchema);