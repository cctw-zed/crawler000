module.exports = (app) => {
    // 申明变量名，实例化类
    const notes = require('../controllers/note.controller.js');

    // Create a new Note
    //app.post('/api/search', notes.create);

    // Retrieve all Notes
    app.get('/api/search', notes.findAll);
    app.get('/api/spider', notes.canbegin);
    // Retrieve a single Note with noteId
    //app.get('/notes/:noteId', notes.findOne);

    // Update a Note with noteId
    ///app.put('/notes/:noteId', notes.update);

    // Delete a Note with noteId
    //app.delete('/notes/:noteId', notes.delete);
}
