const express = require('express');
const path = require('path');
const app = express();
const {spawn}=require('child_process');
const routes = require('./server/routes/routes');

var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({extended: false});

app.use(express.static(path.join(__dirname, 'dist/ang-node')));

app.use('/routes', routes);

app.get('/posts', (req, res)=>{
    res.sendFile(path.join(__dirname, 'dist/ang-node/index.html'))
})

const sleep = (n) => new Promise((res) => setTimeout(res, n));

/*async function start(){
    await sleep(5000);
}*/

app.get('/send', (req, res)=>{
    //start();
    res.sendFile(path.join(__dirname, 'dist/ang-node/index.html'))
    //const obj = JSON.parse(JSON.stringify(req.body));
    /*const obj = JSON.parse(JSON.stringify(req.body));
    //console.log(obj.word);
    const childPython = spawn('python', ['./pythonCode/inverted_index.py', obj.word])

    childPython.stdout.on('data', (data) => {
        console.log(`${data}`);
    });
    
    childPython.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });
    
    childPython.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });*/

});

app.post('/send/submit', urlencodedParser, function(req, res){
    const obj = req.body;/*JSON.parse(JSON.stringify(req.body));*/
    console.log(obj.word)
    const spawn = require('child_process').spawn;
    const process = spawn('python', ['./pythonCode/inverted_index.py', obj.word]);

    process.stdout.on('data', data => {
        console.log("dentro");
        res.redirect('/send');
    }).on('end', function() {
        res.redirect('/send');
    });
});

const port = process.env.PORT || 4600;

app.listen(port, (req, res)=>{
    console.log(`RUNNING on port ${port}`);
})