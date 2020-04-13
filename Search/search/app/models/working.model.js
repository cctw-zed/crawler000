const mongoose = require('mongoose');

const WorkingSchema = mongoose.Schema({
	keyword: String
});
// 表的名字
module.exports = mongoose.model('Working', WorkingSchema);