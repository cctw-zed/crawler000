const Note = require('../models/note.model.js');
const Working = require('../models/working.model.js');
var request = require('request');

// Create and Save a new Note
exports.create = (req, res) => {
    // Validate request
    if(!req.body.content) {
        return res.status(400).send({
            message: "Note content can not be empty"
        });
    }

    // Create a Note
    const note = new Note({
        title: req.body.title || "Untitled Note", 
        content: req.body.content
    });

    // Save Note in the database
    note.save()
    .then(data => {
        res.send(data);
    }).catch(err => {
        res.status(500).send({
            message: err.message || "Some error occurred while creating the Note."
        });
    });
};


//判断是否进行splider
exports.canbegin = (req, res) => {
    let params = req.query;
    //keyword
    let paramskw = params.keyword;
    //captcha
    let paramscap = params.captcha;
    
    if(paramscap != "search")
    {
        let re = {};
        re.feedback = "0";
        res.set({'Access-Control-Allow-Origin': '*'}).send(re);
    }
    else
    {
        Working.find({ keyword: paramskw })
        .then(result => {
            let re = {};
            let len = result.length;
            if(len != 0)
            {
                re.feedback = "1";
            }
            else
            {
                Working.insertMany([{keyword: paramskw}],{safe:true},function(err,result){console.log(result);});
                request.post({url:'http://localhost:5000/my_easy_class/api', form:{
                "keyword" : paramskw
                }}, function(error, response, body) {
                    console.log(error);
                })
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


// Retrieve and return all notes from the database.
exports.findAll = (req, res) => {
    let params = req.query;
    let paramskw = params.keyword;
    const reg = new RegExp(paramskw, 'i')
    let paramspi = params.pageIndex;
    paramspi = Number(paramspi);
    let paramsppn = params.perPageNumber;
    paramsppn = Number(paramsppn);

    Note.find({  keyword : {$regex : reg} })
    .then(notes => {
        let len = notes.length;
	let re = {};
	if(len == 0)
	{ 
        re = {}; 
        re.success = false; 
    }
	else
	{
	let max_number = paramspi * paramsppn;
        let begin;
        if(max_number > len)
        {
            begin = len - paramsppn;
        }
        else
        {
            begin = paramsppn * (paramspi - 1);
        }
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

// Find a single note with a noteId
exports.findOne = (req, res) => {
    Note.findById(req.params.noteId)
    .then(note => {
        if(!note) {
            return res.status(404).send({
                message: "Note not found with id " + req.params.noteId
            });            
        }
        res.send(note);
    }).catch(err => {
        if(err.kind === 'ObjectId') {
            return res.status(404).send({
                message: "Note not found with id " + req.params.noteId
            });                
        }
        return res.status(500).send({
            message: "Error retrieving note with id " + req.params.noteId
        });
    });
};

// Update a note identified by the noteId in the request
exports.update = (req, res) => {
    // Validate Request
    if(!req.body.content) {
        return res.status(400).send({
            message: "Note content can not be empty"
        });
    }

    // Find note and update it with the request body
    Note.findByIdAndUpdate(req.params.noteId, {
        title: req.body.title || "Untitled Note",
        content: req.body.content
    }, {new: true})
    .then(note => {
        if(!note) {
            return res.status(404).send({
                message: "Note not found with id " + req.params.noteId
            });
        }
        res.send(note);
    }).catch(err => {
        if(err.kind === 'ObjectId') {
            return res.status(404).send({
                message: "Note not found with id " + req.params.noteId
            });                
        }
        return res.status(500).send({
            message: "Error updating note with id " + req.params.noteId
        });
    });
};

// Delete a note with the specified noteId in the request
exports.delete = (req, res) => {
    Note.findByIdAndRemove(req.params.noteId)
    .then(note => {
        if(!note) {
            return res.status(404).send({
                message: "Note not found with id " + req.params.noteId
            });
        }
        res.send({message: "Note deleted successfully!"});
    }).catch(err => {
        if(err.kind === 'ObjectId' || err.name === 'NotFound') {
            return res.status(404).send({
                message: "Note not found with id " + req.params.noteId
            });                
        }
        return res.status(500).send({
            message: "Could not delete note with id " + req.params.noteId
        });
    });
};
