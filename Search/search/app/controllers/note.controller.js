// 实例化Node，对应这个model文件
const Note = require('../models/note.model.js');
// 实例化Working，同上
const Working = require('../models/working.model.js');
// 实例化request
var request = require('request');
// 实例化nodejieba
var nodejieba = require('nodejieba');

//判断是否进行splider
exports.canbegin = (req, res) => {
    // 获取参数
    let params = req.query;
    // keyword，获取参数中的keyword字段
    let paramskw = params.keyword;
    // captcha，获取参数中的 验证码 字段
    let paramscap = params.captcha;
    // 如果验证码验证失败，返回 feedback = "0"
    if(paramscap != "search")
    {
        let re = {};
        re.feedback = "0";
        res.set({'Access-Control-Allow-Origin': '*'}).send(re);
    }
    // 如果验证成功
    else
    {
        // workings表用于保存当前关键字是否正在被爬取
        // 从workings表中查找当前关键字
        Working.find({ keyword: paramskw })
        .then(result => {
            let re = {};
            let len = result.length;
            // 如果查找到，返回 feedback = "1"
            if(len != 0)
            {
                re.feedback = "1";
            }
            // 如果没有查找到
            // 三步
            // 第一，保存关键字
            // 第二，发送请求给python（爬虫）服务器
            // 第三，返回 feedback = "2"
            else
            {
                // 如果查找到
                // 将现在这个关键字插入到workings表中
                Working.insertMany([{keyword: paramskw}],
                    {safe:true},
                    function(err,result)
                    {
                        console.log(result);
                    });
                // 向 python服务器（爬虫模块）发送请求
                request.post({url:'http://localhost:5000/my_easy_class/api', 
                form:{
                    "keyword" : paramskw
                }}, 
                function(error, response, body) {
                    console.log(error);
                });
                re.feedback = "2";
            }
            res.set({'Access-Control-Allow-Origin': '*'}).send(re);
        }).catch(err => {
            res.status(500).send({
                message: err.message || "Some error occurred while retrieving notes."
            });
        });
    }
};


// 查询所有满足条件的数据
exports.findAll = (req, res) => {
    // 获得参数
    let params = req.query;
    // 获得参数相应的字段
    let paramskw = params.keyword;

    // 正则表达式匹配
    var cut_keyword = nodejieba.cut(paramskw);
    console.log(cut_keyword);
    var blurry_cut_keyword = [];
    for(var item of cut_keyword)
    {
        var temp = new RegExp(item);
        blurry_cut_keyword.push(temp);
    }

    let paramspi = params.pageIndex;
    // 强制性转换成数字类型
    paramspi = Number(paramspi);
    let paramsppn = params.perPageNumber;
    paramsppn = Number(paramsppn);

    // 用或进行查找,同时进行模糊查找
    Note.find({  keyword : {"$in": blurry_cut_keyword} })
    .then(notes => {
        let len = notes.length;
    let re = {};
    // 如果没有查找到，返回 success = false
	if(len == 0)
	{ 
        re = {}; 
        re.success = false; 
    }
    // 如果查找到
    // 根据用户输入的 页码 和 每页的item数，返回数据还有 success = true
	else
	{
	    let max_number = paramspi * paramsppn;
        let begin;
        // 如果申请的超过了当前最大数目
        if(max_number > len)
        {
            begin = len - paramsppn;
        }
        // 如果没有超过，正常计算
        else
        {
            begin = paramsppn * (paramspi - 1);
        }
        // 切割结果，类似于  array[begin : begin+paramsppn]
        notes = notes.slice(begin, Number(begin) + Number(paramsppn));
        re.success = true;
        re.pageindex = paramspi;
        re.totalnumber = len;
        let data = {};
        let contentlist = [];
        for(let i = 0; i<notes.length; i++)
        {
                
            let item = notes[i];
            let temp = {};
            // 前面是前端需要的字段名，后面是数据库中对应的字段名
            temp.content = item.abstract || "None"; 
            temp.title = item.title || "None";
            temp.time = item.time || "None";
            temp.url = item.real_url || "None";
            temp.platform = item.site || "Node";

            contentlist.push(temp);
        }
        data.contentlist = contentlist;
        re.data = data;
	}
        res.set({'Access-Control-Allow-Origin': '*'}).send(re);
    }).catch(err => {
        res.status(500).send({
            message: err.message || "Some error occurred while retrieving notes."
        });
    });
};